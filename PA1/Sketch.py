"""
This is the main entry of your program. Almost all things you need to implement is in this file.
The main class Sketch inherit from CanvasBase. For the parts you need to implement, they all marked TODO.
First version Created on 09/28/2018

:author: micou(Zezhou Sun)
:version: 2021.2.1

"""

import os

import wx
import math
import random
import numpy as np

from Buff import Buff
from Point import Point
from ColorType import ColorType
from CanvasBase import CanvasBase

try:
    # From pip package "Pillow"
    from PIL import Image
except Exception:
    print("Need to install PIL package. Pip package name is Pillow")
    raise ImportError


class Sketch(CanvasBase):
    """
    Please don't forget to override interrupt methods, otherwise NotImplementedError will throw out
    
    Class Variable Explanation:

    * debug(int): Define debug level for log printing

        * 0 for stable version, minimum log is printed
        * 1 will print general logs for lines and triangles
        * 2 will print more details and do some type checking, which might be helpful in debugging
    
    * texture(Buff): loaded texture in Buff instance
    * random_color(bool): Control flag of random color generation of point.
    * doTexture(bool): Control flag of doing texture mapping
    * doSmooth(bool): Control flag of doing smooth
    * doAA(bool): Control flag of doing anti-aliasing
    * doAAlevel(int): anti-alising super sampling level
        
    Method Instruction:

    * Interrupt_MouseL(R): Used to deal with mouse click interruption. Canvas will be refreshed with updated buff
    * Interrupt_Keyboard: Used to deal with key board press interruption. Use this to add new keys or new methods
    * drawPoint: method to draw a point
    * drawLine: method to draw a line
    * drawTriangle: method to draw a triangle with filling and smoothing
    
    List of methods to override the ones in CanvasBase:

    * Interrupt_MouseL
    * Interrupt_MouseR
    * Interrupt_Keyboard
        
    Here are some public variables in parent class you might need:

    * points_r: list<Point>. to store all Points from Mouse Right Button
    * points_l: list<Point>. to store all Points from Mouse Left Button
    * buff    : Buff. buff of current frame. Change on it will change display on screen
    * buff_last: Buff. Last frame buffer
        
    """

    debug = 0
    texture_file_path = "./pattern.jpg"
    texture = None

    # control flags
    randomColor = False
    doTexture = False
    doSmooth = False
    doAA = False
    doAAlevel = 4

    # test case status
    MIN_N_STEPS = 6
    MAX_N_STEPS = 192
    n_steps = 12  # For test case only
    test_case_index = 0
    test_case_list = []  # If you need more test case, write them as a method and add it to list

    def __init__(self, parent):
        """
        Initialize the instance, load texture file to Buff, and load test cases.

        :param parent: wxpython frame
        :type parent: wx.Frame
        """
        super(Sketch, self).__init__(parent)
        self.test_case_list = [lambda _: self.clear(),
                               self.testCaseLine01,
                               self.testCaseLine02,
                               self.testCaseTri01,
                               self.testCaseTri02,
                               self.testCaseTriTexture01]  # method at here must accept one argument, n_steps
        # Try to read texture file
        if os.path.isfile(self.texture_file_path):
            # Read image and make it to an ndarray
            texture_image = Image.open(self.texture_file_path)
            texture_array = np.array(texture_image).astype(np.uint8)
            # Because imported image is upside down, reverse it
            texture_array = np.flip(texture_array, axis=0)
            # Store texture image in our Buff format
            self.texture = Buff(texture_array.shape[1], texture_array.shape[0])
            self.texture.setStaticBuffArray(np.transpose(texture_array, (1, 0, 2)))
            if self.debug > 0:
                print("Texture Loaded with shape: ", texture_array.shape)
                print("Texture Buff have size: ", self.texture.size)
        else:
            raise ImportError("Cannot import texture file")

    def __addPoint2Pointlist(self, pointlist, x, y):
        if self.randomColor:
            p = Point((x, y), ColorType(random.random(), random.random(), random.random()))
        else:
            p = Point((x, y), ColorType(1, 0, 0))
        pointlist.append(p)

    # Deal with Mouse Left Button Pressed Interruption
    def Interrupt_MouseL(self, x, y):
        self.__addPoint2Pointlist(self.points_l, x, y)
        # Draw a point when one point provided or a line when two ends provided
        if len(self.points_l) % 2 == 1:
            if self.debug > 0:
                print("draw a point", self.points_l[-1])
            self.drawPoint(self.buff, self.points_l[-1])
        elif len(self.points_l) % 2 == 0 and len(self.points_l) > 0:
            if self.debug > 0:
                print("draw a line from ", self.points_l[-1], " -> ", self.points_l[-2])
            self.drawLine(self.buff, self.points_l[-1], self.points_l[-2], self.doSmooth, self.doAA, self.doAAlevel)
            self.points_l.clear()

    # Deal with Mouse Right Button Pressed Interruption
    def Interrupt_MouseR(self, x, y):
        self.__addPoint2Pointlist(self.points_r, x, y)
        if len(self.points_r) % 3 == 1:
            if self.debug > 0:
                print("draw a point", self.points_r[-1])
            self.drawPoint(self.buff, self.points_r[-1])
        elif len(self.points_r) % 3 == 2:
            if self.debug > 0:
                print("draw a line from ", self.points_r[-1], " -> ", self.points_r[-2])
            self.drawPoint(self.buff, self.points_r[-1])
            self.drawLine(self.buff, self.points_r[-1], self.points_r[-2], self.doSmooth, self.doAA, self.doAAlevel)
        elif len(self.points_r) % 3 == 0 and len(self.points_r) > 0:
            if self.debug > 0:
                print("draw a triangle {} -> {} -> {}".format(self.points_r[-3], self.points_r[-2], self.points_r[-1]))
            self.drawPoint(self.buff, self.points_r[-1])
            self.drawTriangle(self.buff, self.points_r[-3], self.points_r[-2], self.points_r[-1], self.doSmooth, self.doAA, self.doAAlevel, self.doTexture)
            self.points_r.clear()

    def Interrupt_Keyboard(self, keycode):
        """
        keycode Reference: https://docs.wxpython.org/wx.KeyCode.enumeration.html#wx-keycode

        * r, R: Generate Random Color point
        * c, C: clear buff and screen
        * LEFT, UP: Last Test case
        * t, T, RIGHT, DOWN: Next Test case
        """
        # Trigger for test cases
        if keycode in [wx.WXK_LEFT, wx.WXK_UP]:  # Last Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index - 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if keycode in [ord("t"), ord("T"), wx.WXK_RIGHT, wx.WXK_DOWN]:  # Next Test Case
            self.clear()
            if len(self.test_case_list) != 0:
                self.test_case_index = (self.test_case_index + 1) % len(self.test_case_list)
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ",<":
            self.clear()
            self.n_steps = max(self.MIN_N_STEPS, round(self.n_steps / 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)
        if chr(keycode) in ".>":
            self.clear()
            self.n_steps = min(self.MAX_N_STEPS, round(self.n_steps * 2))
            self.test_case_list[self.test_case_index](self.n_steps)
            print("Display Test case: ", self.test_case_index, "n_steps: ", self.n_steps)

        # Switches
        if chr(keycode) in "rR":
            self.randomColor = not self.randomColor
            print("Random Color: ", self.randomColor)
        if chr(keycode) in "cC":
            self.clear()
            print("clear Buff")
        if chr(keycode) in "sS":
            self.doSmooth = not self.doSmooth
            print("Do Smooth: ", self.doSmooth)
        if chr(keycode) in "aA":
            self.doAA = not self.doAA
            print("Do Anti-Aliasing: ", self.doAA)
        if chr(keycode) in "mM":
            self.doTexture = not self.doTexture
            print("texture mapping: ", self.doTexture)

    def queryTextureBuffPoint(self, texture: Buff, x: int, y: int) -> Point:
        """
        Query a point at texture buff, should only be used in texture buff query

        :param texture: The texture buff you want to query from
        :type texture: Buff
        :param x: The query point x coordinate
        :type x: int
        :param y: The query point y coordinate
        :type y: int
        :rtype: Point
        """
        if self.debug > 1:
            if x != min(max(0, int(x)), texture.width - 1):
                print("Warning: Texture Query x coordinate outbound")
            if y != min(max(0, int(y)), texture.height - 1):
                print("Warning: Texture Query y coordinate outbound")
        return texture.getPointFromPointArray(x, y)

    @staticmethod
    def drawPoint(buff, point):
        """
        Draw a point on buff

        :param buff: The buff to draw point on
        :type buff: Buff
        :param point: A point to draw on buff
        :type point: Point
        :rtype: None
        """
        x, y = point.coords
        c = point.color
        # because we have already specified buff.buff has data type uint8, type conversion will be done in numpy
        buff.buff[x, y, 0] = c.r * 255
        buff.buff[x, y, 1] = c.g * 255
        buff.buff[x, y, 2] = c.b * 255

    def smooth1D(self, color1, color2, l, m, r):
        if l!=r:
            dist1 = (m-l)/(r-l)
            dist2 = 1 - dist1
            return ColorType(color1.r*dist2 + color2.r*dist1, color1.g*dist2 + color2.g*dist1, color1.b*dist2 + color2.b*dist1)
        else:
            return color1
        
    def smoothTexture1D(self, texture1, texture2, l, m, r):
        if l!=r:
            dist1 = (m-l)/(r-l)
            dist2 = 1 - dist1
            return [texture1[0]*dist2 + texture2[0]*dist1, texture1[1]*dist2 + texture2[1]*dist1]
        else:
            return texture1
        
    def smoothTexture2D(self, texture):
        l = int (np.floor(texture[0]))
        r = int (np.ceil(texture[0]))
        d = int (np.floor(texture[1]))
        u = int (np.ceil(texture[1]))  

        #print(l, r, d, u) 

        color_ld = self.queryTextureBuffPoint(self.texture, l, d).color
        color_lu = self.queryTextureBuffPoint(self.texture, l, u).color
        color_rd = self.queryTextureBuffPoint(self.texture, r, d).color
        color_ru = self.queryTextureBuffPoint(self.texture, r, u).color

        color_l = self.smooth1D(color_ld, color_lu, d, texture[1], u)
        color_r = self.smooth1D(color_rd, color_ru, d, texture[1], u)

        return self.smooth1D(color_l, color_r, l, texture[0], r)
        
    def alpha(self, buff, x, y, color, alpha):
        bg = buff.getPoint(x, y)
        return self.smooth1D(bg.color, color, 0, alpha, 1)

    def drawLine(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4):
        """
        Draw a line between p1 and p2 on buff

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :rtype: None
        """
        ##### TODO 1: Use Bresenham algorithm to draw a line between p1 and p2 on buff.
        # Requirements:
        #   1. Only integer is allowed in interpolate point coordinates between p1 and p2
        #   2. Float number is allowed in interpolate point color

        color = p2.color

        if not doAA:
            doAAlevel = 1

        if p1.coords[0] > p2.coords[0]:
            p1, p2 = p2, p1

        delta_x = (p2.coords[0] - p1.coords[0]) * doAAlevel + (doAAlevel - 1) * (2 * ((p2.coords[0] - p1.coords[0]) >= 0) - 1)
        delta_y = (p2.coords[1] - p1.coords[1]) * doAAlevel + (doAAlevel - 1) * (2 * ((p2.coords[1] - p1.coords[1]) >= 0) - 1)
        #print(delta_x, delta_y)
        cnt = 1 #Indicate how many subpixels are filled in the current pixel

        #print("START AT ", p1.coords)

        if delta_y>=0 and delta_y<=delta_x:
            prev = 2*delta_y - delta_x
            up = False
            y = p1.coords[1]*doAAlevel

            for x in range(p1.coords[0]*doAAlevel+1, (p2.coords[0]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev>0:
                    y += 1
                    up = True
                    if y%doAAlevel==0:
                        #print("Paint Y", (x-1)//doAAlevel, (y-up)//doAAlevel, cnt/doAAlevel)
                        if doSmooth:
                            self.drawPoint(buff, Point(((x-1)//doAAlevel, (y-up)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y-up)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]), cnt/doAAlevel)))
                        else:
                            self.drawPoint(buff, Point(((x-1)//doAAlevel, (y-up)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y-up)//doAAlevel, color, cnt/doAAlevel)))
                        drawn = True
                        cnt = 0
                else:
                    up = False

                #print(x-1, y-up)

                if up:
                    prev += 2*delta_y - 2*delta_x
                else:
                    prev += 2*delta_y

                if x%doAAlevel==0 and not drawn:
                    #print("Paint X", (x-1)//doAAlevel, (y-up)//doAAlevel, cnt/doAAlevel)
                    if doSmooth:
                        self.drawPoint(buff, Point(((x-1)//doAAlevel, (y-up)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y-up)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]), cnt/doAAlevel)))
                    else:
                        self.drawPoint(buff, Point(((x-1)//doAAlevel, (y-up)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y-up)//doAAlevel, color, cnt/doAAlevel)))
                    cnt = 0
                cnt += 1

        elif delta_y>=0:
            prev = 2*delta_x - delta_y
            right = False
            x = p1.coords[0]*doAAlevel

            for y in range(p1.coords[1]*doAAlevel+1, (p2.coords[1]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev>0:
                    x += 1
                    right = True
                    if x%doAAlevel==0:
                        #print("Paint X", (x-right)//doAAlevel, (y-1)//doAAlevel, cnt/doAAlevel)
                        if doSmooth:
                            self.drawPoint(buff, Point(((x-right)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x-right)//doAAlevel, (y-1)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]), cnt/doAAlevel)))
                        else:
                            self.drawPoint(buff, Point(((x-right)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x-right)//doAAlevel, (y-1)//doAAlevel, color, cnt/doAAlevel)))
                        drawn = True
                        cnt = 0
                else:
                    right = False

                #print(x-right, y-1)

                if right:
                    prev += 2*delta_x - 2*delta_y
                else:
                    prev += 2*delta_x

                if y%doAAlevel==0 and not drawn:
                    #print("Paint Y", (x-right)//doAAlevel, (y-1)//doAAlevel, cnt/doAAlevel)
                    if doSmooth:
                        self.drawPoint(buff, Point(((x-right)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x-right)//doAAlevel, (y-1)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]), cnt/doAAlevel)))
                    else:
                        self.drawPoint(buff, Point(((x-right)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x-right)//doAAlevel, (y-1)//doAAlevel, color, cnt/doAAlevel)))
                    cnt = 0
                cnt += 1

        elif delta_y<0 and delta_y>=-delta_x:
            prev = 2*delta_y + delta_x
            down = False
            y = (p1.coords[1]+1)*doAAlevel-1

            for x in range(p1.coords[0]*doAAlevel+1, (p2.coords[0]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev<0:
                    y -= 1
                    down = True
                    if y%doAAlevel==doAAlevel-1:
                        #print("Paint Y", (x-1)//doAAlevel, (y+down)//doAAlevel, cnt/doAAlevel)
                        if doSmooth:
                            self.drawPoint(buff, Point(((x-1)//doAAlevel, (y+down)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y+down)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]), cnt/doAAlevel)))
                        else: 
                            self.drawPoint(buff, Point(((x-1)//doAAlevel, (y+down)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y+down)//doAAlevel, color, cnt/doAAlevel)))
                        drawn = True
                        cnt = 0
                else:
                    down = False

                #print(x-1, y+down)

                if down:
                    prev += 2*delta_y + 2*delta_x
                else:
                    prev += 2*delta_y

                if x%doAAlevel==0 and not drawn:
                    #print("Paint X", (x-1)//doAAlevel, (y+down)//doAAlevel, cnt/doAAlevel)
                    if doSmooth:
                        self.drawPoint(buff, Point(((x-1)//doAAlevel, (y+down)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y+down)//doAAlevel, self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]), cnt/doAAlevel)))
                    else:
                        self.drawPoint(buff, Point(((x-1)//doAAlevel, (y+down)//doAAlevel), self.alpha(buff, (x-1)//doAAlevel, (y+down)//doAAlevel, color, cnt/doAAlevel)))
                    cnt = 0
                cnt += 1

        elif delta_y<0:
            prev = -2*delta_x - delta_y
            left = False
            x = (p2.coords[0]+1)*doAAlevel-1

            for y in range(p2.coords[1]*doAAlevel+1, (p1.coords[1]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev<0:
                    x -= 1
                    left = True
                    if x%doAAlevel==doAAlevel-1:
                        #print("Paint X", (x+left)//doAAlevel, (y-1)//doAAlevel, cnt/doAAlevel)
                        if doSmooth:
                            self.drawPoint(buff, Point(((x+left)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x+left)//doAAlevel, (y-1)//doAAlevel,self.smooth1D(p2.color, p1.color, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]), cnt/doAAlevel)))
                        else: 
                            self.drawPoint(buff, Point(((x+left)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x+left)//doAAlevel, (y-1)//doAAlevel,color, cnt/doAAlevel)))
                        drawn = True
                        cnt = 0
                else:
                    left = False

                #print(x+left, y-1)

                if left:
                    prev += -2*delta_x - 2*delta_y
                else:
                    prev += -2*delta_x

                if y%doAAlevel==0 and not drawn:
                    #print("Paint Y", (x+left)//doAAlevel, (y-1)//doAAlevel, cnt/doAAlevel)
                    if doSmooth:
                        self.drawPoint(buff, Point(((x+left)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x+left)//doAAlevel, (y-1)//doAAlevel, self.smooth1D(p2.color, p1.color, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]), cnt/doAAlevel)))
                    else:
                        self.drawPoint(buff, Point(((x+left)//doAAlevel, (y-1)//doAAlevel), self.alpha(buff, (x+left)//doAAlevel, (y-1)//doAAlevel, color, cnt/doAAlevel)))
                    cnt = 0
                cnt += 1

        #print("END AT ", p2.coords)

        return

    def findLineBoundary(self, buff, p1, p2, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        Mimic drawing a line between p1 and p2 on buff
        Return the leftmost and rightmost position in each y instead

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: One end point of the line
        :type p1: Point
        :param p2: Another end point of the line
        :type p2: Point
        :param doSmooth: Control flag of color smooth interpolation
        :type doSmooth: bool
        :param doAA: Control flag of doing anti-aliasing
        :type doAA: bool
        :param doAAlevel: anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """

        color = p1.color

        if not doAA:
            doAAlevel = 1

        if p1.coords[0] > p2.coords[0]:
            p1, p2 = p2, p1

        #print(p1, p2)
        delta_x = (p2.coords[0] - p1.coords[0]) * doAAlevel + (doAAlevel - 1) * (2 * ((p2.coords[0] - p1.coords[0]) >= 0) - 1)
        delta_y = (p2.coords[1] - p1.coords[1]) * doAAlevel + (doAAlevel - 1) * (2 * ((p2.coords[1] - p1.coords[1]) >= 0) - 1)
        edge = [[Point((buff.width*doAAlevel+1, 0), ColorType(0, 0, 0)), Point((-1, 0), ColorType(0, 0, 0))] for _ in range(abs(delta_y) + 1)] #Store leftmost and rightmost point in for each y value (subpixel included)
        #print(len(edge))
        #print("START AT ", p1.coords)

        if delta_y>=0 and delta_y<=delta_x:
            prev = 2*delta_y - delta_x
            up = False
            y = p1.coords[1]*doAAlevel

            for x in range(p1.coords[0]*doAAlevel+1, (p2.coords[0]+1)*doAAlevel+1):
                if prev>0:
                    y += 1
                    up = True
                else:
                    up = False

                if up:
                    prev += 2*delta_y - 2*delta_x
                else:
                    prev += 2*delta_y

                if edge[y-up-p1.coords[1]*doAAlevel][0].coords[0] > (x-1):
                    if doTexture:
                        edge[y-up-p1.coords[1]*doAAlevel][0] = Point(((x-1), (y-up)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    elif doSmooth:
                        edge[y-up-p1.coords[1]*doAAlevel][0] = Point(((x-1), (y-up)), self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    else:
                        edge[y-up-p1.coords[1]*doAAlevel][0] = Point(((x-1), (y-up)), color)
                
                if edge[y-up-p1.coords[1]*doAAlevel][1].coords[0] < (x-1):
                    if doTexture:
                        edge[y-up-p1.coords[1]*doAAlevel][1] = Point(((x-1), (y-up)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    elif doSmooth:
                        edge[y-up-p1.coords[1]*doAAlevel][1] = Point(((x-1), (y-up)), self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    else:
                        edge[y-up-p1.coords[1]*doAAlevel][1] = Point(((x-1), (y-up)), color)

        elif delta_y>=0:
            prev = 2*delta_x - delta_y
            right = False
            x = p1.coords[0]*doAAlevel

            for y in range(p1.coords[1]*doAAlevel+1, (p2.coords[1]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev>0:
                    x += 1
                    right = True
                else:
                    right = False

                if right:
                    prev += 2*delta_x - 2*delta_y
                else:
                    prev += 2*delta_x

                if edge[y-1-p1.coords[1]*doAAlevel][0].coords[0] > (x-right):
                    if doTexture:
                        edge[y-1-p1.coords[1]*doAAlevel][0] = Point(((x-right), (y-1)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]))
                    elif doSmooth:
                        edge[y-1-p1.coords[1]*doAAlevel][0] = Point(((x-right), (y-1)), self.smooth1D(p1.color, p2.color, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]))
                    else:
                        edge[y-1-p1.coords[1]*doAAlevel][0] = Point(((x-right), (y-1)), color)
                
                if edge[y-1-p1.coords[1]*doAAlevel][1].coords[0] < (x-right):
                    if doTexture:
                        edge[y-1-p1.coords[1]*doAAlevel][1] = Point(((x-right), (y-1)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]))
                    elif doSmooth:
                        edge[y-1-p1.coords[1]*doAAlevel][1] = Point(((x-right), (y-1)), self.smooth1D(p1.color, p2.color, p1.coords[1], (y-1)//doAAlevel, p2.coords[1]))
                    else:
                        edge[y-1-p1.coords[1]*doAAlevel][1] = Point(((x-right), (y-1)), color)

        elif delta_y<0 and delta_y>=-delta_x:
            prev = 2*delta_y + delta_x
            down = False
            y = (p1.coords[1]+1)*doAAlevel-1

            for x in range(p1.coords[0]*doAAlevel+1, (p2.coords[0]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev<0:
                    y -= 1
                    down = True
                else:
                    down = False

                if down:
                    prev += 2*delta_y + 2*delta_x
                else:
                    prev += 2*delta_y

                if edge[y+down-p2.coords[1]*doAAlevel][0].coords[0] > (x-1):
                    if doTexture:
                        edge[y+down-p2.coords[1]*doAAlevel][0] = Point(((x-1), (y+down)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    elif doSmooth:
                        edge[y+down-p2.coords[1]*doAAlevel][0] = Point(((x-1), (y+down)), self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    else:
                        edge[y+down-p2.coords[1]*doAAlevel][0] = Point(((x-1), (y+down)), color)
                
                if edge[y+down-p2.coords[1]*doAAlevel][1].coords[0] < (x-1):
                    if doTexture:
                        edge[y+down-p2.coords[1]*doAAlevel][1] = Point(((x-1), (y+down)), textureCoords=self.smoothTexture1D(p1.texture, p2.texture, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    elif doSmooth:
                        edge[y+down-p2.coords[1]*doAAlevel][1] = Point(((x-1), (y+down)), self.smooth1D(p1.color, p2.color, p1.coords[0], (x-1)//doAAlevel, p2.coords[0]))
                    else:
                        edge[y+down-p2.coords[1]*doAAlevel][1] = Point(((x-1), (y+down)), color)

        elif delta_y<0:
            prev = -2*delta_x - delta_y
            left = False
            x = (p2.coords[0]+1)*doAAlevel-1

            for y in range(p2.coords[1]*doAAlevel+1, (p1.coords[1]+1)*doAAlevel+1):
                drawn = False #Indicate whether we have drawn this pixel
                if prev<0:
                    x -= 1
                    left = True
                else:
                    left = False

                if left:
                    prev += -2*delta_x - 2*delta_y
                else:
                    prev += -2*delta_x

                if edge[y-1-p2.coords[1]*doAAlevel][0].coords[0] > (x+left):
                    if doTexture:
                        edge[y-1-p2.coords[1]*doAAlevel][0] = Point(((x+left), (y-1)), textureCoords=self.smoothTexture1D(p2.texture, p1.texture, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]))
                    elif doSmooth:
                        edge[y-1-p2.coords[1]*doAAlevel][0] = Point(((x+left), (y-1)), self.smooth1D(p2.color, p1.color, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]))
                    else:
                        edge[y-1-p2.coords[1]*doAAlevel][0] = Point(((x+left), (y-1)), color)
                
                if edge[y-1-p2.coords[1]*doAAlevel][1].coords[0] < (x+left):
                    if doTexture:
                        edge[y-1-p2.coords[1]*doAAlevel][1] = Point(((x+left), (y-1)), textureCoords=self.smoothTexture1D(p2.texture, p1.texture, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]))
                    elif doSmooth:
                        edge[y-1-p2.coords[1]*doAAlevel][1] = Point(((x+left), (y-1)), self.smooth1D(p2.color, p1.color, p2.coords[1], (y-1)//doAAlevel, p1.coords[1]))
                    else:
                        edge[y-1-p2.coords[1]*doAAlevel][1] = Point(((x+left), (y-1)), color)

        #print("END AT ", p2.coords)

        return edge

    def drawTriangle(self, buff, p1, p2, p3, doSmooth=True, doAA=False, doAAlevel=4, doTexture=False):
        """
        draw Triangle to buff. apply smooth color filling if doSmooth set to true, otherwise fill with first point color
        if doAA is true, apply anti-aliasing to triangle based on doAAlevel given.

        :param buff: The buff to edit
        :type buff: Buff
        :param p1: First triangle vertex
        :param p2: Second triangle vertex
        :param p3: Third triangle vertex
        :type p1: Point
        :type p2: Point
        :type p3: Point
        :param doSmooth: Color smooth filling control flag
        :type doSmooth: bool
        :param doAA: Anti-aliasing control flag
        :type doAA: bool
        :param doAAlevel: Anti-aliasing super sampling level
        :type doAAlevel: int
        :param doTexture: Draw triangle with texture control flag
        :type doTexture: bool
        :rtype: None
        """
        ##### TODO 2: Write a triangle rendering function, which support smooth bilinear interpolation of the vertex color

        ##### TODO 3(For CS680 Students): Implement texture-mapped fill of triangle. Texture is stored in self.texture
        # Requirements:
        #   1. For flat shading of the triangle, use the first vertex color.
        #   2. Polygon scan fill algorithm and the use of barycentric coordinate are not allowed in this function
        #   3. You should be able to support both flat shading and smooth shading, which is controlled by doSmooth
        #   4. For texture-mapped fill of triangles, it should be controlled by doTexture flag.

        color = p1.color
        if not doAA:
            doAAlevel = 1
        if not doSmooth or doTexture:
            p2.color = color
            p3.color = color
        if doTexture:
            #Setup for texture mapping
            bound_l = min(min(p1.coords[0], p2.coords[0]), p3.coords[0])
            bound_r = max(max(p1.coords[0], p2.coords[0]), p3.coords[0])
            bound_d = min(min(p1.coords[1], p2.coords[1]), p3.coords[1])
            bound_u = max(max(p1.coords[1], p2.coords[1]), p3.coords[1])
            bound_width = bound_r - bound_l
            bound_height = bound_u - bound_d

            scale = min((self.texture.width - 1)/(bound_width), (self.texture.height - 1)/(bound_height))
            p1.texture = [(self.texture.width - 1)/2 + (p1.coords[0] - bound_l - bound_width/2)*scale, (self.texture.height - 1)/2 + (p1.coords[1] - bound_d - bound_height/2)*scale]
            p2.texture = [(self.texture.width - 1)/2 + (p2.coords[0] - bound_l - bound_width/2)*scale, (self.texture.height - 1)/2 + (p2.coords[1] - bound_d - bound_height/2)*scale]
            p3.texture = [(self.texture.width - 1)/2 + (p3.coords[0] - bound_l - bound_width/2)*scale, (self.texture.height - 1)/2 + (p3.coords[1] - bound_d - bound_height/2)*scale]
            #print(bound_width, bound_height)
            #print(self.texture.width, self.texture.height)
            #print(p1.texture)
            #print(p2.texture)
            #print(p3.texture)
        
        #Sort p to have their y-value ascending
        if p1.coords[1] > p2.coords[1]:
            p1, p2 = p2, p1
        if p2.coords[1] > p3.coords[1]:
            p2, p3 = p3, p2
        if p1.coords[1] > p2.coords[1]:
            p1, p2 = p2, p1

        edge1 = self.findLineBoundary(buff, p1, p2, doSmooth, doAA, doAAlevel, doTexture)                       
        edge2 = self.findLineBoundary(buff, p2, p3, doSmooth, doAA, doAAlevel, doTexture)
        edge3 = self.findLineBoundary(buff, p1, p3, doSmooth, doAA, doAAlevel, doTexture)
        '''
        print("Edge 1: ")
        for points in edge1:
            print(points[0].coords, "->", points[1].coords)
        print("Edge 2: ")
        for points in edge2:
            print(points[0].coords, "->", points[1].coords)
        print("Edge 3: ")
        for points in edge3:
            print(points[0].coords, "->", points[1].coords)
        '''

        #One is the left side, another is the right side
        for _ in range(doAAlevel): 
            edge1.pop()
        side1 = edge1 + edge2
        side2 = edge3
        #print(len(side1), len(side2), p3.coords[1]*doAAlevel - p1.coords[1]*doAAlevel + 1)
        for y in range(p1.coords[1], p3.coords[1]+1):
            left = Point((buff.width*doAAlevel+1, y))
            right = Point((-1, y))
            for y_sub in range(doAAlevel): #y_sub refers to subpixel
                y_side = (y-p1.coords[1])*doAAlevel + y_sub

                if side1[y_side][0].coords[0] < side2[y_side][0].coords[0]:
                    if side1[y_side][0].coords[0] < left.coords[0]:
                        left = side1[y_side][0]
                else:
                    if side2[y_side][0].coords[0] < left.coords[0]:
                        left = side2[y_side][0]

                if side1[y_side][1].coords[0] > side2[y_side][1].coords[0]:
                    if side1[y_side][1].coords[0] > right.coords[0]:
                        right = side1[y_side][1]
                else:
                    if side2[y_side][1].coords[0] > right.coords[0]:
                        right = side2[y_side][1]

            #print(left.coords[0]//doAAlevel, right.coords[0]//doAAlevel, y)

            for x in range(left.coords[0]//doAAlevel, right.coords[0]//doAAlevel+1):
                '''
                cnt = 0 #count number of subpixels in the pixel
                for y_sub in range(doAAlevel): #y_sub refers to subpixel
                    y_side = (y-p1.coords[1])*doAAlevel + y_sub
                    #cnt += min(right.coords[0], (x+1)*doAAlevel - 1) - max(left.coords[0], x*doAAlevel) + 1

                if doSmooth:
                    self.drawPoint(buff, Point((x, y), self.alpha(buff, x, y, self.smooth1D(left.color, right.color, left.coords[0]//doAAlevel, x, right.coords[0]//doAAlevel), cnt/(doAAlevel**2))))
                else:
                    self.drawPoint(buff, Point((x, y), self.alpha(buff, x, y, color, cnt/(doAAlevel**2))))'''
                
                cnt_x = 0 #count number of subpixels in the pixel horizontally
                cnt_y = 0 #count number of subpixels in the pixel vertically
                for y_sub in range(doAAlevel): #y_sub refers to subpixel
                    y_side = (y-p1.coords[1])*doAAlevel + y_sub
                    cnt_x = max(cnt_x, min(right.coords[0], (x+1)*doAAlevel - 1) - max(left.coords[0], x*doAAlevel) + 1)
                    cnt_y += min(min(right.coords[0], (x+1)*doAAlevel - 1) - max(left.coords[0], x*doAAlevel) + 1, 1)
                    cnt = max(cnt_x, cnt_y)

                if doTexture:
                    #print('(', left.coords[0]//doAAlevel, ',', right.coords[0]//doAAlevel, ') ->', self.smoothTexture1D(left.texture, right.texture, left.coords[0]//doAAlevel, x, right.coords[0]//doAAlevel))
                    self.drawPoint(buff, Point((x, y), self.smoothTexture2D(self.smoothTexture1D(left.texture, right.texture, left.coords[0]//doAAlevel, x, right.coords[0]//doAAlevel))))
                elif doSmooth:
                    self.drawPoint(buff, Point((x, y), self.alpha(buff, x, y, self.smooth1D(left.color, right.color, left.coords[0]//doAAlevel, x, right.coords[0]//doAAlevel), cnt/doAAlevel)))
                else:
                    self.drawPoint(buff, Point((x, y), self.alpha(buff, x, y, color, cnt/doAAlevel)))

        return

    # test for lines lines in all directions
    def testCaseLine01(self, n_steps):
        center_x = int(self.buff.width / 2)
        center_y = int(self.buff.height / 2)
        radius = int(min(self.buff.width, self.buff.height) * 0.45)

        v0 = Point([center_x, center_y], ColorType(1, 1, 0))
        for step in range(0, n_steps):
            theta = math.pi * step / n_steps
            v1 = Point([center_x + int(math.sin(theta) * radius), center_y + int(math.cos(theta) * radius)],
                       ColorType(0, 0, (1 - step / n_steps)))
            v2 = Point([center_x - int(math.sin(theta) * radius), center_y - int(math.cos(theta) * radius)],
                       ColorType(0, (1 - step / n_steps), 0))
            self.drawLine(self.buff, v2, v0, doSmooth=True)
            self.drawLine(self.buff, v0, v1, doSmooth=True)

    # test for lines: drawing circle and petal 
    def testCaseLine02(self, n_steps):
        n_steps = 2 * n_steps
        d_theta = 2 * math.pi / n_steps
        d_petal = 12 * math.pi / n_steps
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        radius = (0.75 * min(cx, cy))
        p = radius * 0.25

        # Outer petals
        for i in range(n_steps + 2):
            self.drawLine(self.buff,
                          Point((math.floor(0.5 + radius * math.sin(d_theta * i) + p * math.sin(d_petal * i)) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * i) + p * math.cos(d_petal * i)) + cy),
                                ColorType(1, (128 + math.sin(d_theta * i * 5) * 127) / 255,
                                          (128 + math.cos(d_theta * i * 5) * 127) / 255)),
                          Point((math.floor(
                              0.5 + radius * math.sin(d_theta * (i + 1)) + p * math.sin(d_petal * (i + 1))) + cx,
                                 math.floor(0.5 + radius * math.cos(d_theta * (i + 1)) + p * math.cos(
                                     d_petal * (i + 1))) + cy),
                                ColorType(1, (128 + math.sin(d_theta * 5 * (i + 1)) * 127) / 255,
                                          (128 + math.cos(d_theta * 5 * (i + 1)) * 127) / 255)),
                          doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

        # Draw circle
        for i in range(n_steps + 1):
            v0 = Point((math.floor(0.5 * radius * math.sin(d_theta * i)) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * i)) + cy), ColorType(1, 97. / 255, 0))
            v1 = Point((math.floor(0.5 * radius * math.sin(d_theta * (i + 1))) + cx,
                        math.floor(0.5 * radius * math.cos(d_theta * (i + 1))) + cy), ColorType(1, 97. / 255, 0))
            self.drawLine(self.buff, v0, v1, doSmooth=True, doAA=self.doAA, doAAlevel=self.doAAlevel)

    # test for smooth filling triangle
    def testCaseTri01(self, n_steps):
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v1, v0, v2, False, self.doAA, self.doAAlevel)

    def testCaseTri02(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            self.drawTriangle(self.buff, v0, v1, v2, True, self.doAA, self.doAAlevel)

    def testCaseTriTexture01(self, n_steps):
        # Test case for no smooth color filling triangle
        n_steps = int(n_steps / 2)
        delta = 2 * math.pi / n_steps
        radius = int(min(self.buff.width, self.buff.height) * 0.45)
        cx = int(self.buff.width / 2)
        cy = int(self.buff.height / 2)
        theta = 0

        triangleList = []
        for _ in range(n_steps):
            theta += delta
            v0 = Point((cx, cy), ColorType(1, 1, 1))
            v1 = Point((int(cx + math.sin(theta) * radius), int(cy + math.cos(theta) * radius)),
                       ColorType((127. + 127. * math.sin(theta)) / 255,
                                 (127. + 127. * math.sin(theta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + 4 * math.pi / 3)) / 255))
            v2 = Point((int(cx + math.sin(theta + delta) * radius), int(cy + math.cos(theta + delta) * radius)),
                       ColorType((127. + 127. * math.sin(theta + delta)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 2 * math.pi / 3)) / 255,
                                 (127. + 127. * math.sin(theta + delta + 4 * math.pi / 3)) / 255))
            triangleList.append([v0, v1, v2])

        for t in triangleList:
            self.drawTriangle(self.buff, *t, doTexture=True)


if __name__ == "__main__":
    def main():
        print("This is the main entry! ")
        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE & ~(wx.RESIZE_BORDER | wx.MAXIMIZE_BOX))

        canvas = Sketch(frame)
        canvas.debug = 0

        frame.Show()
        app.MainLoop()


    def codingDebug():
        """
        If you are still working on the assignment, we suggest to use this as the main call.
        There will be more strict type checking in this version, which might help in locating your bugs.
        """
        print("This is the debug entry! ")
        import cProfile
        import pstats
        profiler = cProfile.Profile()
        profiler.enable()

        app = wx.App(False)
        # Set FULL_REPAINT_ON_RESIZE will repaint everything when scaling the frame
        # here is the style setting for it: wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE
        # wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER will disable canvas resize.
        frame = wx.Frame(None, size=(500, 500), title="Test", style=wx.DEFAULT_FRAME_STYLE | wx.FULL_REPAINT_ON_RESIZE)
        canvas = Sketch(frame)
        canvas.debug = 2
        frame.Show()
        app.MainLoop()

        profiler.disable()
        stats = pstats.Stats(profiler).sort_stats('cumtime').reverse_order()
        stats.print_stats()


    main()
    # codingDebug()
    

