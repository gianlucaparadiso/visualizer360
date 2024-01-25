from matplotlib import cm


def createPalette(palette_name: str, palette_size: int):
    return cm.get_cmap(palette_name, palette_size)


def createSPalette(palette_name: str):
    return cm.get_cmap(palette_name)
