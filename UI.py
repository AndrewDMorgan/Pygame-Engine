from Pygen import Events  # for the event manager
from enum import Enum  # for enums (great for representing states)
import pygame  # for pygame (duh)


# ===================================================================================================================
#           Text Rendering
# ===================================================================================================================


# renders text but also cashes some aspects (make it more cashable)   (good fonts) https://www.1001fonts.com/pixel+video-game-fonts.html
class TextRenderer:
    def __init__(self, size: int, font: str, text: str, pos: tuple, color: tuple, centered: bool=False, trans: int=255) -> None:
        # initializing the parameters
        self.size = size
        self.font = font
        self.text = text
        self.pos = pos
        self.color = color
        self.centered = centered
        self.trans = trans

        # getting the color to replace as transparent
        self.transColor = (0, 0, 0)
        if self.color == (0, 0, 0):  # making sure black text still works with transparecy
            self.transColor = (255, 255, 255)
        
        # generating the text
        self.sprite = self.Update()
    
    # updates the cashed render
    def Update(self) -> pygame.Rect:
        # creating the font
        self.Font = pygame.font.Font(self.font, self.size)
        
        # creating the text surface
        TextSurf = self.Font.render(self.text, True, self.color)
        TextRect = TextSurf.get_rect()

        # accounting for transparency
        if self.trans != 255:
            # rendering the surface onto another surface and adjusting the alpha
            surf = pygame.Surface(TextRect.size)
            surf.fill(self.transColor)
            surf.set_colorkey(self.transColor)
            surf.set_alpha(self.trans)
            
            # rendering the text onto the new surface
            sprite = surf.blit(TextSurf, (0, 0))
            self.textSurf = surf
            self.sprite = sprite
            return sprite
        
        # rendering normal text
        self.textSurf = TextSurf
        self.sprite = TextRect
        return TextRect
    
    # renders the text
    def Render(self, screen: object):
        # rendering the text
        if self.centered:
            screen.blit(self.textSurf, (self.pos[0]- self.sprite.size[0] // 2, self.pos[1] - self.sprite.size[1] // 2))
        else:
            screen.blit(self.textSurf, self.pos)  # not centering it


# a basic text render (doesn't cash anything may be a bit slower)
def DrawText(screen: object, size: int, font: str, text: str, pos: tuple, color: tuple, centered: bool=False, trans: int=255) -> pygame.Rect:
    # creating the font
    Font = pygame.font.Font(font, size)
    
    # creating the text surface
    TextSurf = Font.render(text, True, color)
    TextRect = TextSurf.get_rect()

    # rendering transparent text
    if trans != 255:
        # getting the transparent color
        transColor = (0, 0, 0)
        if color == (0, 0, 0):
            transColor = (255, 255, 255)

        # rendering the surface onto another surface and adjusting the alpha
        surf = pygame.Surface(TextRect.size)
        surf.fill(transColor)
        surf.set_colorkey(transColor)
        surf.set_alpha(trans)

        # rendering the text onto the new surface
        sprite = surf.blit(TextSurf, (0, 0))

        # rendering the surf onto the screen
        if centered:
            screen.blit(surf, (pos[0] - TextRect.size[0] // 2, pos[1] - TextRect.size[1] // 2))
            return sprite
        
        screen.blit(surf, pos)
        return sprite
    
    # rendering the normal text
    if centered:  # centering it
        TextRect.center = pos
        screen.blit(TextSurf, TextRect)
    else:
        screen.blit(TextSurf, pos)  # not centering it
    
    return TextRect


# ===================================================================================================================
#           Basic UI
# ===================================================================================================================


# creates a ui element that can be cashed, render, ect...
class Element:
    def __init__(self, pos: tuple, size: tuple, transparentColor: tuple=(0,0,0)) -> None:
        # initializing values
        self.pos = pos
        self.transparentColor = transparentColor
        self.size = size

        # creating a surface for it
        self.surface = pygame.Surface(size)
        self.surface.fill(self.transparentColor)
        self.surface.set_colorkey(self.transparentColor)

        self.CreateRender(self.surface, (0, 0), Events.Manager())
    
    # clears the display
    def Clear(self) -> None:
        self.surface.fill(self.transparentColor)
    
    # can be overwritten to render the graphics
    def CreateRender(self, disp: object, relativeMousePos: tuple, events: Events.Manager) -> None:
        pass
    
    # updates the box, can be overwritten to do things, returns if the ui element should be re-rendered
    def Update(self, relativeMousePos: tuple, events: Events.Manager) -> bool:
        return True
    
    # controls the rendering, cashing, and updating
    def Render(self, screen: object, events: Events.Manager) -> None:
        # getting the relative mouse pos and checking if the element should update the cash (along with updating the element)
        relativeMousePos = events.GetRelativeMousePos(self.pos)
        shouldUpdate = self.Update(relativeMousePos, events)

        # updating the cashed render
        if shouldUpdate:
            self.Clear()
            self.CreateRender(self.surface, relativeMousePos, events)
        
        # rendering the cashed render
        screen.blit(self.surface, self.pos)


# ===================================================================================================================
#           Prefabs For Buttons, Typing Boxes, Lists, ect...
# ===================================================================================================================


# a simple button class (so I don't have to repeated re-create one for basic use)
class Button (Element):
    # the different states the button can be
    class States (Enum):
        pressed = 0
        held = 1
        realeased = 2
        up = 3
    
    # initializing the information for the button
    def __init__(self, pos: tuple, size: tuple, color: tuple, text: str="", textSize: int=10, font: str="pixel2.ttf", textColor: tuple=(0, 0, 0)) -> None:
        # the state the button is in
        self.state = self.States.up
        self.color = color  # the color of the button
        self.textRenderer = TextRenderer(textSize, font, text, (size[0]//2, size[1]//2-2), textColor, centered=True)

        # initializing the parent classes information
        transparentColor = (255, 255, 255)
        if color == (255, 255, 255):
            transparentColor = (0, 0, 0)
        super().__init__(pos, size, transparentColor=transparentColor)

    # updates the button (and gets if the cashed render should be re-rendered)
    def Update(self, relativeMousePos: tuple, events: Events.Manager) -> bool:
        # if the button needs to be updated
        updated = False

        # updating the state of the button
        dif = 5
        if self.state == self.States.pressed:
            self.state = self.States.held
            self.textRenderer.size += 5
            self.textRenderer.Update()
            updated = True
            dif = 0
        elif self.state == self.States.realeased:
            self.state = self.States.up
            self.textRenderer.size -= 5
            self.textRenderer.Update()
            updated = True
        
        # checking if mouse has clicked
        if events.mouseStates["left"] == Events.MouseStates.pressed:
            # checking if the mouse is overlapping the button
            if relativeMousePos[0] >= dif and relativeMousePos[1] >= dif and relativeMousePos[0] <= self.size[0]-dif and relativeMousePos[1] <= self.size[1]-dif:
                # updating the buttons state
                self.state = self.States.pressed
                updated = True
        
        # setting the button to released if it is held and the mouse is no longer being pressed
        elif events.mouseStates["left"] == Events.MouseStates.realeased and self.state == self.States.held:
            self.state = self.States.realeased

        # returning if the button has been updated
        return updated
    
    # renders the button
    def CreateRender(self, disp: object, relativeMousePos: tuple, events: Events.Manager) -> None:
        # getting the size of the button (adjusted for the different states)
        dif = 5
        color = self.color
        if self.state in [self.States.pressed, self.States.held]:
            color = (self.color[0]//1.15, self.color[1]//1.15, self.color[2]//1.15)
            dif = 0
        
        # rendering the button
        pygame.draw.rect(disp, (color[0]//1.5, color[1]//1.5, color[2]//1.5), [dif, dif, self.size[0] - dif*2, self.size[1] - dif*2], border_radius=6)
        pygame.draw.rect(disp, color, [dif+2, dif+2, self.size[0] - dif*2-4, self.size[1] - dif*2-8], border_radius=6)

        self.textRenderer.Render(disp)

