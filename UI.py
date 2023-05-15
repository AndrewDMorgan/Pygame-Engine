from Pygen import Events  # for the event manager
from enum import Enum  # for enums (great for representing states)
import pygame  # for pygame (duh)


# ===================================================================================================================
#           A Basic Color Palette Tool
# ===================================================================================================================


# stores a basic color palette
class ColorPalette:
    # initializing everything
    def __init__(self, darkColor: tuple, color: tuple, brightColor: tuple, textColor: tuple) -> None:
        self.darkColor = darkColor
        self.color = color
        self.brightColor = brightColor
        self.textColor = textColor
    
    # creates a monochromatic color scheme (very very basic though)
    def CreateMono(color: tuple, textColor: tuple=(0, 0, 0)) -> object:
        darkColor = (color[0]//1.5, color[1]//1.5, color[2]//1.5)
        brightColor = (color[0]//0.75, color[1]//0.75, color[2]//0.75)
        return ColorPalette(darkColor, color, brightColor, textColor)


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
#           Basic UI Stuff
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
        self.forceUpdate = False

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
    def __init__(self, pos: tuple, size: tuple, color: ColorPalette, text: str="", textSize: int=10, font: str="pixel2.ttf", transparentColor: tuple=(255, 255, 255)) -> None:
        # the state the button is in
        self.state = self.States.up
        self.color = color  # the color of the button
        self.textRenderer = TextRenderer(textSize, font, text, (size[0]//2, size[1]//2-2), color.textColor, centered=True)
        self.textSize = textSize

        # initializing the parent classes information
        
        if transparentColor != (255, 255, 255) and color.color == (255, 255, 255):
            transparentColor = (0, 0, 0)
        super().__init__(pos, size, transparentColor=transparentColor)

    # updates the button (and gets if the cashed render should be re-rendered)
    def Update(self, relativeMousePos: tuple, events: Events.Manager) -> bool:
        # if the button needs to be updated
        updated = self.forceUpdate
        self.forceUpdate = False

        # updating the state of the button
        dif = 0
        if self.state == self.States.pressed:
            self.state = self.States.held
            updated = True
            dif = 5
        elif self.state == self.States.realeased:
            self.state = self.States.up
            self.textRenderer.size = self.textSize + 3
            updated = True

        # checking if mouse has clicked
        if events.mouseStates["left"] == Events.MouseStates.pressed:
            # checking if the mouse is overlapping the button
            if relativeMousePos[0] >= dif and relativeMousePos[1] >= dif and relativeMousePos[0] <= self.size[0]-dif and relativeMousePos[1] <= self.size[1]-dif:
                # updating the buttons state
                self.state = self.States.pressed
                self.textRenderer.size = self.textSize - 3
                updated = True
        
        # setting the button to released if it is held and the mouse is no longer being pressed
        if events.mouseStates["left"] == Events.MouseStates.realeased and self.state == self.States.held:
            self.state = self.States.realeased

        # returning if the button has been updated
        return updated
    
    # renders the button
    def CreateRender(self, disp: object, relativeMousePos: tuple, events: Events.Manager) -> None:
        # getting the size of the button (adjusted for the different states)
        dif = 0
        color = self.color.color
        darkColor = self.color.darkColor
        if self.state in [self.States.pressed, self.States.held]:
            color = (self.color.color[0]//1.15, self.color.color[1]//1.15, self.color.color[2]//1.15)
            darkColor = (self.color.darkColor[0]//1.15, self.color.darkColor[1]//1.15, self.color.darkColor[2]//1.15)
            dif = 5
        
        # rendering the button
        pygame.draw.rect(disp, darkColor, [dif, dif, self.size[0] - dif*2, self.size[1] - dif*2], border_radius=6)
        pygame.draw.rect(disp, color, [dif+2, dif+2, self.size[0] - dif*2-4, self.size[1] - dif*2-8], border_radius=6)

        self.textRenderer.Update()
        self.textRenderer.Render(disp)


# a typing box
class TypingBox (Element):
    # initializing the information for the typing box
    def __init__(self, pos: tuple, size: tuple, color: ColorPalette, cursorOffset: int=-2, baseText: str="Type Here", textSize: int=10, font: str="pixel2.ttf", transparentColor: tuple=(255, 255, 255)) -> None:
        # information about the typing box
        self.cursorOffset = cursorOffset
        self.textSize = textSize
        self.baseText = baseText
        self.color = color
        self.font = font
        self.charPos = 0
        self.text = ""

        # if the box is selected or not
        self.selected = False

        # the center
        self.center = (size[0]//2, size[1]//2)

        # creating the font
        self.Font = pygame.font.Font(self.font, self.textSize)

        # initializing the parent classes information
        if transparentColor == (255, 255, 255) and color.color == (255, 255, 255):
            transparentColor = (0, 0, 0)
        super().__init__(pos, size, transparentColor=transparentColor)
    
    # updates the typing box
    def Update(self, relativeMousePos: tuple, events: Events.Manager) -> bool:
        # if the cashed render should be updated
        updated = self.forceUpdate
        self.forceUpdate = False

        # checking if enter was pressed
        if pygame.K_RETURN in events.events:
            self.selected = False
            self.charPos = len(self.text)
            updated = True

        # checking if mouse was pressed
        if events.mouseStates["left"] == Events.MouseStates.pressed:
            # checking if the box was clicked and updating its state
            if relativeMousePos[0] >= 0 and relativeMousePos[1] >= 0 and relativeMousePos[0] <= self.size[0] and relativeMousePos[1] <= self.size[1]:
                if not self.selected:
                    self.selected = True
                    updated = True
            elif self.selected:
                self.selected = False
                self.charPos = len(self.text)
                updated = True

        # making sure the button is actually being typed in
        if self.selected:
            # moving the cursor
            if pygame.K_LEFT in events.events:
                self.charPos = max(self.charPos - 1, 0)
                updated = True
            elif pygame.K_RIGHT in events.events:
                self.charPos = min(self.charPos + 1, len(self.text))
                updated = True
            
            # checking if anything was typed
            if events.typed:
                updated = True
                for char in events.typed:
                    self.text = self.text[:self.charPos] + char + self.text[self.charPos:]
                    self.charPos += 1
            
            # checking for deleting characters
            if pygame.K_BACKSPACE in events.events:
                updated = True
                self.text = self.text[:self.charPos][:-1] + self.text[self.charPos:]
                self.charPos = max(self.charPos - 1, 0)
        
        # returning if the box was updated
        return updated
    
    # cashes a render of the typing box whenever it's updated
    def CreateRender(self, disp: object, relativeMousePos: tuple, events: Events.Manager) -> None:
        # rendering the background for the button
        pygame.draw.rect(disp, self.color.darkColor, [0, 0, self.size[0], self.size[1]], border_radius=6)
        pygame.draw.rect(disp, self.color.color, [2, 2, self.size[0] - 4, self.size[1] - 8], border_radius=6)
        
        # rendering the text
        text = self.text[:self.charPos] + " " + self.text[self.charPos:]
        textSprite = DrawText(disp, self.textSize, self.font, text, (self.center[0], self.center[1] - 2), self.color.textColor, True)

        if self.selected:
            # finding the distance to the cursor
            leftText = self.text[:self.charPos]
            textSurfLeft = self.Font.render(leftText, True, self.color.textColor)
            cursorPos = textSurfLeft.get_size()[0]

            # drawing the cursor
            pygame.draw.rect(disp, self.color.textColor, [(self.center[0] + (cursorPos - textSprite.size[0]//2)) + self.textSize//3.5 + self.cursorOffset, self.center[1] - self.textSize//2 - 2, 2, self.textSize])
        elif self.text == "":
            # rendering text saying to type there
            DrawText(disp, self.textSize, self.font, self.baseText, (self.center[0], self.center[1] - 2), self.color.textColor, True)


# a slider
class Slider (Element):
    # initializing the slider
    def __init__(self, pos: tuple, size: tuple, color: ColorPalette, slide: float=0.5, backgroundText: str="", font: str="pixel2.ttf", transparentColor: tuple=(255, 255, 255)) -> None:
        # information about the slider
        self.slide = slide  # 0 to 1
        self.color = color
        self.held = False
        
        # the background text under the slider (could be used to instruct the user on what the setting does)
        self.text = TextRenderer(size[1]//2, font, backgroundText, (size[0]//2, size[1]//2), color.textColor, True)

        # initializing the parent class
        if transparentColor != (255, 255, 255) and color.color == (255, 255, 255):
            transparentColor = (0, 0, 0)
        super().__init__(pos, size, transparentColor=transparentColor)
    
    # updates the slider
    def Update(self, relativeMousePos: tuple, events: Events.Manager) -> bool:
        # if the cashed render should be re-rendeefd
        update = self.forceUpdate
        self.forceUpdate = False

        # checking if the slider has been released
        if self.held and events.mouseStates["left"] == Events.MouseStates.realeased:
            self.held = False
        
        # checking if the slider has been grabbed
        if not self.held and events.mouseStates["left"] == Events.MouseStates.pressed:
            if relativeMousePos[0] >= 0 and relativeMousePos[1] >= 0 and relativeMousePos[0] <= self.size[0] and relativeMousePos[1] <= self.size[1]:
                self.held = True

        # checking if the slider is currently held
        if self.held:
            update = True
            self.slide = max(min(relativeMousePos[0]/self.size[0], 1), 0)

        # renturning if the cash needs re-rendering
        return update
    
    # renders the slider
    def CreateRender(self, disp: object, relativeMousePos: tuple, events: Events.Manager) -> None:
        # drawing the box the slider is in
        pygame.draw.rect(disp, self.color.darkColor, [0, 0, self.size[0], self.size[1]], border_radius=6)  # outside edge
        pygame.draw.rect(disp, self.color.color, [2, 2, self.size[0]-4, self.size[1]-8], border_radius=6)  # rim
        pygame.draw.rect(disp, self.color.darkColor, [4, 4, self.size[0]-8, self.size[1]-12], border_radius=6)  # inside edge
        pygame.draw.rect(disp, self.color.color, [6, 10, self.size[0]-12, self.size[1]-20], border_radius=6)  # inside bottom

        # rendering the background text
        self.text.Render(disp)

        # drawing the slider
        buttonWidth = (self.size[1]-14)//1.25
        sliderOffset = (self.slide*2-1) * (self.size[0]//2 - buttonWidth//2-5)
        pygame.draw.rect(disp, self.color.brightColor, [self.size[0]//2-buttonWidth//2+sliderOffset, 5, buttonWidth, self.size[1]-14], border_radius=6)

