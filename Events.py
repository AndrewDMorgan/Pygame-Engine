from enum import Enum
import pygame, sys


# ===================================================================================================================
#           An Event Manager
# ===================================================================================================================


# the mouse states
class MouseStates (Enum):
    pressed = 0
    held = 1
    realeased = 2
    up = 3


# manages events
class Manager:
    def __init__(self) -> None:
        # getting the mouses current position
        self.mousePos = pygame.mouse.get_pos()

        # the events that have happened
        self.events = []
        self.typed = []
        self.held = []

        # the state of the mouse
        self.mouseStates = {"left": MouseStates.up, "right": MouseStates.up}
    
    # gets the relative mouse position (compared to a point)
    def GetRelativeMousePos(self, pos: tuple) -> tuple:
        return (self.mousePos[0] - pos[0], self.mousePos[1] - pos[1])
    
    # gets the events
    def GetEvents(self) -> None:
        # updating the mouse pos
        self.mousePos = pygame.mouse.get_pos()

        # resetting the events and type characters
        self.events = []
        self.typed = []

        # updating the mouses state
        for key in self.mouseStates:
            if self.mouseStates[key] == MouseStates.pressed:
                self.mouseStates[key] = MouseStates.held
            elif self.mouseStates[key] == MouseStates.realeased:
                self.mouseStates[key] = MouseStates.up

        # going through all the events
        for event in pygame.event.get():
            # checking if the window has been closed
            if event.type == pygame.QUIT:
                # stopping the program
                pygame.quit()
                sys.exit()
            
            # checking if a key was pressed down or up
            elif event.type == pygame.KEYDOWN:
                self.events.append(event.key)
                self.held.append(event.key)
            elif event.type == pygame.KEYUP:
                self.held.remove(event.key)
        
            # updating the mouses state
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # left click
                    self.mouseStates["left"] = MouseStates.pressed
                elif event.button == 3:  # right click
                    self.mouseStates["right"] = MouseStates.pressed
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:  # left click
                    self.mouseStates["left"] = MouseStates.realeased
                elif event.button == 3:  # right click
                    self.mouseStates["right"] = MouseStates.realeased

            # checking if a character was typed (for typing boxes)
            if event.type == pygame.TEXTINPUT:
                self.typed.append(event.text)


