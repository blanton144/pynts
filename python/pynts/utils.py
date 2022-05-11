#!
if __name__ == '__build__':
    raise Exception

import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import pynts.navigation
import pynts.pyntsMain as pm
import sys

#
# pyntsUtils.py
#
# Utility codes for pynts (menus, idle functions, etc)
#
# Written by MRB 2002-12-10
#

#######################################
# Deal with idle spinning function
#


class spinPynts:
    timeStep = 4096
    xy = 1


# The routine to run on "idle"
def idleSpinning(pynts, camera):
    if(pynts.lasttime > spin.timeStep):
        if spin.xy == 0:
            camera.circleCenter(pynts.rotationMethod, -2., 0.)
        else:
            camera.circleCenter(pynts.rotationMethod, 0., -2.)
        pynts.lasttime = 0
        pynts.flagNewPynts()
    pynts.lasttime = pynts.lasttime+1
    return


# Menu settings
POS_I = 0
POS_I = POS_I + 1
START_STOP_SPINNING_POS = POS_I
STOP_SPINNING_INDX = 0
START_SPINNING_INDX = 1
POS_I = POS_I + 1
SLOW_SPINNING_POS = POS_I
SLOW_SPINNING_INDX = 2
POS_I = POS_I + 1
FAST_SPINNING_POS = POS_I
FAST_SPINNING_INDX = 3
POS_I = POS_I + 1
SPIN_ABOUT_POS = POS_I
SPIN_ABOUT_X_INDX = 4
SPIN_ABOUT_Y_INDX = 5


# Create the menu
def spinningMenu(pynts):
    global spin
    spin = spinPynts()
    outmenuname = "Spinning"
    outmenu = GLUT.glutCreateMenu(spinningMenuAction)
    if idleSpinning in pynts.idle:
        startStopSpinning = "Stop spinning"
        startStopSpinningIndx = STOP_SPINNING_INDX
    else:
        startStopSpinning = "Start spinning"
        startStopSpinningIndx = START_SPINNING_INDX
    GLUT.glutAddMenuEntry(startStopSpinning, startStopSpinningIndx)
    GLUT.glutAddMenuEntry("Slow down", SLOW_SPINNING_INDX)
    GLUT.glutAddMenuEntry("Speed up", FAST_SPINNING_INDX)
    GLUT.glutAddMenuEntry("Spin about x-axis", SPIN_ABOUT_X_INDX)
    return outmenu, outmenuname


# Menu controls
def spinningMenuAction(option):
    if option == STOP_SPINNING_INDX:
        pm.pynts.idle.remove(idleSpinning)
        GLUT.glutChangeToMenuEntry(START_STOP_SPINNING_POS,
                                   "Start spinning",
                                   START_SPINNING_INDX)
        return
    if option == START_SPINNING_INDX:
        pm.pynts.idle.append(idleSpinning)
        GLUT.glutChangeToMenuEntry(START_STOP_SPINNING_POS, "Stop spinning",
                                   STOP_SPINNING_INDX)
        return
    if option == SLOW_SPINNING_INDX:
        spin.timeStep = spin.timeStep * 2
        return
    if option == FAST_SPINNING_INDX:
        spin.timeStep = spin.timeStep / 2
        if(spin.timeStep <= 1):
            spin.timeStep = 1
            print("Reached maximum spinning speed.")
        return
    if option == SPIN_ABOUT_X_INDX:
        GLUT.glutChangeToMenuEntry(SPIN_ABOUT_POS, "Spin about y-axis",
                                   SPIN_ABOUT_Y_INDX)
        spin.xy = 0
        return
    if option == SPIN_ABOUT_Y_INDX:
        GLUT.glutChangeToMenuEntry(SPIN_ABOUT_POS,
                                   "Spin about x-axis",
                                   SPIN_ABOUT_X_INDX)
        spin.xy = 1
        return
    return

###############################
# Deal with movement functions
#


# Center sphere
def showCenterSphere():
    GL.glPushMatrix()
    GL.glTranslatef(pm.camera.center[0],
                    pm.camera.center[1],
                    pm.camera.center[2])
    GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, 50.)
    GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT,
                    pm.pynts.centerSphereColor)
    GL.glutSolidSphere(pm.pynts.scale * 0.02, 30, 30)
    GL.glMaterialf(GL.GL_FRONT_AND_BACK, GL.GL_SHININESS, 0.)
    GL.glPopMatrix()


# Menu settings
POS_I = 0
POS_I = POS_I+1
MOVE_SLOWER_POS = POS_I
MOVE_SLOWER_INDX = 0
POS_I = POS_I+1
MOVE_FASTER_POS = POS_I
MOVE_FASTER_INDX = 1
POS_I = POS_I+1
BODY_CAMERA_POS = POS_I
BODY_AXES_INDX = 2
CAMERA_AXES_INDX = 3
POS_I = POS_I + 1
SHOW_HIDE_CENTER_POS = POS_I
SHOW_CENTER_INDX = 8
HIDE_CENTER_INDX = 9
POS_I = POS_I + 1
CENTER_TO_ZERO_POS = POS_I
CENTER_TO_ZERO_INDX = 4
POS_I = POS_I + 1
CENTER_TO_FRONT_POS = POS_I
CENTER_TO_FRONT_INDX = 5
POS_I = POS_I + 1
PICK_UP_DROP_CENTER_POS = POS_I
PICK_UP_CENTER_INDX = 6
DROP_CENTER_INDX = 7


# Create the menu
def movementMenu(pynts):
    global spin
    spin = spinPynts()
    outmenuname = "Movement"
    outmenu = GLUT.glutCreateMenu(movementMenuAction)
    GLUT.glutAddMenuEntry("Move slower", MOVE_SLOWER_INDX)
    GLUT.glutAddMenuEntry("Move faster", MOVE_FASTER_INDX)
    GLUT.glutAddMenuEntry("Rotate on body axes", BODY_AXES_INDX)
    GLUT. GLUT.glutAddMenuEntry("Show center", SHOW_CENTER_INDX)
    GLUT.glutAddMenuEntry("Center to zero", CENTER_TO_ZERO_INDX)
    GLUT.glutAddMenuEntry("Center to front", CENTER_TO_FRONT_INDX)
    GLUT.glutAddMenuEntry("Pick up center", PICK_UP_CENTER_INDX)
    return outmenu, outmenuname


# Menu controls
def movementMenuAction(option):
    if option == MOVE_SLOWER_INDX:
        pm.pynts.moveSize = pm.pynts.moveSize/2.
        pm.pynts.moveBigSize = pm.pynts.moveBigSize/2.
        return
    if option == MOVE_FASTER_INDX:
        pm.pynts.moveSize = pm.pynts.moveSize*2.
        pm.pynts.moveBigSize = pm.pynts.moveBigSize*2.
        return
    if option == CAMERA_AXES_INDX:
        GLUT.glutChangeToMenuEntry(BODY_CAMERA_POS,
                                   "Rotate on body axes",
                                   BODY_AXES_INDX)
        pm.pynts.rotationMethod = 1
        return
    if option == BODY_AXES_INDX:
        GLUT.glutChangeToMenuEntry(BODY_CAMERA_POS,
                                   "Rotate on camera axes",
                                   CAMERA_AXES_INDX)
        pm.pynts.rotationMethod = 0
        return
    if option == SHOW_CENTER_INDX:
        pm.pynts.extra.append(showCenterSphere)
        GLUT.glutChangeToMenuEntry(SHOW_HIDE_CENTER_POS,
                                   "Hide center",
                                   HIDE_CENTER_INDX)
        return
    if option == HIDE_CENTER_INDX:
        pm.pynts.extra.remove(showCenterSphere)
        GLUT.glutChangeToMenuEntry(SHOW_HIDE_CENTER_POS,
                                   "Show center",
                                   SHOW_CENTER_INDX)
        return
    if option == CENTER_TO_ZERO_INDX:
        pm.camera.pos = pm.camera.pos + pm.camera.center
        pm.camera.center = np.zeros(3)
        pm.camera.carryRecenter=0
        GLUT.glutChangeToMenuEntry(PICK_UP_DROP_CENTER_POS,
                                   "Pick up center",
                                   PICK_UP_CENTER_INDX);
        return
    if option == CENTER_TO_FRONT_INDX:
        full = pm.camera.center + pm.camera.pos
        pm.camera.center = (full + 0.5 * pm.pynts.scale *
                                   pm.camera.fvec)
        pm.camera.pos = full - pm.camera.center
        pm.camera.carryRecenter = 1
        if (showCenterSphere not in pm.pynts.extra):
            pm.pynts.extra.append(showCenterSphere)
            GLUT.glutChangeToMenuEntry(PICK_UP_DROP_CENTER_POS,
                                       "Drop center",
                                       DROP_CENTER_INDX)
            GLUT.glutChangeToMenuEntry(SHOW_HIDE_CENTER_POS,
                                       "Hide center",
                                       HIDE_CENTER_INDX)
        return
    if option == PICK_UP_CENTER_INDX:
        pm.camera.carryRecenter = 1
        GLUT.glutChangeToMenuEntry(PICK_UP_DROP_CENTER_POS,
                                   "Drop center",
                                   DROP_CENTER_INDX)
        return
    if option == DROP_CENTER_INDX:
        pm.camera.carryRecenter = 0
        GLUT.glutChangeToMenuEntry(PICK_UP_DROP_CENTER_POS,
                                   "Pick up center",
                                   PICK_UP_CENTER_INDX)
        return
    return
