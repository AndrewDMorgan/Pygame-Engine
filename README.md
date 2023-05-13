# Pygame-Engine
A basic engine built on top of pygame to reduce repetitive code (eg. an event manager).
I'm hoping to add things like tile maps and spritesheet readers. I'm not sure how far this probject will go. I would also like to add other helpful features like a particle system or entity system or something. Maybe even create an animation manager for more complicated animations.

## Current Features:
* An event manager
* Text rendering
* A base UI element class
* A basic button

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
        - textColor (default is black)
    - Public Variables
        - state (the state of the button in terms of the States enum within the class)
