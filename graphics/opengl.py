#
# This file is part of Zhockon Foundation.
# 
# Copyright (C) 2009-2011 William Oliveira de Lagos <william.lagos1@gmail.com>
#
# Zhockon is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zhockon is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zhockon.  If not, see <http://www.gnu.org/licenses/>.
#

from OpenGL.GL import *
from OpenGL.GLU import *

class Camera:
    def __init__(self):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."
class Depth:
    def __init__(self):
        pass
    def draw_polygon(self,points,colors,verts,edges):
        allpoints = zip(points,colors)
        glBegin(GL_QUADS)
        for face in verts:
            for vert in face:
                pos, color = allpoints[vert]
                glColor3fv(color)
                glVertex3fv(pos)
        glEnd()
        glColor3f(1.0, 1.0, 1.0)
        glBegin(GL_LINES)
        for line in edges:
            for vert in line:
                pos, color = allpoints[vert]
                glVertex3fv(pos)
        glEnd()

class Handler(BaseHandler):
    def __init__(self):
        pass
    def test_opengl(self):
        try:
            raise NotImplementedError
        except NotImplementedError, e:
            print "Option not already implemented."