import pygame
import os


class Animation:
    def __init__(self, images, max_animation, current_animation=0):
        """
        :param images: Liste d'images pour l'animation.
        :param max_animation: Le nombre d'animations dans la liste.
        :param current_animation: L'index de l'animation actuellement affichée.
        """
        self.images = images  # Liste des images d'animation
        self.max_animation = max_animation  # Nombre total d'animations
        self.current_animation = current_animation  # Animation actuelle

    def next_animation(self):
        """Avance à la prochaine animation dans la liste."""
        self.current_animation = (self.current_animation + 1) % self.max_animation
        return self.images[self.current_animation]

    def reset(self):
        """Réinitialise l'animation à la première image."""
        self.current_animation = 0


class ImageManager:
    def __init__(self):
        self.root = {}  # Le répertoire racine où seront stockés les dossiers et les images

    def add_image(self, path, image_path, image_size=None):
        """Ajoute une image à un dossier spécifié dans l'arborescence."""
        path_parts = path.split("/")  # Découpe le chemin en parties (dossier1/dossier2/...)
        folder = self.root

        # Parcours des dossiers jusqu'à celui spécifié
        for part in path_parts[:-1]:
            folder = folder.setdefault(part, {})

        # Ajout de l'image dans le dossier final
        image_name = os.path.basename(image_path)
        image = pygame.image.load(image_path).convert_alpha()
        if image_size:
            image = pygame.transform.scale(image, image_size)
        folder[image_name] = image

    def add_image_set(self, path, image_paths, image_size=None):
        """Ajoute un ensemble d'images à un dossier."""
        path_parts = path.split("/")
        folder = self.root

        # Parcours des dossiers jusqu'à celui spécifié
        for part in path_parts[:-1]:
            folder = folder.setdefault(part, {})

        # Ajoute les images à cet emplacement
        for image_path in image_paths:
            image_name = os.path.basename(image_path)
            image = pygame.image.load(image_path).convert_alpha()
            if image_size:
                image = pygame.transform.scale(image, image_size)
            folder[image_name] = image

    def create_animation(self, path, images, max_animation, current_animation=0):
        """Crée une animation à partir d'une liste d'images et l'ajoute au dossier spécifié."""
        path_parts = path.split("/")
        folder = self.root

        # Parcours des dossiers jusqu'à celui spécifié
        for part in path_parts[:-1]:
            folder = folder.setdefault(part, {})

        # Crée l'animation et l'ajoute dans le dossier
        animation = Animation(images, max_animation, current_animation)
        folder["animation"] = animation

    def get_image(self, path):
        """Récupère une image à partir d'un chemin dans l'arborescence."""
        path_parts = path.split("/")
        folder = self.root

        for part in path_parts:
            folder = folder.get(part, {})

        return folder if isinstance(folder, pygame.Surface) else None

    def get_animation(self, path):
        """Récupère une animation à partir d'un chemin dans l'arborescence."""
        path_parts = path.split("/")
        folder = self.root

        for part in path_parts:
            folder = folder.get(part, {})

        return folder.get("animation") if isinstance(folder, dict) else None

    def update_animation(self, path):
        """Met à jour l'animation pour obtenir la prochaine image."""
        animation = self.get_animation(path)
        if animation:
            return animation.next_animation()
        return None

    def draw_image(self, screen, path, position, scale=None):
        """Dessine une image à l'écran."""
        image = self.get_image(path)
        if image:
            if scale:
                image = pygame.transform.scale(image, scale)
            screen.blit(image, position)
        else:
            print(f"L'image à {path} n'a pas été trouvée.")

    def draw_animation(self, screen, path, position, scale=None):
        """Dessine l'image de l'animation à l'écran."""
        image = self.update_animation(path)
        if image:
            if scale:
                image = pygame.transform.scale(image, scale)
            screen.blit(image, position)
        else:
            print(f"L'animation à {path} n'a pas été trouvée.")

    def load_assets(self, assets_dir):
        """Charge automatiquement tous les fichiers d'un répertoire d'assets, y compris les animations."""
        for root_dir, subdirs, files in os.walk(assets_dir):
            # Récupère le chemin relatif du dossier
            folder_path = os.path.relpath(root_dir, assets_dir)

            # Vérifie si ce répertoire contient des images
            image_files = [f for f in files if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]

            if image_files:
                # Ajoute les images au dossier
                for image_file in image_files:
                    image_path = os.path.join(root_dir, image_file)
                    self.add_image(folder_path, image_path)

            # Vérifie si ce répertoire pourrait être une animation
            image_files_sorted = sorted(image_files)
            if len(image_files_sorted) > 1 and self._is_possible_animation(image_files_sorted):
                # Crée une animation si plusieurs images semblent liées
                images = [pygame.image.load(os.path.join(root_dir, file)).convert_alpha() for file in
                          image_files_sorted]
                self.create_animation(folder_path, images, len(images))

    def _is_possible_animation(self, files):
        """Vérifie si les fichiers dans le dossier sont numérotés et peuvent constituer une animation."""
        try:
            indices = [int(f.split('_')[-1].split('.')[0]) for f in files]
            return all(indices[i] + 1 == indices[i + 1] for i in range(len(indices) - 1))
        except ValueError:
            return False  # Si les fichiers ne sont pas numérotés correctement


import pygame
import os

# Initialisation de Pygame
pygame.init()

# Créer la fenêtre
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Afficher l'image")

# Définir le chemin de l'image
image_path = os.path.join("../assets", "conveyors", "armored-conveyor-0-0.png")

# Charger l'image
image = pygame.image.load(image_path).convert_alpha()

# Boucle de jeu principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dessiner l'image à la position (100, 100)
    screen.fill((0, 0, 0))  # Remplir l'écran de noir (optionnel)
    screen.blit(image, (100, 100))  # Dessiner l'image à la position (100, 100)

    pygame.display.flip()  # Actualiser l'affichage

# Quitter Pygame
pygame.quit()
