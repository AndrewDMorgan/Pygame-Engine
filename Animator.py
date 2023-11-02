from Pygen import Sprites, Events
from types import FunctionType
import pygame

# ===================================================================================================================
#           Loading An Animation
# ===================================================================================================================


# loads an animation     {Walking: {"speed": 1, "reset": False, sprites: [1, 2, 3, 4]}}
def LoadAnimation(sprites: list, baseState: int, animationInformation: dict, stateFunction: FunctionType) -> object:
    # copying the dictionary so nothing is messed up
    animations = {state: {key: animationInformation[state][key] for key in animationInformation[state]} for state in animationInformation}

    # loading the sprites into the animation
    for state in animations:
        stateSprites = []
        for spriteIndex in animations[state]["sprites"]:
            stateSprites.append(sprites[spriteIndex])
        animations[state]["sprites"] = stateSprites

    # returning it in an Animation object
    return Animation(baseState, animations, stateFunction)


# ===================================================================================================================
#           Animation
# ===================================================================================================================


# a class for an animation
class Animation:
    # initializing information about the animation
    def __init__(self, baseState: int, animations: dict, stateFunction: FunctionType) -> None:
        self.state = baseState
        # {Walking: {"speed": 1, "reset": False, "sprites": []}}
        self.animations = animations  # a dictionary with a dictionary for every state with a speed (for the animation), a list of sprites, and a boolean for if it should reset the frame counter when swtiching to it
        self.stateFunction = stateFunction  # returns the new state when given the events and dt
        self.frame = 0
    
    # updating the animation
    def Update(self, events: Events.Manager, dt: float, playDirection: int=1) -> None:
        # updating the state
        oldState = self.state
        self.state = self.stateFunction(events, dt)

        # udpating the frame count
        if oldState != self.state and self.animations[self.state]["reset"]:
            self.frame = 0
        else:
            self.frame += self.animations[self.state]["speed"] * playDirection * dt
    
    # renders the animation
    def Render(self, screen: pygame.Surface, position: tuple) -> None:
        sprites = self.animations[self.state]["sprites"]
        screen.blit(sprites[int(self.frame % len(sprites))], position)
    
    # gets the3 current sprite
    def GetCurrentSprite(self) -> pygame.Surface:
        sprites = self.animations[self.state]["sprites"]
        return sprites[int(self.frame % len(sprites))]

