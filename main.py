from bluedot import BlueDot
from signal import pause

bd = BlueDot()

def move(pos):
    if pos.top:
        print(pos.distance)
    elif pos.bottom:
        print(pos.distance)
    elif pos.left:
        print(pos.distance)
    elif pos.right:
        print(pos.distance)

def stop():
    print('stop')

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()