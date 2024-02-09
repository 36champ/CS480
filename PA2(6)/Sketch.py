"""
This is the main entry of your program. Almost all things you need to implement are in this file.
The main class Sketch inherits from CanvasBase. For the parts you need to implement, they are all marked with TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.1.1

Modified by Daniel Scrivener 07/2022
"""

import math

import numpy as np
from ModelAxes import ModelAxes
from ModelLinkage import ModelLinkage

import ColorType
from Point import Point
from CanvasBase import CanvasBase
from GLProgram import GLProgram
from Quaternion import Quaternion
import GLUtility

try:
    import wx
    from wx import glcanvas
except ImportError:
    raise ImportError("Required dependency wxPython not present")
try:
    # From pip package "Pillow"
    from PIL import Image
except:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError
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


class Sketch(CanvasBase):
    """
    Drawing methods and interrupt methods will be implemented in this class.
    
    Variable Instruction:
        * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging

        
    Method Instruction:
        
        
    Here are the list of functions you need to override:
        * Interrupt_MouseL: Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
        * Interrupt_MouseLeftDragging: Used to deal with mouse dragging interruption.
        * Interrupt_Keyboard: Used to deal with keyboard press interruption. Use this to add new keys or new methods
        
    Here are some public variables in parent class you might need:
        
        
    """
    context = None

    debug = 1

    last_mouse_leftPosition = None
    last_mouse_middlePosition = None
    components = None

    texture = None
    shaderProg = None
    glutility = None

    lookAtPt = None
    upVector = None
    backgroundColor = None
    # use these three to control camera position, mainly used in mouse dragging
    cameraDis = None
    cameraTheta = None  # theta on horizontal sphere cut, in range [0, 2pi]
    cameraPhi = None  # in range [-pi, pi], for smooth purpose

    viewMat = None
    perspMat = None

    select_obj_index = -1 # index of selected component in self.components
    select_obj_parts = []
    select_axis_index = -1  # index of selected axis
    select_color = [ColorType.SOFTRED, ColorType.SOFTGREEN, ColorType.SOFTBLUE]

    # If you are having trouble rotating the camera, try increasing this parameter
    # (Windows users with trackpads may need this)
    MOUSE_ROTATE_SPEED = 1
    MOUSE_SCROLL_SPEED = 2.5

    def __init__(self, parent):
        super(Sketch, self).__init__(parent)
        # prepare OpenGL context
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        # Initialize Parameters
        self.last_mouse_leftPosition = [0, 0]
        self.last_mouse_middlePosition = [0, 0]
        self.backgroundColor = ColorType.BLUEGREEN

        # add components to top level
        self.resetView()

        self.glutility = GLUtility.GLUtility()

    def resetView(self):
        self.lookAtPt = [0, 0, 0]
        self.upVector = [0, 1, 0]
        self.cameraDis = 6
        self.cameraPhi = math.pi / 6
        self.cameraTheta = math.pi / 2

        
    def InitGL(self):
        """
        Called once in order to initialize the OpenGL environemnt.
        You must set your model here (and not in __init__)
        due to the fact that the shader is only compiled once we reach this function.
        """
        self.shaderProg = GLProgram()
        self.shaderProg.compile()

        ##### TODO 3: Initialize your model
        # You should initialize your model here.
        # self.topLevelComponent should refer to your model
        # and self.components should refer to your model's components.
        # Optionally, you can create a dictionary (self.cDict) to index your model's components by name.

        model = ModelLinkage(self, Point((0, 0, 0)), self.shaderProg)
        axes = ModelAxes(self, Point((-1, -1, -1)), self.shaderProg)

        self.topLevelComponent.clear()
        self.topLevelComponent.addChild(model)
        self.topLevelComponent.addChild(axes)
        self.topLevelComponent.initialize()

        self.components = model.componentList
        self.cDict = model.componentDict

        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClearDepth(1.0)
        gl.glViewport(0, 0, self.size[0], self.size[1])

        # enable depth checking
        gl.glEnable(gl.GL_DEPTH_TEST)

        # set basic viewing matrix
        self.perspMat = self.glutility.perspective(45, self.size.width, self.size.height, 0.01, 100)
        self.shaderProg.setMat4("projectionMat", self.perspMat)
        self.shaderProg.setMat4("viewMat", self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector))
        self.shaderProg.setMat4("modelMat", np.identity(4))

        #Set Key Binding
        self.keybinds = {
            "a": ["body"],
            "b": ["shoulder"],
            "c": ["neck"],
            "d": ["head"],
            "e": ["L_arm_1"],
            "E": ["R_arm_1"],
            "f": ["L_arm_2"],
            "F": ["R_arm_2"],
            "g": ["L_hand"],
            "G": ["R_hand"],
            "h": ["pelvis"],
            "i": ["L_leg_1"],
            "I": ["R_leg_1"],
            "j": ["L_leg_2"],
            "J": ["R_leg_2"],
            "k": ["L_foot"],
            "K": ["R_foot"],
            "l": ["L_wing_1"],
            "L": ["R_wing_1"],
            "m": ["L_wing_2"],
            "M": ["R_wing_2"],
            "n": ["L_wing_3"],
            "N": ["R_wing_3"],
            "u": ["L_wing_upper_accessory_1", "L_wing_lower_accessory_1"], 
            "U": ["R_wing_upper_accessory_1", "R_wing_lower_accessory_1"],
            "v": ["L_wing_upper_accessory_2", "L_wing_lower_accessory_2"], 
            "V": ["R_wing_upper_accessory_2", "R_wing_lower_accessory_2"],
            "w": ["L_wing_upper_accessory_3", "L_wing_lower_accessory_3"], 
            "W": ["R_wing_upper_accessory_3", "R_wing_lower_accessory_3"],
            "x": ["L_wing_upper_accessory_4", "L_wing_lower_accessory_4"], 
            "X": ["R_wing_upper_accessory_4", "R_wing_lower_accessory_4"],
            "y": ["L_wing_upper_accessory_5", "L_wing_lower_accessory_5"], 
            "Y": ["R_wing_upper_accessory_5", "R_wing_lower_accessory_5"],
        }

        self.test_case_index = 0
        #Set Test Case
        self.test_cases = [
            {},
            {
                "L_arm_1": [50, 0, 0],
                "L_arm_2": [0, -125, 50],
                "L_hand": [0, 80, 0],

                "R_arm_1": [12.5, 0, 0],
                "R_arm_2": [0, 0, 75],
                "R_hand": [0, 40, 0],

                "L_leg_1": [10, 0, 0],
                "L_leg_2": [0, 20, 0],
                "L_foot": [0, 5, -15],

                "R_leg_1": [-5, 0, 0],
                "R_leg_2": [0, 0, 0],
                "R_foot": [0, 25, -12.5],

                "L_wing_1": [5, 0, 10],
                "L_wing_2": [0, 0, 0],
                "L_wing_3": [30, 0, 0],

                "R_wing_1": [5, 0, 10],
                "R_wing_2": [0, 0, 0],
                "R_wing_3": [30, 0, 0],

                "L_wing_upper_accessory_1": [0, 0, 5],
                "L_wing_upper_accessory_2": [0, 0, -25],
                "L_wing_upper_accessory_3": [0, 0, -25],
                "L_wing_upper_accessory_4": [0, 0, -25],
                "L_wing_upper_accessory_5": [0, 0, -25],

                "R_wing_upper_accessory_1": [0, 0, 5],
                "R_wing_upper_accessory_2": [0, 0, -25],
                "R_wing_upper_accessory_3": [0, 0, -25],
                "R_wing_upper_accessory_4": [0, 0, -25],
                "R_wing_upper_accessory_5": [0, 0, -25],
            },
            {
                "L_arm_1": [45, 0, 0],
                "L_arm_2": [0, -25, 30],
                "L_hand": [0, 90, 0],

                "R_arm_1": [45, 0, 0],
                "R_arm_2": [0, -25, 30],
                "R_hand": [0, 90, 0],

                "pelvis": [0, 0, 60],

                "L_leg_1": [0, 10, 60],
                "L_leg_2": [0, 15, 0],
                "L_foot": [0, 60, 0],

                "R_leg_1": [0, -5, 60],
                "R_leg_2": [0, 0, 0],
                "R_foot": [0, 60, 0],

                "L_wing_1": [15, 0, 0],
                "L_wing_2": [0, 0, 0],
                "L_wing_3": [80, 0, 0],

                "R_wing_1": [15, 0, 0],
                "R_wing_2": [0, 0, 0],
                "R_wing_3": [80, 0, 0],

                "L_wing_upper_accessory_1": [0, 0, 30],
                "L_wing_upper_accessory_2": [0, 0, -15],
                "L_wing_upper_accessory_3": [0, 0, -15],
                "L_wing_upper_accessory_4": [0, 0, -15],
                "L_wing_upper_accessory_5": [0, 0, -15],

                "R_wing_upper_accessory_1": [0, 0, 30],
                "R_wing_upper_accessory_2": [0, 0, -15],
                "R_wing_upper_accessory_3": [0, 0, -15],
                "R_wing_upper_accessory_4": [0, 0, -15],
                "R_wing_upper_accessory_5": [0, 0, -15],
            },
            {
                "shoulder": [0, 0, -15],

                "L_arm_1": [0, -20, 0],
                "L_arm_2": [-40, -140, 0],
                "L_hand": [0, 80, 0],

                "R_arm_1": [0, 20, 0],
                "R_arm_2": [0, -80, 40],
                "R_hand": [0, 80, 45],

                "pelvis": [0, 0, 20],

                "L_leg_1": [-10, 70, 20],
                "L_leg_2": [0, 30, 0],
                "L_foot": [0, 40, 0],

                "R_leg_1": [0, 80, 0],
                "R_leg_2": [45, 60, 0],
                "R_foot": [0, 20, 0],

                "L_wing_1": [-15, 0, 0],
                "L_wing_2": [30, 90, 0],
                "L_wing_3": [-45, 0, 30],

                "R_wing_1": [-15, 0, 0],
                "R_wing_2": [30, 90, 0],
                "R_wing_3": [-45, 0, 30],

                "L_wing_upper_accessory_1": [0, 0, -20],
                "L_wing_upper_accessory_2": [0, 0, 30],
                "L_wing_upper_accessory_3": [0, 0, 30],
                "L_wing_upper_accessory_4": [0, 0, 30],
                "L_wing_upper_accessory_5": [0, 0, 30],

                "R_wing_upper_accessory_1": [0, 0, -20],
                "R_wing_upper_accessory_2": [0, 0, 30],
                "R_wing_upper_accessory_3": [0, 0, 30],
                "R_wing_upper_accessory_4": [0, 0, 30],
                "R_wing_upper_accessory_5": [0, 0, 30],
            },
            {
                "body": [0, 15, 0],

                "L_arm_1": [-15, -25, 0],

                "R_arm_1": [-10, -20, 0],
                "R_arm_2": [-20, -160, 0],
                "R_hand": [0, 20, 40],

                "L_leg_1": [-15, 70, 0],
                "L_leg_2": [20, 150, 0],
                "L_foot": [0, 90, 0],

                "R_leg_1": [-15, 70, 0],
                "R_leg_2": [20, 150, 0],
                "R_foot": [0, 90, 0],

                "L_wing_1": [0, 0, 10],
                "L_wing_3": [75, 0, 0],

                "R_wing_1": [0, 0, 10],
                "R_wing_3": [75, 0, 0],

                "L_wing_upper_accessory_1": [0, 0, 20],
                "L_wing_upper_accessory_2": [0, 0, -20],
                "L_wing_upper_accessory_3": [0, 0, -20],
                "L_wing_upper_accessory_4": [0, 0, -20],
                "L_wing_upper_accessory_5": [0, 0, -20],

                "R_wing_upper_accessory_1": [0, 0, 20],
                "R_wing_upper_accessory_2": [0, 0, -20],
                "R_wing_upper_accessory_3": [0, 0, -20],
                "R_wing_upper_accessory_4": [0, 0, -20],
                "R_wing_upper_accessory_5": [0, 0, -20],
            },
            {
                "body": [0, -10, -20],
                "shoulder": [0, 0, -30],

                "L_arm_1": [30, -160, 0],
                "L_arm_2": [-45, -45, 0],
                "L_hand": [0, 60, 0],

                "R_arm_1": [30, -160, 0],
                "R_arm_2": [-45, -45, 0],
                "R_hand": [0, 60, 0],

                "pelvis": [0, 0, 20],

                "L_leg_1": [10, -10, 0],
                "L_leg_2": [15, 20, 0],
                "L_foot": [0, 20, 10],

                "R_leg_1": [-15, 15, 0],
                "R_leg_2": [15, 75, 0],
                "R_foot": [0, 20, -10],

                "L_wing_1": [0, 0, 10],
                "L_wing_3": [30, 0, 0],

                "R_wing_1": [0, 0, 10],
                "R_wing_3": [30, 0, 0],

                "L_wing_upper_accessory_1": [0, 0, 20],

                "R_wing_upper_accessory_1": [0, 0, 20],
            },
        ]

    def getCameraPos(self):
        ct = math.cos(self.cameraTheta)
        st = math.sin(self.cameraTheta)
        cp = math.cos(self.cameraPhi)
        sp = math.sin(self.cameraPhi)
        result = [self.lookAtPt[0] + self.cameraDis * ct * cp,
                  self.lookAtPt[1] + self.cameraDis * sp,
                  self.lookAtPt[2] + self.cameraDis * st * cp]
        return result

    def OnResize(self, event):
        contextAttrib = glcanvas.GLContextAttrs()
        contextAttrib.PlatformDefaults().CoreProfile().MajorVersion(3).MinorVersion(3).EndList()
        self.context = glcanvas.GLContext(self, ctxAttrs=contextAttrib)
        self.size = self.GetClientSize()
        self.size[1] = max(1, self.size[1])  # avoid divided by 0
        self.SetCurrent(self.context)

        self.init = False
        self.Refresh(eraseBackground=True)
        self.Update()

    def OnPaint(self, event=None):
        """
        This will be called at every frame
        """
        self.SetCurrent(self.context)
        if not self.init:
            # Init the OpenGL environment if not initialized
            self.InitGL()
            self.init = True
        # the draw method
        self.OnDraw()

    def OnDraw(self):
        gl.glClearColor(*self.backgroundColor, 1.0)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT | gl.GL_DEPTH_BUFFER_BIT)

        # These are per-frame updates to the shader. Update the viewing matrix
        self.viewMat = self.glutility.view(self.getCameraPos(), self.lookAtPt, self.upVector)
        self.shaderProg.setMat4("viewMat", self.viewMat)

        self.topLevelComponent.update(np.identity(4))
        self.topLevelComponent.draw(self.shaderProg)

        self.SwapBuffers()

    def OnDestroy(self, event):
        """
        Window destroy event binding

        :param event: Window destroy event
        :return: None
        """
        if self.shaderProg is not None:
            del self.shaderProg
        super(Sketch, self).OnDestroy(event)

    def Interrupt_MouseMoving(self, x, y):
        ##### TODO 6 (CS680 Required, CS480 Extra Credit): Eye movement
        # Make your creature's eyes follow the cursor.
        # The eye rotation only needs to work correctly when the creature is looking toward the viewer.
        # You do not need to account for other camera orientations.
        # Try to implement this using quaternions for additional credit!
        size_x, size_y = self.size[0], self.size[1]

        default_eye_direction = Point((1, 0, 0))
        current_mouse_direction = Point((size_x + size_y, size_x-2*x, size_y-2*y)).normalize()
        rotation_axis = default_eye_direction.cross3d(current_mouse_direction).normalize()

        # print(x, y, self.cameraDis)

        sin_eye = default_eye_direction.cross3d(current_mouse_direction).norm()
        cos_eye = default_eye_direction.dot(current_mouse_direction)
        sin_half_eye = ((1-cos_eye)/2)**(1/2)
        
        if sin_half_eye != 0:
            cos_half_eye = sin_eye/2/sin_half_eye
        elif default_eye_direction == current_mouse_direction:
            cos_half_eye = 1
        else:
            cos_half_eye = -1
    
        eye_Quaternion = Quaternion(cos_half_eye, *([sin_half_eye*val for val in rotation_axis]))

        self.cDict["L_eye_1"].setQuaternion(eye_Quaternion)
        self.cDict["R_eye_1"].setQuaternion(eye_Quaternion)

    def Interrupt_Scroll(self, wheelRotation):
        """
        When mouse wheel rotating detected, do following things

        :param wheelRotation: mouse wheel changes, normally +120 or -120
        :return: None
        """
        if wheelRotation == 0:
            return
        wheelChange = wheelRotation / abs(wheelRotation)  # normalize wheel change

        #Single Select Mode
        if len(self.components) > 0 and self.select_obj_index >= 0:
            self.components[self.select_obj_index].rotate(wheelChange * self.MOUSE_SCROLL_SPEED,
                                                            self.components[self.select_obj_index].
                                                            axisBucket[self.select_axis_index])
            
        #Multi Select Mode
        if len(self.components) > 0 and len(self.select_obj_parts) > 0:
            for part in self.select_obj_parts:
                self.cDict[part].rotate(wheelChange * self.MOUSE_SCROLL_SPEED,
                                                            self.cDict[part].
                                                            axisBucket[self.select_axis_index])
        self.update()

    def unprojectCanvas(self, x, y, u=0.5):
        """
        unproject a canvas point to world coordiantes. 2D -> 3D
        you need give an extra parameter u, to tell the method how far are you from znear
        u is the proportion of distance to znear / zfar-znear
        in the gluUnProject, the distribution of z is not linear when using perspective projection,
        so z=0.5 is not in the middle,
        that's why we compute out the ray and use linear interpolation and u to get the point

        :param u: u is the proportion to the znear/, in range [0, 1]
        :type u: float
        """
        result1 = glu.gluUnProject(x, y, 0.0,
                                   np.identity(4),
                                   self.viewMat @ self.perspMat,
                                   gl.glGetIntegerv(gl.GL_VIEWPORT))
        result2 = glu.gluUnProject(x, y, 1.0,
                                   np.identity(4),
                                   self.viewMat @ self.perspMat,
                                   # be careful, the concate of view and persp is called projection matrix in opengl
                                   gl.glGetIntegerv(gl.GL_VIEWPORT))
        result = Point([(1 - u) * r1 + u * r2 for r1, r2 in zip(result1, result2)])
        return result

    def Interrupt_MouseL(self, x, y):
        """
        When mouse click detected, store current position in last_mouse_leftPosition

        :param x: Mouse click's x coordinate
        :type x: int
        :param y: Mouse click's y coordinate
        :type y: int
        :return: None
        """
        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def Interrupt_MouseMiddleDragging(self, x, y):
        """
        When mouse drag motion with middle key detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_middlePosition[0] = x
            self.last_mouse_middlePosition[1] = y
            return
        
        dx = x - self.last_mouse_middlePosition[0]
        dy = y - self.last_mouse_middlePosition[1]

        originalMidPt = self.unprojectCanvas(*self.last_mouse_middlePosition, 0.5)

        self.last_mouse_middlePosition[0] = x
        self.last_mouse_middlePosition[1] = y

        currentMidPt = self.unprojectCanvas(x, y, 0.5)
        changes = currentMidPt - originalMidPt
        moveSpeed = 0.185 * self.cameraDis / 6
        self.lookAtPt = [self.lookAtPt[0] - changes[0] * moveSpeed,
                         self.lookAtPt[1] - changes[1] * moveSpeed,
                         self.lookAtPt[2] - changes[2] * moveSpeed]

    def Interrupt_MouseLeftDragging(self, x, y):
        """
        When mouse drag motion detected, interrupt with new mouse position

        :param x: Mouse drag new position's x coordinate
        :type x: int
        :param y: Mouse drag new position's x coordinate
        :type y: int
        :return: None
        """

        if self.new_dragging_event:
            self.last_mouse_leftPosition[0] = x
            self.last_mouse_leftPosition[1] = y
            return

        # Change viewing angle when dragging happened
        dx = x - self.last_mouse_leftPosition[0]
        dy = y - self.last_mouse_leftPosition[1]

        # restrict phi movement range, stop cameraphi changes at pole points
        self.cameraPhi = min(math.pi / 2, max(-math.pi / 2, self.cameraPhi - dy / 50))
        self.cameraTheta += dx / 100 * (self.MOUSE_ROTATE_SPEED)

        self.cameraTheta = self.cameraTheta % (2 * math.pi)

        self.last_mouse_leftPosition[0] = x
        self.last_mouse_leftPosition[1] = y

    def update(self):
        """
        Update current canvas
        :return: None
        """
        self.topLevelComponent.update(np.identity(4))

    def Interrupt_Keyboard(self, keycode):
        """
        Keyboard interrupt bindings

        :param keycode: wxpython keyboard event's keycode
        :return: None
        """

        ##### TODO 5: Set up your poses and finish the user interface
        # Define keyboard events to make your creature act in different ways when keys are pressed.
        # Create five unique poses to demonstrate your creature's joint rotations.
        # HINT: selecting individual components is easier if you create a dictionary of components (self.cDict)
        # that can be indexed by name (e.g. self.cDict["leg1"] instead of self.components[10])
            
        if keycode in [wx.WXK_RETURN]:
            # enter component editing mode
            for part in self.select_obj_parts:
                self.cDict[part].reset("color")
                self.select_obj_parts.remove(part)

            self.select_obj_parts = []
            self.select_axis_index = 0

            if len(self.components) > 0:
                # reset color of last selected component
                self.components[self.select_obj_index].reset("color")
                # set new selected component & its color
                self.select_obj_index = (self.select_obj_index + 1) % len(self.components)
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])
                
            self.update()

        if keycode in [wx.WXK_LEFT]:
            # Last rotation axis of this component
            self.select_axis_index = (self.select_axis_index - 1) % 3

            #Single Select Mode
            if self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])

            #Multi Select Mode
            if len(self.select_obj_parts) > 0:
                for part in self.select_obj_parts:
                    self.cDict[part].setCurrentColor(self.select_color[self.select_axis_index])

            self.update()
        
        if keycode in [wx.WXK_RIGHT]:
            # Next rotation axis of this component
            self.select_axis_index = (self.select_axis_index + 1) % 3

            #Single Select Mode
            if self.select_obj_index >= 0:
                self.components[self.select_obj_index].setCurrentColor(self.select_color[self.select_axis_index])

            #Multi Select Mode
            if len(self.select_obj_parts) > 0:
                for part in self.select_obj_parts:
                    self.cDict[part].setCurrentColor(self.select_color[self.select_axis_index])

            self.update()

        if keycode in [wx.WXK_UP]:
            # Increase rotation angle
            self.Interrupt_Scroll(1)
            self.update()

        if keycode in [wx.WXK_DOWN]:
            # Decrease rotation angle
            self.Interrupt_Scroll(-1)
            self.update()

        if keycode in [wx.WXK_ESCAPE]:
            # exit component editing mode
            self.components[self.select_obj_index].reset("color")
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()

        if chr(keycode) in "r":
            # reset viewing angle only
            self.resetView()

        if chr(keycode) in "R":
            # reset everything but Axis
            for c in self.components:
                c.reset("angle")
                c.reset("position")
                c.reset("scale")
                c.reset("color")
            self.resetView()
            self.select_obj_index = -1
            self.select_axis_index = -1
            self.update()

        if chr(keycode) in self.keybinds.keys():
            if self.select_obj_index != -1:
                self.components[self.select_obj_index].reset("color")
                self.select_obj_index = -1
                
            if self.select_axis_index == -1:
                self.select_axis_index = 0

            for part in self.keybinds[chr(keycode)]:
                if part in self.select_obj_parts:
                    self.cDict[part].reset("color")
                    self.select_obj_parts.remove(part)
                else:
                    self.select_obj_parts.append(part)
                    self.cDict[part].setCurrentColor(self.select_color[self.select_axis_index])

        if chr(keycode) in ["t", "T"]:
            for c in self.components:
                c.reset("angle")
                c.reset("position")
                c.reset("scale")
                c.reset("color")

            self.test_case_index = (self.test_case_index + 1) % len(self.test_cases)

            for part, angle in self.test_cases[self.test_case_index].items():
                self.cDict[part].rotate(angle[0], self.cDict[part].uAxis)
                self.cDict[part].rotate(angle[1], self.cDict[part].vAxis)
                self.cDict[part].rotate(angle[2], self.cDict[part].wAxis)


if __name__ == "__main__":
    print("This is the main entry! ")
    app = wx.App(False)
    # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame, here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
    # Resize disabled in this one
    frame = wx.Frame(None, size=(500, 500), title="Test",
                     style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)  # Disable Resize: ^ wx.RESIZE_BORDER
    canvas = Sketch(frame)

    frame.Show()
    app.MainLoop()
