"""
Define displayable cube here. Current version only use VBO
First version in 10/20/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""

from Displayable import Displayable
from GLBuffer import VAO, VBO, EBO
import numpy as np
import ColorType
import math

try:
    import OpenGL

    try:
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
    except ImportError:
        from ctypes import util

        orig_util_find_library = util.find_library


        def new_util_find_library(name):
            res = orig_util_find_library(name)
            if res:
                return res
            return '/System/Library/Frameworks/' + name + '.framework/' + name


        util.find_library = new_util_find_library
        import OpenGL.GL as gl
        import OpenGL.GLU as glu
except ImportError:
    raise ImportError("Required dependency PyOpenGL not present")


class DisplayableCylinder(Displayable):
    vao = None
    vbo = None
    ebo = None
    shaderProg = None

    vertices = None  # array to store vertices information
    indices = None  # stores triangle indices to vertices

    # stores current cube's information, read-only
    length = None
    width = None
    height = None
    color = None

    def __init__(self, shaderProg, endRadius=1, height=1, slices=30, stacks=30, color=ColorType.WHITE):
        super(DisplayableCylinder, self).__init__()
        self.shaderProg = shaderProg
        self.shaderProg.use()

        self.vao = VAO()
        self.vbo = VBO()  # vbo can only be initiate with glProgram activated
        self.ebo = EBO()

        self.generate(endRadius, height, slices, stacks, color)

    def generate(self, endRadius=1, height=1, slices=30, stacks=30, color=None):

        v_data = []
        for z in np.linspace(-height/2, height/2, stacks):
            new_stack = []
            for theta in np.linspace(-np.pi, np.pi, slices + 1)[:slices]:
                new_v = [
                    endRadius * np.cos(theta),
                    endRadius * np.sin(theta),
                    z,
                    np.cos(theta),
                    np.sin(theta),
                    0,
                    *color,
                    0, 
                    0
                ]
                new_stack.append(new_v)
            v_data.append(new_stack)
        # For Lower Cylinder Cap
        new_stack = []
        for theta in np.linspace(-np.pi, np.pi, slices + 1)[:slices]:
            new_v = [
                endRadius * np.cos(theta),
                endRadius * np.sin(theta),
                -height/2,
                0,
                0,
                -1,
                *color,
                0, 
                0
            ]
            new_stack.append(new_v)
        v_data.append(new_stack)
        # For Upper Cylinder Cap
        new_stack = []
        for theta in np.linspace(-np.pi, np.pi, slices + 1)[:slices]:
            new_v = [
                endRadius * np.cos(theta),
                endRadius * np.sin(theta),
                height/2,
                0,
                0,
                1,
                *color,
                0, 
                0
            ]
            new_stack.append(new_v)
        v_data.append(new_stack)
        
        self.vertices = np.array(v_data)

        self.indices = []
        for stack in range(stacks - 1):
            for slice in range(slices):
                next_stack = stack + 1
                next_slice = (slice + 1) % slices

                self.indices.append([stack * slices + slice, stack * slices + next_slice, next_stack * slices + slice])
                self.indices.append([stack * slices + next_slice, next_stack * slices + slice, next_stack * slices + next_slice])
                
        for slice in range(1, slices - 1):
            next_slice = slice + 1
            self.indices.append([stacks * slices + slice, stacks * slices + next_slice, stacks * slices])
            self.indices.append([(stacks + 1) * slices + slice, (stacks + 1) * slices + next_slice, (stacks + 1) * slices ])

        self.indices = np.array(self.indices)

    def draw(self):
        self.vao.bind()
        # TODO 1.1 is at here, switch from vbo to ebo
        self.ebo.draw()
        self.vao.unbind()

    def initialize(self):
        """
        Remember to bind VAO before this initialization. If VAO is not bind, program might throw an error
        in systems that don't enable a default VAO after GLProgram compilation
        """
        self.vao.bind()
        self.vbo.setBuffer(self.vertices, 11)
        self.ebo.setBuffer(self.indices)

        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexPos"),
                                  stride=11, offset=0, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexNormal"),
                                  stride=11, offset=3, attribSize=3)
        self.vbo.setAttribPointer(self.shaderProg.getAttribLocation("vertexColor"),
                                  stride=11, offset=6, attribSize=3)
        # TODO/BONUS 6.1 is at here, you need to set attribPointer for texture coordinates
        # you should check the corresponding variable name in GLProgram and set the pointer
        self.vao.unbind()

