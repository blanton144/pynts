#!
if __name__ == '__build__':
    raise Exception


import sys
import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import pynts.navigation as navigation
import pynts.utils as utils

#
# pyntsMain.py
#
# Code to handle the user interface into the "pynts" world
#
# Translated from Plotting.c by MRB 2002-12-10
#

#
# TODO
#
#  implement coloring
#  implement selection
#

# Definitions for interface
PYNTS_ROTATE_LEFT = 'h'
PYNTS_ROTATE_RIGHT = 'l'
PYNTS_ROTATE_UP = 'j'
PYNTS_ROTATE_DOWN = 'k'
PYNTS_TRANSLATE_FORWARD = 'a'
PYNTS_TRANSLATE_BACKWARD = 'z'
PYNTS_TRANSLATE_UP = 'i'
PYNTS_TRANSLATE_DOWN = 'u'
PYNTS_TRANSLATE_LEFT = 'y'
PYNTS_TRANSLATE_RIGHT = 'o'
PYNTS_QUIT = 'q'
QUIT = "Quit"
INDX_QUIT = 666

# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = '\033'


# general interface settings
class pyntsProperties:
    newPynts = 1
    moveSize = 0.1
    moveBigSize = 1.
    initSize = [480, 480]
    initPosition = [0, 0]
    fov = 20.
    aspect = 1.
    znear = 0.1
    zfar = 60.
    lasttime = 0
    rotationMethod = 1
    centerSphereColor = [0., 1., 0.]
    scale = 1.
    menu = []
    idle = []
    extra = []
    # overwrite with argv
    windowName = "pynts"

    def flagNewPynts(self):
        self.newPynts = 1
        GLUT.glutPostRedisplay()


# redraw the view of the world by the camera
def redrawPynts(*args):
    GL.glClearColor(0., 0., 0., 0.)
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    if(pynts.newPynts):
        recalcPynts()
        pynts.newPynts = 0
    GL.glDepthMask(GL.GL_TRUE)
    GL.glDisable(GL.GL_TEXTURE_2D)
    currentLightPosition = np.zeros(4, dtype=np.float64)
    currentLightPosition[0] = (camera.lightPosition[0] * camera.cvec[0] +
                               camera.lightPosition[1] * camera.uvec[0] +
                               camera.lightPosition[2] * camera.fvec[0])
    currentLightPosition[1] = (camera.lightPosition[0] * camera.cvec[1] +
                               camera.lightPosition[1] * camera.uvec[1] +
                               camera.lightPosition[2] * camera.fvec[1])
    currentLightPosition[2] = (camera.lightPosition[0] * camera.cvec[2] +
                               camera.lightPosition[1] * camera.uvec[2] +
                               camera.lightPosition[2] * camera.fvec[2])
    currentLightPosition[3] = 0.
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, currentLightPosition)
    GL.glDisable(GL.GL_LIGHTING)
    for extraFunction in pynts.extra[:]:
        extraFunction()
    GL.glEnable(GL.GL_LIGHTING)
    GL.glCallList(pynts.pyntsList)
    GL.glDisable(GL.GL_LIGHTING)
    GL.glDisable(GL.GL_LIGHT0)
    GLUT.glutSwapBuffers()


# mechanism to recalculate the view of the space
def recalcPynts():
    GL.glPopMatrix()
    GL.glPushMatrix()
    GLU.gluLookAt(camera.center[0] + camera.pos[0],
                  camera.center[1] + camera.pos[1],
                  camera.center[2] + camera.pos[2],
                  camera.center[0] + camera.pos[0] + camera.fvec[0],
                  camera.center[1] + camera.pos[1] + camera.fvec[1],
                  camera.center[2] + camera.pos[2] + camera.fvec[2],
                  camera.uvec[0], camera.uvec[1], camera.uvec[2])
    return


# interactive properties of the mouse
class mouseProperties:
    xmouse = 0
    ymouse = 0
    xmoving = 0
    ymoving = 0
    xbegin = 0
    ybegin = 0


# what to do on button press
def mousePynts(button, state, x, y):
    if(button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN):
        mouse.ymoving = 1
        mouse.ybegin = x
    if(button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_UP):
        mouse.ymoving = 0
    if(button == GLUT.GLUT_MIDDLE_BUTTON and state == GLUT.GLUT_DOWN):
        mouse.xmoving = 1
        mouse.xbegin = y
    if(button == GLUT.GLUT_MIDDLE_BUTTON and state == GLUT.GLUT_UP):
        mouse.xmoving = 0
    return


# what to do when mouse is moving (with button pressed)
def mouseMotionPynts(*args):
    if(mouse.ymoving > 0):
        yangle = args[0] - mouse.ybegin
        xangle = 0
        mouse.ybegin = args[0]
    if(mouse.xmoving > 0):
        xangle = args[1] - mouse.xbegin
        yangle = 0
        mouse.xbegin = args[1]
    if(mouse.xmoving > 0 or mouse.ymoving > 0):
        camera.circleCenter(pynts.rotationMethod, xangle, yangle)
        xangle = 0
        yangle = 0
        pynts.flagNewPynts()
    mouse.xmouse = args[1]
    mouse.ymouse = args[0]
    return


# what to do when mouse is moving (without button pressed)
def mousePassiveMotionPynts(*args):
    mouse.xmouse = args[1]
    mouse.ymouse = args[0]
    return


# what to do on a keypress
def keyPynts(*args):
    scale = pynts.moveSize
    key = args[0].decode()

    # where available, upper case means faster movement
    if hasattr(key, "upper"):
        if key == key.upper():
            scale = pynts.moveBigSize
        key = key.lower()

    # or, if shift is set
    if(GLUT.glutGetModifiers() & GLUT.GLUT_ACTIVE_SHIFT) > 0:
        scale = pynts.moveBigSize

    # translate special keys to vi-keys
    if key == GLUT.GLUT_KEY_LEFT:
        key = PYNTS_ROTATE_LEFT
    if key == GLUT.GLUT_KEY_RIGHT:
        key = PYNTS_ROTATE_RIGHT
    if key == GLUT.GLUT_KEY_UP:
        key = PYNTS_ROTATE_UP
    if key == GLUT.GLUT_KEY_DOWN:
        key = PYNTS_ROTATE_DOWN

    # deal with forward/back movement
    if key == PYNTS_TRANSLATE_FORWARD or key == PYNTS_TRANSLATE_BACKWARD:
        sign = 0.
        if(key == PYNTS_TRANSLATE_FORWARD):
            sign = 1.
        if(key == PYNTS_TRANSLATE_BACKWARD):
            sign = -1.
        delta = scale * sign
        camera.translate(delta * camera.fvec)
        pynts.flagNewPynts()

    # deal with up/down movement
    if key == PYNTS_TRANSLATE_UP or key == PYNTS_TRANSLATE_DOWN:
        sign = 0.
        if(key == PYNTS_TRANSLATE_UP):
            sign = 1.
        if(key == PYNTS_TRANSLATE_DOWN):
            sign = -1.
        delta = scale * sign
        camera.translate(delta * camera.uvec)
        pynts.flagNewPynts()

    # deal with left/right movement
    if key == PYNTS_TRANSLATE_LEFT or key == PYNTS_TRANSLATE_RIGHT:
        sign = 0.
        if(key == PYNTS_TRANSLATE_LEFT):
            sign = -1.
        if(key == PYNTS_TRANSLATE_RIGHT):
            sign = 1.
        delta = scale * sign
        camera.translate(delta * camera.cvec)
        pynts.flagNewPynts()

    # deal with left/right rotation
    if key == PYNTS_ROTATE_LEFT or key == PYNTS_ROTATE_RIGHT:
        sign = 0.
        if(key == PYNTS_ROTATE_LEFT):
            sign = 1.
        if(key == PYNTS_ROTATE_RIGHT):
            sign = -1.
        delta = scale * sign
        camera.rotate(delta, camera.uvec)
        pynts.flagNewPynts()

    # deal with left/right rotation
    if key == PYNTS_ROTATE_UP or key == PYNTS_ROTATE_DOWN:
        sign = 0.
        if(key == PYNTS_ROTATE_UP):
            sign = -1.
        if(key == PYNTS_ROTATE_DOWN):
            sign = 1.
        delta = scale * sign
        camera.rotate(delta, camera.cvec)
        pynts.flagNewPynts()
    if key == '/':
        pynts.flagNewPynts()
    if key == ESCAPE or key == PYNTS_QUIT:
        sys.exit()
    return


# basic menu
def menuPynts(option):
    if(option == INDX_QUIT):
        sys.exit()
    return


# idle function runs when nothing else is happening; user can supply
# any number of these
def idleWrapper():
    for idleFunc in pynts.idle:
        idleFunc(pynts, camera)


# idle function which literally is idle
def idleNull():
    idleIdle = 1
    return


# what to do when we are visible (basically, run the idle function)
def visiblePynts(*args):
    if args[0] == GLUT.GLUT_VISIBLE:
        GLUT.glutIdleFunc(idleWrapper)
    else:
        GLUT.glutIdleFunc(idleNull)
    return


# save the image
def saveImage():
    print("saving image")
    return


# configure the menu
def configureMenu():
    menu = [0] * len(pynts.menu)
    menuName = [""] * len(pynts.menu)
    nMenu = 0
    for menuFunction in pynts.menu[:]:
        menu[nMenu], menuName[nMenu] = menuFunction(pynts)
        nMenu = nMenu + 1
    topMenu = GLUT.glutCreateMenu(menuPynts)
    i = 0
    for menuFunction in pynts.menu[:]:
        GLUT.glutAddSubMenu(menuName[i], menu[i])
        i = i + 1
    GLUT.glutAddMenuEntry(QUIT, INDX_QUIT)
    GLUT.glutAttachMenu(GLUT.GLUT_RIGHT_BUTTON)
    return


# create the properties of the world the data live in
def createWorld():
    GLUT.glutDisplayFunc(redrawPynts)
    GLUT.glutMouseFunc(mousePynts)
    GLUT.glutMotionFunc(mouseMotionPynts)
    GLUT.glutPassiveMotionFunc(mousePassiveMotionPynts)
    GLUT.glutVisibilityFunc(visiblePynts)
    GLUT.glutKeyboardFunc(keyPynts)
    GLUT.glutSpecialFunc(keyPynts)
    configureMenu()
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glDisable(GL.GL_POINT_SMOOTH)
    GL.glDisable(GL.GL_PROGRAM_POINT_SIZE)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GL.glLoadIdentity()
    GLU.gluPerspective(pynts.fov, pynts.aspect, pynts.znear, pynts.zfar)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glPushMatrix()


# create our window on that world
def createWindow(argv):

    GLUT.glutInit(argv)
    GLUT.glutInitDisplayMode(GLUT.GLUT_RGBA | GLUT.GLUT_DOUBLE |
                             GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE)
    GLUT.glutInitWindowSize(pynts.initSize[0], pynts.initSize[1])
    GLUT.glutInitWindowPosition(pynts.initPosition[0], pynts.initPosition[1])
    window = GLUT.glutCreateWindow(pynts.windowName)
    return window


# navigate that world
def navigateList(createListFunction, argv, idle=[], extra=[], menu=[]):
    global window, camera, mouse, pynts

    pynts = pyntsProperties()
    pynts.idle = idle
    pynts.extra = extra
    pynts.menu = menu

    # Some menus are not optional
    if(utils.spinningMenu not in pynts.menu):
        pynts.menu.append(utils.spinningMenu)
    if(utils.movementMenu not in pynts.menu):
        pynts.menu.append(utils.movementMenu)

    # overwrite defaults with argv
    #for arg in argv[1:]:
    #    exec "pynts."+arg

    # Create the window
    window = createWindow(sys.argv)

    # now implement the list
    pynts.pyntsList = createListFunction()

    # Create the "points" world interactions
    createWorld()

    # Create mechanisms to handle navigation
    camera = navigation.cameraProperties()
    mouse = mouseProperties()

    # Start event processing engine
    GLUT.glutMainLoop()
