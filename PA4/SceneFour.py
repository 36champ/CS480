"""
Define a fixed scene with rotating lights
First version in 11/08/2021

:author: micou(Zezhou Sun)
:version: 2021.1.1
"""
import math

import numpy as np

import os
from PIL import Image

import ColorType
from Animation import Animation
from Component import Component
from Light import Light
from Material import Material
from Point import Point
import GLUtility

from DisplayableCube import DisplayableCube
from DisplayableCylinder import DisplayableCylinder
from DisplayableEllipsoid import DisplayableEllipsoid
from DisplayableTorus import DisplayableTorus
from DisplayableSphere import DisplayableSphere

##### TODO 1: Generate Triangle Meshes
# Requirements:
#   1. Use Element Buffer Object (EBO) to draw the cube. The cube provided in the start code is drawn with Vertex Buffer
#   Object (VBO). In the DisplayableCube class draw method, you should switch from VBO draw to EBO draw. To achieve
#   this, please first read through VBO and EBO classes in GLBuffer. Then you rewrite the self.vertices and self.indices
#   in the DisplayableCube class. Once you have all these down, then switch the line vbo.draw() to ebo.draw().
#   2. Generate Displayable classes for an ellipsoid, torus, and cylinder with end caps.
#   These classes should be like the DisplayableCube class and they should all use EBO in the draw method.
#   PS: You must use the ellipsoid formula to generate it, scaling the Displayable sphere doesn't count
#
#   Displayable object's self.vertices numpy matrix should be defined as this table:
#   Column | 0:3                | 3:6           | 6:9          | 9:11
#   Stores | Vertex coordinates | Vertex normal | Vertex Color | Vertex texture Coordinates
#
#   Their __init__ method should accept following input
#   arguments:
#   DisplayableEllipsoid(radiusInX, radiusInY, radiusInZ, slices, stacks)
#   DisplayableTorus(innerRadius, outerRadius, nsides, rings)
#   DisplayableCylinder(endRadius, height, slices, stacks)
#

##### TODO 5: Create your scenes
# Requirements:
#   1. We provide a fixed scene (SceneOne) for you with preset lights, material, and model parameters.
#   This scene will be used to examine your illumination implementation, and you should not modify it.
#   2. Create 3 new scenes (can be static scenes). Each of your scenes must have
#      * at least 3 differently shaped solid objects
#      * each object should have a different material
#      * at least 2 lights
#      * All types of lights should be used
#   3. Provide a keyboard interface that allows the user to toggle on/off each of the lights in your scene model:
#   Hit 1, 2, 3, 4, etc. to identify which light to toggle.


class SceneFour(Component, Animation):
    shaderProg = None
    glutility = None

    lights = None
    lightCubes = None

    angle = 0

    def __init__(self, shaderProg):
        super().__init__(Point((0, 0, 0)))
        self.shaderProg = shaderProg
        self.glutility = GLUtility.GLUtility()

        sphere = Component(Point((0, 0, 0)), DisplayableSphere(shaderProg, 0.5, 36, 36, ColorType.WHITE))
        m1 = Material(
            np.array([0.1, 0.1, 0.1, 1]),
            np.array([0.4, 0.4, 0.4, 1]),
            np.array([1, 1, 1, 1]),
            64,
        )
        sphere.setMaterial(m1)
        sphere.setTexture(self.shaderProg, './assets/normalmap.jpg')
        sphere.renderingRouting = "lightingbump"
        sphere.setDefaultAngle(-90, sphere.uAxis)
        self.addChild(sphere)

        torus = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, 0.1, 1, 36, 36, ColorType.RED))
        m1 = Material(
            np.array([0.2, 0.2, 0.2, 1]),
            np.array([0.4, 0.4, 0.4, 1]),
            np.array([0.1, 0.1, 0.1, 1]),
            3,
        )
        torus.setMaterial(m1)
        torus.setTexture(self.shaderProg, './assets/normalmap.jpg')
        torus.renderingRouting = "lightingbump"
        torus.setDefaultAngle(-90, torus.uAxis)
        self.addChild(torus)

        torus2 = Component(Point((0, 0, 0)), DisplayableTorus(shaderProg, 0.1, 1.5, 36, 36, ColorType.BLUE))
        m1 = Material(
            np.array([0.1, 0.1, 0.1, 1]),
            np.array([0.1, 0.1, 0.1, 1]),
            np.array([1, 1, 1, 1]),
            64,
        )
        torus2.setMaterial(m1)
        torus2.setTexture(self.shaderProg, './assets/normalmap.jpg')
        torus2.renderingRouting = "lightingbump"
        torus2.setDefaultAngle(-90, torus.uAxis)
        self.addChild(torus2)


        m1 = Material(
            np.array([0.1, 0.1, 0.1, 1]),
            np.array([0.5, 0.5, 0.5, 1]),
            np.array([0.4, 0.4, 0.4, 1]),
            2,
        )
        num_cubes = 8
        for i in range(num_cubes):
            cube = Component(Point([0.8 * np.cos(2 * i * np.pi / num_cubes), 0.8 * np.sin(2 * i * np.pi / num_cubes), 0]), DisplayableCube(shaderProg, 0.1, 0.1, 0.1, ColorType.WHITE))
            cube.setMaterial(m1)
            if i%2: 
                cube.renderingRouting = "lighting"
            else:
                cube.renderingRouting = "normal"
            sphere.addChild(cube)
        num_cylinders = 12
        for i in range(num_cylinders):
            cylinder = Component(Point([1.2 * np.cos(2 * i * np.pi / num_cylinders), 1.2 * np.sin(2 * i * np.pi / num_cylinders), 0]), DisplayableCylinder(shaderProg, 0.05, 0.2, color = ColorType.WHITE))
            cylinder.setMaterial(m1)
            if i%2: 
                cylinder.renderingRouting = "lighting"
            else:
                cylinder.renderingRouting = "normal"
            sphere.addChild(cylinder)

        l0 = Light(
            Point([0, 2, 0]),
            np.array([*ColorType.SOFTRED, 1])
        )

        l1 = Light(
            Point([0, -2, 0]),
            np.array([*ColorType.SOFTBLUE, 1]),
            spotDirection = np.array([0, 1, 0]),
            spotRadialFactor = np.array([0.1, 0.1, 0.1]),
            spotAngleLimit = 6
        )

        l2 = Light(
            Point([0, 0, 0]),
            np.array([0.5, 0.5, 0.5, 1]),
            infiniteDirection = np.array([0, 0, -1])
        )

        l3 = Light(
            Point([0, 0, 0]),
            np.array([0.5, 0.5, 0.5, 1]),
            infiniteDirection = np.array([0, 0, 1])
        )

        self.lights = [l0, l1, l2, l3]
        self.lightCubes = []
        self.objects = {
            "earth": sphere,
            "ring": torus,
            "ring2": torus2,
        }

    def animationUpdate(self):
        self.angle = (self.angle + 0.5) % 360
        
        self.objects["earth"].setCurrentAngle(self.angle, self.objects["earth"].wAxis)
        self.objects["ring"].setCurrentAngle(2*self.angle % 360, self.objects["ring"].wAxis)
        self.objects["ring"].setCurrentAngle(self.angle, self.objects["ring"].vAxis)
        self.objects["ring2"].setCurrentAngle(self.angle, self.objects["ring"].wAxis)
        self.objects["ring2"].setCurrentAngle(self.angle, self.objects["ring"].uAxis)

        self.lights[1].setSpotAngleLimit(abs(self.angle - 180) / 6 + 15)
        self.shaderProg.setLight(1, self.lights[1])

        for c in self.children:
            if isinstance(c, Animation):
                c.animationUpdate()

    def initialize(self):
        self.shaderProg.clearAllLights()
        for i, v in enumerate(self.lights):
            self.shaderProg.setLight(i, v)
        super().initialize()
