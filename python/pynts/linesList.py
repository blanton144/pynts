#!
if __name__ == '__build__':
    raise Exception
from numpy import *
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from navigation import *
import sys

# This is statement is required by the build system to query build info

#
# lineList.py
#
# lineList() takes a list of points and indices and creates a line object
# UNFINISHED
#

def vertexCallback(vertex):
    v=vertex[0:3]
    n=vertex[3:6]
    glVertex3dv(v)
    glNormal3dv(n)
    return

def beginCallback(which):
    glBegin(which)
    return

def endCallback():
    glEnd()
    return

def errorCallback(ecode):
    estring=gluErrorString(ecode)
    print "Tesselation error"+estring

def combineCallback(coords,vertex_data,weight,dataOut):
    vertex = zeros(6,"double")
    vertex[0:3]=coords[0:3]
    for i in (3+range(4)):
        vertex[i]=weight[0]*vertex_data[0][i] \
                   +weight[1]*vertex_data[1][i] \
                   +weight[2]*vertex_data[2][i]  \
                   +weight[3]*vertex_data[3][i]
    dataOut=vertex;
    print dataOut
    return

def polygonsList(positions,polygons):
    tobj=gluNewTess()
    gluTessCallback(tobj,GLU_TESS_VERTEX,vertexCallback);
    gluTessCallback(tobj,GLU_TESS_BEGIN,beginCallback);
    gluTessCallback(tobj,GLU_TESS_END,endCallback);
#    gluTessCallback(tobj,GLU_TESS_ERROR,errorCallback);
    gluTessCallback(tobj,GLU_TESS_COMBINE,combineCallback);
    polygonsListNum=glGenLists(1)
    glNewList(polygonsListNum, GL_COMPILE);
    color=zeros(4,"double")+1.
    print color
    glEnable(GL_LIGHTING)
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, color)
    for ipoly in range(len(polygons)):
        v1=positions[polygons[ipoly][1]]-positions[polygons[ipoly][0]]
        v2=positions[polygons[ipoly][2]]-positions[polygons[ipoly][0]]
        normal=crossVec(v1,v2)
        normal=normVec(normal)
        full=zeros((len(polygons[ipoly]),6),"double")
        coords=zeros(3,"double")
        gluTessBeginPolygon(tobj,full)
        gluTessBeginContour(tobj)
        for jpos in range(len(polygons[ipoly])):
            full[jpos][0]=positions[polygons[ipoly][jpos]][0];
            full[jpos][1]=positions[polygons[ipoly][jpos]][1];
            full[jpos][2]=positions[polygons[ipoly][jpos]][2];
            full[jpos][3]=normal[0]
            full[jpos][4]=normal[1]
            full[jpos][5]=normal[2]
            coords[0]=full[jpos][0]
            coords[1]=full[jpos][1]
            coords[2]=full[jpos][2]
            gluTessVertex(tobj,coords,full[jpos]);
        gluTessEndContour(tobj);
        gluTessEndPolygon(tobj);
    glDisable(GL_LIGHTING)
    glEndList()
    return polygonsListNum
    

