#!
if __name__ == '__build__':
    raise Exception

import numpy as np
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import sys

#
# navigation.py
#
# Code to handle navigating the space in pynts (the python version of points).
# This code does NOT deal with the interface to the user, which is handled
# in pyntsMain.py, but only defines the operations usable by that interface
#
# Translated from Navigation.c by MRB 2002-12-10
#


# class which contain the properties of the camera with which we look
# at the world; there will be a single actual camera
class cameraProperties:
    center = np.array([0., 0., 0.])  # center of the world
    pos = np.array([0., 0., 4.])     # position of the camera wrt. the center
    fvec = np.array([0., 0., -1.])   # direction which camera faces
    uvec = np.array([0., 1., 0.])    # direction "up" on the screen
    cvec = np.array([1., 0., 0.])    # direction to the right on the screen
    carryRecenter = 0           # are we carrying the recent sphere with us?
    lightPosition = np.array([0., 0., -1.])  # direction of our flashlight

    # given uvec and fvec, set cvec
    def setCvec(self):
        newcvec = normVec(crossVec(self.fvec, self.uvec))
        self.cvec = newcvec

    # circle the camera around the center by the given yangle, then xangle
    # (this operation makes it look as if the objects in the space are
    #  spinning around their center)
    def circleCenter(self, method, xangle, yangle):
        self.pos = rotateObject(self, method, self.pos[:], - xangle, - yangle)
        self.fvec = rotateObject(self, method, self.fvec[:], - xangle, - yangle)
        self.uvec = rotateObject(self, method, self.uvec[:], - xangle, - yangle)
        self.setCvec()

    # translate the camera, either carrying the recenter with it or not
    def translate(self, direction):
        if(self.carryRecenter):
            self.center = self.center[:] + direction[:]
        else:
            self.pos = self.pos[:] + direction[:]

    # rotate the camera around some axis
    def rotate(self, angle, axis):
        self.fvec = rotateVector(self.fvec, angle, axis)
        self.uvec = rotateVector(self.uvec, angle, axis)
        self.setCvec()
        if(self.carryRecenter):
            full = self.center + self.pos
            self.pos = rotateVector(self.pos, angle, axis)
            self.center = full - self.pos


# normalize a vector
def normVec(vec):
    norm = np.sqrt(np.inner(vec, vec))
    outvec = vec / norm
    return outvec


# cross product between vectors
def crossVec(vec1, vec2):
    outvec = np.zeros(3, dtype=np.float64)
    outvec[0] = vec1[1] * vec2[2] - vec1[2] * vec2[1]
    outvec[1] = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    outvec[2] = vec1[0] * vec2[1] - vec1[1] * vec2[0]
    return outvec


# rotate a vector some angle (in degrees) around some axis
def rotateVector(vec, angle, axis):
    deg2rad = np.pi / 180.
    outvec = np.array([0., 0., 0.])

    # normalize input axis
    anorm = np.sqrt(np.inner(axis, axis))
    adir = normVec(axis)

    # find direction perp to axis, in plane of vec and axis
    vdota = np.inner(vec, adir)
    vmag2 = np.inner(vec, vec)
    vperp2 = vmag2 - vdota**2
    if (vperp2 < 1.e-6):
        outvec = vec
        return outvec
    vperp = np.sqrt(vperp2)
    vdir = normVec(vec - vdota * adir)

    # find other direction
    cdir = crossVec(adir, vdir)

    # rotate around adir
    sinangle = np.sin(angle * deg2rad)
    cosangle = np.cos(angle * deg2rad)
    vdir = sinangle * cdir + cosangle * vdir

    # adjust vec
    outvec = anorm * (adir * vdota + vdir * vperp)
    return outvec


# rotate a vector around the camera or body axes by
# xangle or yangle
def rotateObject(currCamera, method, vec, xangle, yangle):
    xdir = np.array([1., 0., 0.])
    ydir = np.array([0., 1., 0.])
    if(method == 1):
        xdir = currCamera.cvec
        ydir = currCamera.uvec
    outvec1 = rotateVector(vec, yangle, ydir)
    outvec2 = rotateVector(outvec1, xangle, xdir)
    return outvec2
