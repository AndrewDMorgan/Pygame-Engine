import pygame


# ===================================================================================================================
#           Spritesheet Loading
# ===================================================================================================================


# loads a spritesheet
def LoadSpritesheet(image: pygame.Surface, tileSize: tuple, transColor: tuple=(0,0,0)) -> list:
    # finding the number of sprites
    imageSize = image.get_size()
    numAcross = imageSize[0] // tileSize[0]
    numHigh = imageSize[1] // tileSize[1]

    # all the sprites
    sprites = []

    # looping through all the sprites
    for y in range(numHigh):
        for x in range(numAcross):
            # creating the indivdual tile and adding it
            surf = pygame.Surface((tileSize[0], tileSize[1]))
            surf.fill(transColor)
            surf.set_colorkey(transColor)
            surf.blit(image, [-x*tileSize[0], -y*tileSize[1]])
            sprites.append(surf)

    # returning the sprites
    return sprites


# scales a list of sprites to a new size
def ScaleSprites(sprites: list, scale: tuple) -> list:
    # scaling all the sprites
    scaled = []
    for sprite in sprites:
        scaled.append(pygame.transform.scale(sprite, scale))
    
    # returning the scaled sprites
    return scaled

