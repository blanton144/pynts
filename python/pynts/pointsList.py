#!
if __name__ == '__build__':
    raise Exception

import OpenGL.GL as GL

#
# pointsList.py
#
# pointsList() takes a list of points and creates a display list
#
# MRB 2002-12-15 (translated from SetPlotPoints.c)
#


def pointsList(positions, pointSize=1):
    numPoints = len(positions)
    GL.glEnableClientState(GL.GL_VERTEX_ARRAY)
    GL.glVertexPointerf(positions)
    pointsListNum = GL.glGenLists(1)
    GL.glNewList(pointsListNum, GL.GL_COMPILE)
    GL.glEnable(GL.GL_BLEND)
    GL.glBlendFunc(GL.GL_SRC_ALPHA, GL.GL_ONE_MINUS_SRC_ALPHA)
    GL.glDisable(GL.GL_PROGRAM_POINT_SIZE)
    GL.glDisable(GL.GL_LIGHTING)
    GL.glPointSize(pointSize)
    GL.glDrawArrays(GL.GL_POINTS, 0, numPoints)
    GL.glEndList()
    return pointsListNum
