from tile import Tile, Conveyer, Starter


def get_color(param):
    if isinstance(param, str):
        class_name = param
    elif hasattr(param, '__class__'):
        class_name = param.__class__.__name__
    else:
        raise TypeError("Le paramètre doit être une classe sous forme de chaîne ou une instance d'objet.")

    if class_name == Tile.__name__:
        return 255, 0, 0
    elif class_name == Conveyer.__name__:
        return 0, 255, 0
    elif class_name == Starter.__name__:
        return 0, 0, 255
    else:
        raise KeyError(f"Couleur pour {class_name} non trouvée.")