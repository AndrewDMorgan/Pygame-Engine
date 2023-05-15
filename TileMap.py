import pygame, math


# ===================================================================================================================
#           Tilemap Stuff
# ===================================================================================================================


# a constant for a blank tile (aka an air tile or something)
blankTile = pygame.Surface((0, 0))
blankTile.set_colorkey((0, 0, 0))


# a tile map
class TileMap:
    # initializing the data
    def __init__(self, tileMapFile: str, tiles: list, tileSize: int) -> None:
        # loading the map
        self.map = [[int(j) for j in i.split(",")] for i in open(tileMapFile).read().split("\n")]

        # initializing the variables/parameters
        self.tileSize = tileSize
        self.tiles = tiles

        # getting the size of the map
        self.mapSize = (len(self.map), len(self.map[0]))

    # gets the position of a point in grid space
    def GetGridPosition(self, point: tuple) -> tuple:
        return (round(point[0] // self.tileSize), round(point[1] // self.tileSize))

    # gets a tile
    def GetTileNumber(self, xy: tuple) -> object:
        # getting the tile and making sure the point isn't out of bounds
        if xy[0] not in range(0, self.mapSize[0]) or xy[1] not in range(0, self.mapSize[1]):
            return -1
        return self.map[xy[1]][xy[0]]

    # renders the map to a surface
    def Render(self, screen: object, cameraPos: tuple, screenSize: tuple) -> None:
        # getting the offset of the tileMap based on the camera pos and stuff
        offset = [self.tileSize - (cameraPos[0] % self.tileSize), self.tileSize - (cameraPos[1] % self.tileSize)]
        offset[0] -= (cameraPos[0] // self.tileSize+1) * self.tileSize# + self.tileSize//2
        offset[1] -= (cameraPos[1] // self.tileSize+1) * self.tileSize# + self.tileSize//2
        offset[0] += screenSize[0]//2
        offset[1] += screenSize[1]//2
        offset = [round(offset[0]), round(offset[1])]

        # getting the position of the edges of the map
        rightPos = offset[0] + self.mapSize[0]
        bottomPos = offset[1] + self.mapSize[1]

        # getting the overlap of the edges of the screen and the map
        rightOverlap = screenSize[0] - rightPos
        bottomOverlap = screenSize[1] - bottomPos

        # constraining the bounds of the map
        left = min(math.floor(max(-offset[0], 0) / self.tileSize), self.mapSize[0]-1)
        top = min(math.floor(max(-offset[1], 0) / self.tileSize), self.mapSize[1]-1)
        right = min(math.ceil(max(rightOverlap+12, 0) / self.tileSize), self.mapSize[0]-1)
        bottom = min(math.ceil(max(bottomOverlap+12, 0) / self.tileSize), self.mapSize[1]-1)

        # rendering the tiles
        for x in range(left, right):
            for y in range(top, bottom):
                screen.blit(self.tiles[self.map[y][x]], (x * 64 + offset[0], y * 64 + offset[1]))


