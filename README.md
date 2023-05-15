# Pygame-Engine
A basic engine built on top of pygame to reduce repetitive code (eg. an event manager).
I'm hoping to add additional things I need for gamedevelopment. I'm not sure how far this probject will go. I would like to add other helpful features like a particle system or entity system or something. I migth even create an animation manager for more complicated animations. But I'm not sure how much I will actually create.

## Current Features:
* An event manager
* Text rendering
* A base UI element class
* A basic button
* A typing box
* A slider
* A spritesheet loader
* A color palette tool
* A basic tilemap

## Details
It will only work if the files for Pygen are under a folder called Pygen which is placed in the same directory as your program

## Events.py
- MouseStates (Enum)
    - pressed
    - held
    - released
    - up
- Manager
    - Public Variables
        - events (a list of the gathered special events)
        - typed (a list of typed chars like abcd...)
        - mousePos (the position of the mouse)
        - mouseStates (a dictionary with keys for "left" and "right" storing a MouseStates in each)
    - GetEvents
        - Gathers events (updating the variables above)

## UI.py
- TextRenderer
    - Public Variables
        - size
        - font
        - text
        - pos
        - color
        - centered (default is not centered / false)
        - trans (default is solid)
    - Update
        - updates the cashed render (use if you changed the text, color, ect... of the object)
        - returns the rect of the text
    - Render
        - Takes in a surface
        - Renders the cashed text render (uses cashing to improve preformance in larger scale aplications)
- DrawText
    - takes in screen (pygame.surface)
    - size (for the font)
    - font ("example.ttf")
    - text
    - pos
    - color
    - centered (default is false)
    - trans (deafult is solid)
    - returns the rect of the text
- Element
    - Public Variables
        - pos
        - forceUpdate (a boolean that forces the element to update the cash when true)
    - CreateRender
        - overwrite this to render your UI element
    - Update
        - overwrite this to udpate your UI element
        - updates the UI element (called right before rendering)
        - returns if the UI element should re-render the cashed render
    - Render
        - renders and updates the UI element
        - takes in a screen (pygame.surface), and an Events.Manager object
- Button extends Element (A prefab button, inherits the Element class, and is a good example of how to use the Element class)
    - States (Enum)
        - pressed
        - held
        - released
        - up
    - In the constructor, it takes:
        - pos
        - size
        - color
        - text (default is no text)
        - textSize (default is 10)
        - font (default is "pixel2.ttf")
    - Public Variables
        - state (the state of the button in terms of the States enum within the class)
- TypingBox extends Element (A prefab typing box)
    - Public Variables
        - text (the current text thats written in the box)
        - selected (if the box is selected or not)
    - Constructor Args
        - pos
        - size
        - color
        - cursorOffset (default is -2)
        - baseText (default is "Type Here")
        - textSize (default is 10)
        - font (default is "pixel2.ttf")
        - transparentColor (default is (255, 255, 255))
- Slider extends Element (A prefab slider)
    - Public Variables
        - slide (the position of the slider, goes from 0 to 1)
    - Constructor Args
        - pos
        - size
        - color
        - slide (default is 0.5 aka halfway)
        - backgroundText (default is none)
        - font (default is "pixel2.ttf")
        - transparentColor (default is (255, 255, 255))

## Sprites.py
- LoadSpritesheet
    - takes in:
        - image (a surface, not a file path)
        - tileSize
        - transColor (default is (0, 0, 0))
    - returns a list of surfaces (the tiles in the spritesheet)
- ScaleSprites
    - takes in:
        - sprites (a list of surfaces)
        - scale
    - returns the list of sprites but scaled

## TileMap.py
- blankTile (a variable for a blank tile / an air tile)
- TileMap
    - Public Variables
        - map (a 2D list of the tile numbers)
        - tileSize (the size of the tiles)
        - mapSize (a 2D tuple storing the size of the map)
    - Constructor Args
        - tileMapFile (the file path for the tile map)
        - tiles (the tile surfaces, corresponding to the tile numbers)
        - tileSize (the size of the tiles)
    - GetGridPosition
        - takes in a 2D position in a tuple
        - returns a 2D index for the tileMap in a tuple
    - GetTileNumber
        - gets the tile number at a provided index (2D position)
    - Render
        - Takes in:
            - screen (the display)
            - cameraPos (position of the camera)
            - screenSize (the size of the screen)
        - returns nothing
        - renders tile map to the screen


