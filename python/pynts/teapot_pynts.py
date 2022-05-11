#!/usr/bin/python2
if __name__ == '__build__':
    raise Exception

import sys
import pynts as pm
import OpenGL.GL as GL
import OpenGL.GLUT as GLUT

#
# teapot_pynts.py
#
# Code to test pynts.py with a simple teapot
#
# Written by MRB 2002-12-10
#


def teapotList():
    pyntsList = GL.glGenLists(1)
    GL.glNewList(pyntsList, GL.GL_COMPILE)
    GL.glMaterialfv(GL.GL_FRONT_AND_BACK, GL.GL_AMBIENT, [1., 1., 1.])
    GLUT.glutSolidTeapot(1.0)
    GL.glEndList()
    return pyntsList


def main(*args):
    # Dummy display list to play with
    sys.argv.append("scale=10.")
    pm.navigateList(teapotList, sys.argv)


# run main
main()
