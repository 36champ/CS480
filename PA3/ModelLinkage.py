"""
Model our creature and wrap it in one class
First version at 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

Modified by Daniel Scrivener 08/2022
"""
import random
import numpy as np

from Component import Component
from Shapes import Cube
from Shapes import Hair
from Shapes import Sphere
from Shapes import Cone
from Shapes import Cylinder
from Point import Point
import ColorType as Ct
from EnvironmentObject import EnvironmentObject
from Quaternion import Quaternion

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

##### TODO 1: Construct your two different creatures
# Requirements:
#   1. For the basic parts of your creatures, feel free to use routines provided with the previous assignment.
#   You are also free to create your own basic parts, but they must be polyhedral (solid).
#   2. The creatures you design should have moving linkages of the basic parts: legs, arms, wings, antennae,
#   fins, tentacles, etc.
#   3. Model requirements:
#         1. Predator: At least one (1) creature. Should have at least two moving parts in addition to the main body
#         2. Prey: At least two (2) creatures. The two prey can be instances of the same design. Should have at
#         least one moving part.
#         3. The predator and prey should have distinguishable different colors.
#         4. You are welcome to reuse your PA2 creature in this assignment.

class Jellyfish(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None
    rotation_speed = None
    translation_speed = None

    def __init__(self, parent, position, shaderProg):
        super(Jellyfish, self).__init__(position)
        arm1 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm2.setDefaultAngle(120, arm2.vAxis)
        arm3 = ModelArm(parent, Point((0, 0, 0)), shaderProg, 0.1)
        arm3.setDefaultAngle(240, arm3.vAxis)

        self.components = arm1.components + arm2.components + arm3.components
        self.addChild(arm1)
        self.addChild(arm2)
        self.addChild(arm3)

        self.rotation_speed = []
        for comp in self.components:

            comp.setRotateExtent(comp.uAxis, 0, 35)
            comp.setRotateExtent(comp.vAxis, -45, 45)
            comp.setRotateExtent(comp.wAxis, -45, 45)
            self.rotation_speed.append([0.5, 0, 0])

        self.translation_speed = Point([random.random()-0.5 for _ in range(3)]).normalize() * 0.01

        self.bound_center = Point((0, 0, 0))
        self.bound_radius = 0.1 * 4
        self.species_id = 1

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        for i, comp in enumerate(self.components):
            comp.rotate(self.rotation_speed[i][0], comp.uAxis)
            comp.rotate(self.rotation_speed[i][1], comp.vAxis)
            comp.rotate(self.rotation_speed[i][2], comp.wAxis)
            if comp.uAngle in comp.uRange:  # rotation reached the limit
                self.rotation_speed[i][0] *= -1
            if comp.vAngle in comp.vRange:
                self.rotation_speed[i][1] *= -1
            if comp.wAngle in comp.wRange:
                self.rotation_speed[i][2] *= -1
        self.vAngle = (self.vAngle + 3) % 360

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        pass

class ModelArm(Component):
    """
    Define our linkage model
    """

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, linkageLength=0.5, display_obj=None):
        super().__init__(position, display_obj)
        self.components = []
        self.contextParent = parent

        link1 = Cube(Point((0, 0, 0)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE1)
        link2 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE2)
        link3 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE3)
        link4 = Cube(Point((0, 0, linkageLength)), shaderProg, [linkageLength / 4, linkageLength / 4, linkageLength], Ct.DARKORANGE4)

        self.addChild(link1)
        link1.addChild(link2)
        link2.addChild(link3)
        link3.addChild(link4)

        self.components = [link1, link2, link3, link4]

class Rabbit(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None

    def __init__(self, parent, position, shaderProg):
        super(Rabbit, self).__init__(position)

        self.t = 0
        self.collision_list = []
        self.ignore_time = 0
        self.credibility = 1

        parts = {
            "head": {
                "shape": "sphere",
                "point": (0, 0, 2.5),
                "scale": [1, 1, 1],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": -30, "axis": "v"}],
                "origin": (0, 0, 2.5),
                },

            "L_eye_1": {
                "shape": "cube",
                "point": (0.911, 0, 2.5),
                "scale": [0.05, 0.05, 0.6],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -15, "axis": "v"}, {"deg": 15, "axis": "w"}],
                "origin": (0, 0, 2.5),
                },
            "R_eye_1": {
                "shape": "cube",
                "point": (0.911, 0, 2.5),
                "scale": [0.05, 0.05, 0.6],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -15, "axis": "v"}, {"deg": -15, "axis": "w"}],
                "origin": (0, 0, 2.5),
                },

            "L_ear": {
                "shape": "sphere",
                "point": (0, 0.6, 3.6),
                "scale": [0.15, 0.25, 0.8],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, 0.6, 3.6),
                },
            "R_ear": {
                "shape": "sphere",
                "point": (0, -0.6, 3.6),
                "scale": [0.15, 0.25, 0.8],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, -0.6, 3.6),
                },

            "core": {
                "shape": "sphere",
                "point": (0, 0, 0),
                "scale": [0, 0, 0],
                "color": Ct.WHITE,
                # "initial_rotation": [],
                "initial_rotation": [{"deg": -90, "axis": "u"}, {"deg": -30, "axis": "w"}],
                # "initial_rotation": [{"deg": -90, "axis": "u"}, {"deg": -90, "axis": "v"}],
                "origin": (0, 0, 0),
                },
            "bound": {
                "shape": "sphere",
                "point": (0, 0, 0),
                "scale": [0, 0, 0],
                "color": Ct.BLACK,
                "initial_rotation": [],
                "origin": (0, 0, 0),
                },

            "body": {
                "shape": "sphere",
                "point": (0, 0, 1),
                "scale": [0.8, 0.8, 0.9],
                "color": Ct.GRAY,
                "initial_rotation": [{"deg": -30, "axis": "v"}],
                "origin": (0, 0, 1),
                },

            "tail": {
                "shape": "sphere",
                "point": (-0.8, 0, 0.6),
                "scale": [0.2, 0.2, 0.2],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (-0.8, 0, 0.6),
                },

            "L_hand": {
                "shape": "sphere",
                "point": (0.4, 0.5, 1.6),
                "scale": [0.6, 0.25, 0.15],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": 30, "axis": "v"}, {"deg": 45, "axis": "w"}],
                "origin": (0, 0.5, 1.6),
                },
            "R_hand": {
                "shape": "sphere",
                "point": (0.4, -0.5, 1.6),
                "scale": [0.6, 0.25, 0.15],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": 30, "axis": "v"}, {"deg": -45, "axis": "w"}],
                "origin": (0, -0.5, 1.6),
                },

            "L_foot": {
                "shape": "sphere",
                "point": (0.4, 0.4, 0.4),
                "scale": [0.6, 0.25, 0.15],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, 0.4, 0.4),
                },
            "R_foot": {
                "shape": "sphere",
                "point": (0.4, -0.4, 0.4),
                "scale": [0.6, 0.25, 0.15],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, -0.4, 0.4),
                },
        }

        childList = {
            "bound": ["core"],
            "core": ["head", "body"],

            "head": ["L_ear", "R_ear", "L_eye_1", "R_eye_1"],
            "body": ["L_hand", "R_hand", "L_foot", "R_foot", "tail"],
        }
        parentDict = {
            "bound": None,
            "core": "bound",

            "head": "core",

            "L_eye_1": "head",
            "R_eye_1": "head",

            "L_ear": "head",
            "R_ear": "head",

            "body": "core",

            "L_hand": "body",
            "R_hand": "body",
            "L_foot": "body",
            "R_foot": "body",
            "tail": "body",
        }

        self.speed = 0.04
        self.direction = Point([random.random()-0.5 for _ in range(3)]).normalize()
        # self.direction = Point([-(2**0.5), -1, -1]).normalize()
        # self.direction = Point([1, 0, 0]).normalize()
        # self.direction = Point([3**0.5, 0, 1]).normalize()
        # self.direction = Point([0, 0, 1]).normalize()

        scale = 0.1 + random.random() * 0.05
        # scale = 0.12
        r = 0.911
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = Point((0.625*scale, (5*(3**0.5)/4+1.1+1.7*r)/2*scale, 0)).norm()
        # print(self.bound_center, self.bound_radius)
        self.species_id = 1
        # self.name = random.randint(1000, 9999)
        # print(self.name)
        obj = {}
        queue = ["bound"]

        self.components = dict()

        while len(queue):
            part = queue.pop(0)
            parent = parentDict[part]

            if parent == "bound":
                center = ((parts[part]["point"][0]-parts[parent]["point"][0]-0.625)*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1]-(5*(3**0.5)/4+2.1-0.1*r)/2)*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0]-0.625)*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1]-(5*(3**0.5)/4+2.1-0.1*r)/2)*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            elif parent: 
                center = ((parts[part]["point"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            else:
                center = ((parts[part]["point"][0])*scale, 
                          parts[part]["point"][1] *scale, 
                          (parts[part]["point"][2])*scale)
                origin = ((parts[part]["origin"][0])*scale, 
                          parts[part]["origin"][1]*scale, 
                          (parts[part]["origin"][2])*scale)

            scaling = [val*scale for val in parts[part]["scale"]]
            if parts[part]["shape"] == "sphere":
                obj[part] = Sphere(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "cube":
                obj[part] = Cube(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))

            if "rotation_axis" in parts[part].keys():
                obj[part].changeRotationAxis(*parts[part]["rotation_axis"])
            
            for rotation in parts[part]["initial_rotation"]:
                if rotation["axis"] == "u":
                    # obj[part].rotate(rotation["deg"], obj[part].uAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].uAxis)
                elif rotation["axis"] == "v":
                    # obj[part].rotate(rotation["deg"], obj[part].vAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].vAxis)
                elif rotation["axis"] == "w":
                    # obj[part].rotate(rotation["deg"], obj[part].wAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].wAxis)

            if parent:
                obj[parent].addChild(obj[part])
            else:
                self.addChild(obj[part])

            self.components[part] = obj[part]

            if part in childList:
                for child in childList[part]:
                    queue.append(child)

        self.components["bound"].quat = Quaternion(1, 0, 0, 0)
        
        # rotation_limits = {
        #     "head": [(-30, 30), (-30, 30), (-45, 45)],
        # }

        # for part, limit in rotation_limits.items():
        #     obj[part].setRotateExtent(obj[part].uAxis, obj[part].default_uAngle + limit[0][0], obj[part].default_uAngle + limit[0][1])
        #     obj[part].setRotateExtent(obj[part].vAxis, obj[part].default_vAngle + limit[1][0], obj[part].default_vAngle + limit[1][1])
        #     obj[part].setRotateExtent(obj[part].wAxis, obj[part].default_wAngle + limit[2][0], obj[part].default_wAngle + limit[2][1])

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        
        self.t += 1

        t = self.t % 60
        K = np.e**(-9 + 0.6 * abs(t - 30))

        if abs(t - 30) > 3:
            angle = 60 / (1 + K)
        else:
            angle = 60

        parts = ["L_foot", "R_foot"]
        for part in parts:
            self.components[part].setCurrentAngle(angle, self.components[part].vAxis)

        parts = ["L_hand", "R_hand"]
        for part in parts:
            self.components[part].setCurrentAngle(30 + angle/2, self.components[part].vAxis)

        if t > 30:
            self.speed = (0.1 - 0.2 * K * (1 + K)**(-2)) * 0.2 * (0.5 + random.random() * 1) * 2
        else:
            self.speed = (0.2 * K * (1 + K)**(-2) + 0.1) * 0.2 * (0.5 + random.random() * 1) * 2

        # print(self.speed)

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        credibility = 0
        count = 0
        direction = Point((0, 0, 0))
        for component in components:
            temp = component.currentPos - self.currentPos
            if component.species_id == 1 and self.ignore_time == 0:
                if temp.norm() > 0.1 * self.bound_radius and temp.norm() < self.bound_radius + component.bound_radius:
                    # print(temp.norm(), self.name, component.name)
                    self.collision_list += [component]
                    component.collision_list += [self]
                elif temp.norm() < 2.5 * self.bound_radius:
                    # print(self.name, component.name)
                    direction += component.direction * component.credibility
                    credibility += component.credibility
                    count += 1
            elif component.species_id == 2:
                if temp.norm() < 5 * self.bound_radius:
                    # print(self.name, component.name)
                    direction -= temp * (1/temp.norm())
            elif component.species_id == 3:
                if temp.norm() < self.bound_radius + component.bound_radius:
                    # print(temp.norm(), self.name, component.name)
                    self.collision_list += [component]
                    component.collision_list += [self]
                elif temp.norm() < 10 * self.bound_radius:
                    # print(self.name, component.name)
                    direction += temp * (0.1/temp.norm())

        if len(self.collision_list) != 0:
            self.collide(vivarium)
        elif direction.norm() > 0 and component.ignore_time == 0:
            # print(self.direction)
            self.direction = direction.normalize()

        if count != 0:
            self.credibility = max(credibility / count - 9, 1)
        else:
            self.credibility = max(self.credibility - 9, 1)
        self.ignore_time = max(0, self.ignore_time - 1)

        # self.speed = 0
        # self.speed = 0.02 + self.t/1000

        # self.direction = Point((np.cos(self.t/300), np.sin(self.t/300), 3**0.5)).normalize()
        nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)

        hitXright = nextPosition.coords[0] > tank_dimensions[0] / 2 - 1.5 * self.bound_radius
        hitXleft = nextPosition.coords[0] < (-tank_dimensions[0] / 2) + 1.5 * self.bound_radius
        hitYtop = nextPosition.coords[1] > tank_dimensions[1] / 2 - 1.5 * self.bound_radius
        hitYbottom = nextPosition.coords[1] < (-tank_dimensions[1] / 2) + 1.5 * self.bound_radius
        hitZfront = nextPosition.coords[2] > tank_dimensions[2] / 2 - 1.5 * self.bound_radius
        hitZback = nextPosition.coords[2] < (-tank_dimensions[2] / 2) + 1.5 * self.bound_radius
        if hitXright or hitXleft:
            self.direction.coords[0] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)
        if hitYtop or hitYbottom:
            self.direction.coords[1] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)
        if hitZfront or hitZback:
            self.direction.coords[2] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)

        nextPosition = self.currentPos + (self.direction * self.speed)
        self.to_q = Quaternion()

        if self.direction.coords[0] >= 0:
            rotation_axis = self.uAxis.cross3d(self.direction).normalize()
            if rotation_axis.norm() == 0:
                rotation_axis = Point((0, 1, 0))

            theta = np.arccos(self.uAxis.dot(self.direction))
            self.to_q = Quaternion(np.cos(theta/2), *([np.sin(theta/2)*val for val in rotation_axis]))
        else:
            u, v, w = self.direction
            theta = theta = np.pi/2
            if v:
                theta = np.arctan((1-u)/v)
            cos_phi = (u-1)/np.sin(theta)**2 + 1
            sin_phi = -w/np.sin(theta)
            if cos_phi > 1:
                cos_phi = 1
            if cos_phi < -1:
                cos_phi = -1
            phi = np.arccos(cos_phi)
            n = Point()

            if sin_phi >= 0:
                n = Point((np.cos(theta), np.sin(theta), 0))
            else:
                n = Point((-np.cos(theta), -np.sin(theta), 0))

            self.to_q = Quaternion(np.cos(phi/2), *([np.sin(phi/2)*val for val in n]))

        # print(self.direction.coords, rotation_axis.coords, q.s, q.v)
        self.slerp()
        self.setCurrentPosition(nextPosition)

    def collide(self, vivarium):
        # print(self.currentPos.coords, [x.currentPos.coords for x in self.collision_list])
        # print(self.name, [x.name for x in self.collision_list])

        direction = Point((0, 0, 0))
        for component in self.collision_list:
            if component.species_id == 1:
                # self.ignore_time = 30
                direction += (self.currentPos - component.currentPos).normalize()
            elif component.species_id == 3:
                if component in vivarium.components:
                    vivarium.delObjInTank(component)

        if direction.norm() > 0:
            self.direction = direction.normalize()

        self.collision_list = []
        self.collision_list = []
        
    def check(self):
        q = self.components["bound"].quat.multiply(self.to_q)

        # print(q.s, q.v)

        if q.s < 0:
            self.to_q.s = -self.to_q.s
            self.to_q.v = [-self.to_q.v[i] for i in range(3)]

    def slerp(self):
        self.check()

        q1 = self.components["bound"].quat.conjugate()
        q2 = self.to_q
        q = Quaternion()
        cos = q1.s * q2.s + Point(q1.v).dot(Point(q2.v))
        if cos > 1:
            cos = 1
        elif cos < -1:
            cos = -1
        theta = np.arccos(cos)

        if theta != 0:
            u = min(np.pi/15/theta, 1)
            q = Quaternion()
            q.s = (np.sin((1-u) * theta) * q1.s + np.sin(u * theta) * q2.s) / np.sin(theta)
            q.v[0] = (np.sin((1-u) * theta) * q1.v[0] + np.sin(u * theta) * q2.v[0]) / np.sin(theta)
            q.v[1] = (np.sin((1-u) * theta) * q1.v[1] + np.sin(u * theta) * q2.v[1]) / np.sin(theta)
            q.v[2] = (np.sin((1-u) * theta) * q1.v[2] + np.sin(u * theta) * q2.v[2]) / np.sin(theta)
            
            p = Quaternion(0, 1, 0, 0)
            p = q.multiply(p.multiply(q.conjugate()))

            # self.direction = Point(p.v)

            q = q.conjugate()
        else:
            q = q1.conjugate()


        self.components["bound"].setQuaternion(q)
        # print(q1.s, q1.v, q.s, q.v, q2.s, q2.v)
        # if u == 0:
            # print(q1.s, q1.v, q.s, q.v, q2.s, q2.v, u)
            # print(self.direction)
        
class Tewi(Component, EnvironmentObject):

    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None

    def __init__(self, parent, position, shaderProg):
        super(Tewi, self).__init__(position)

        self.t = 0
        self.collision_list = []
        self.ignore_time = 0
        self.credibility = 1

        parts = {
            "head": {
                "shape": "sphere",
                "point": (0, 0, 2.8435),
                "scale": [1, 1, 1],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0, 1.934),
                },
            "hair": {
                "shape": "hair",
                "point": (0, 0, 2.8435),
                "scale": [1.1, 1.1, 1.1],
                "color": Ct.BLACK,
                "initial_rotation": [],
                "origin": (0, 0, 2.8435),
                },
            "L_ear": {
                "shape": "sphere",
                "point": (0, 0.6, 4.2),
                "scale": [0.15, 0.25, 0.8],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": -15, "axis": "u"}],
                "origin": (0, 0.6, 3.6),
                },
            "R_ear": {
                "shape": "sphere",
                "point": (0, -0.6, 4.2),
                "scale": [0.15, 0.25, 0.8],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": 15, "axis": "u"}],
                "origin": (0, -0.6, 3.6),
                },

            "L_eye_1": {
                "shape": "sphere",
                "point": (0.72, 0.3, 3),
                "scale": [0.2, 0.2, 0.2],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0.72, 0.3, 3),
                },
            "L_eye_2": {
                "shape": "sphere",
                "point": (0.82, 0.3, 3),
                "scale": [0.1, 0.1, 0.12],
                "color": Ct.SOFTRED,
                "initial_rotation": [],
                "origin": (0.72, 0.3, 3),
                },
            "L_eye_3": {
                "shape": "sphere",
                "point": (0.9, 0.3, 3),
                "scale": [0.02, 0.02, 0.024],
                "color": Ct.RED,
                "initial_rotation": [],
                "origin": (0.72, 0.3, 3),
                }, 

            "R_eye_1": {
                "shape": "sphere",
                "point": (0.72, -0.3, 3),
                "scale": [0.2, 0.2, 0.2],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0.72, -0.3, 3),
                },
            "R_eye_2": {
                "shape": "sphere",
                "point": (0.82, -0.3, 3),
                "scale": [0.1, 0.1, 0.12],
                "color": Ct.SOFTRED,
                "initial_rotation": [],
                "origin": (0.72, -0.3, 3),
                },
            "R_eye_3": {
                "shape": "sphere",
                "point": (0.9, -0.3, 3),
                "scale": [0.02, 0.02, 0.024],
                "color": Ct.RED,
                "initial_rotation": [],
                "origin": (0.72, -0.3, 3),
                }, 

            "neck": {
                "shape": "cylinder",
                "point": (0, 0, 1.95),
                "scale": [0.2, 0.2, 0.2],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0, 1.755),
                },

            "shoulder": {
                "shape": "cone",
                "point": (0, 0, 1.65),
                "scale": [0.65, 1, 0.2],
                "color": Ct.PINK,
                "initial_rotation": [],
                "origin": (0, 0, 1.65),
                },

            "L_arm_1": {
                "shape": "cylinder",
                "point": (0, 0.85, 0.66),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0.85, 1.435),
                },
            "L_arm_2": {
                "shape": "cylinder",
                "point": (0, 0.85, -0.89),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0.85, -0.115),
                },
            "L_hand": {
                "shape": "sphere",
                "point": (0.225, 0.85, -1.665),
                "scale": [0.45, 0.3, 0.2],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0.85, -1.665),
                },
            "L_arm_joint_1": {
                "shape": "sphere",
                "point": (0, 0.85, 1.435),
                "scale": [0.19, 0.19, 0.1],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, 0.85, 1.435),
                },
            "L_arm_joint_2": {
                "shape": "sphere",
                "point": (0, 0.85, -0.115),
                "scale": [0.19, 0.19, 0.19],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0.85, -0.115),
                },

            "R_arm_1": {
                "shape": "cylinder",
                "point": (0, -0.85, 0.66),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, -0.85, 1.435),
                "rotation_axis": [Point([-1, 0, 0]), Point([0, 1, 0]), Point([0, 0, 1])]
                },
            "R_arm_2": {
                "shape": "cylinder",
                "point": (0, -0.85, -0.89),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, -0.85, -0.115),
                "rotation_axis": [Point([-1, 0, 0]), Point([0, 1, 0]), Point([0, 0, -1])]
                },
            "R_hand": {
                "shape": "sphere",
                "point": (0.225, -0.85, -1.665),
                "scale": [0.45, 0.3, 0.2],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, -0.85, -1.665),
                "rotation_axis": [Point([1, 0, 0]), Point([0, 1, 0]), Point([0, 0, -1])]
                },
            "R_arm_joint_1": {
                "shape": "sphere",
                "point": (0, -0.85, 1.435),
                "scale": [0.19, 0.19, 0.1],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, -0.85, 1.435),
                },
            "R_arm_joint_2": {
                "shape": "sphere",
                "point": (0, -0.85, -0.115),
                "scale": [0.19, 0.19, 0.19],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, -0.85, -0.115),
                },

            "body": {
                "shape": "cylinder",
                "point": (0, 0, 0.47),
                "scale": [0.7, 0.7, 1],
                "color": Ct.PINK,
                "initial_rotation": [],
                "origin": (0, 0, 0.47),
                },
            "core": {
                "shape": "sphere",
                "point": (0, 0, 0.47),
                "scale": [0, 0, 0],
                "color": Ct.RED,
                "initial_rotation": [{"deg": -90, "axis": "u"}],
                "origin": (0, 0, 0.47),
                },
            "bound": {
                "shape": "sphere",
                "point": (0, 0, 0),
                "scale": [0, 0, 0],
                "color": Ct.BLACK,
                "initial_rotation": [],
                "origin": (0, 0, 0),
                },

            "pelvis": {
                "shape": "cone",
                "point": (0, 0, -0.71),
                "origin": (0, 0, -0.71),
                "scale": [0.66, 0.66, 0.2],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": 180, "axis": "u"}],
                },
            "skirt": {
                "shape": "cone",
                "point": (0, 0, -0.2),
                "origin": (0, 0, -0.2),
                "scale": [1.5, 1.5, 2],
                "color": Ct.PINK,
                "initial_rotation": [],
                },
            "tail": {
                "shape": "sphere",
                "point": (-1, 0, -0.3),
                "origin": (-1, 0, -0.3),
                "scale": [0.4, 0.4, 0.4],
                "color": Ct.WHITE,
                "initial_rotation": [],
                },

            "L_leg_1": {
                "shape": "cylinder",
                "point": (0, -0.5, -1.28 - 0.4158),
                "origin": (0, -0.5, -0.505 - 0.4158),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [{"deg": -180, "axis": "u"}],
                },
            "L_leg_2": {
                "shape": "cylinder",
                "point": (0, -0.5, -2.83 - 0.4158),
                "origin": (0, -0.5, -2.055 - 0.4158),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },
            "L_foot": {
                "shape": "sphere",
                "point": (0.3, -0.5, -3.7 - 0.4158),
                "origin": (0, -0.5, -3.7 - 0.4158),
                "scale": [0.6, 0.3, 0.2],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },
            "L_leg_joint_1": {
                "shape": "sphere",
                "point": (0, -0.5, -0.505 - 0.4158),
                "origin": (0, -0.5, -0.505 - 0.4158),
                "scale": [0.19, 0.19, 0.1],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },
            "L_leg_joint_2": {
                "shape": "sphere",
                "point": (0, -0.5, -2.055 - 0.4158),
                "origin": (0, -0.5, -2.055 - 0.4158),
                "scale": [0.19, 0.19, 0.19],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },

            "R_leg_1": {
                "shape": "cylinder",
                "point": (0, 0.5, -1.28 - 0.4158),
                "origin": (0, 0.5, -0.505 - 0.4158),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [{"deg": -180, "axis": "u"}],
                "rotation_axis": [Point([-1, 0, 0]), Point([0, 1, 0]), Point([0, 0, 1])],
                },
            "R_leg_2": {
                "shape": "cylinder",
                "point": (0, 0.5, -2.83 - 0.4158),
                "origin": (0, 0.5, -2.055 - 0.4158),
                "scale": [0.18, 0.18, 0.8],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "rotation_axis": [Point([-1, 0, 0]), Point([0, 1, 0]), Point([0, 0, 1])],
                },
            "R_foot": {
                "shape": "sphere",
                "point": (0.3, 0.5, -3.7 - 0.4158),
                "origin": (0, 0.5, -3.7 - 0.4158),
                "scale": [0.6, 0.3, 0.2],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "rotation_axis": [Point([1, 0, 0]), Point([0, 1, 0]), Point([0, 0, -1])]
                },
            "R_leg_joint_1": {
                "shape": "sphere",
                "point": (0, 0.5, -0.505 - 0.4158),
                "origin": (0, 0.5, -0.505 - 0.4158),
                "scale": [0.19, 0.19, 0.1],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },
            "R_leg_joint_2": {
                "shape": "sphere",
                "point": (0, 0.5, -2.055 - 0.4158),
                "origin": (0, 0.5, -2.055 - 0.4158),
                "scale": [0.19, 0.19, 0.19],
                "color": Ct.SKIN,
                "initial_rotation": [],
                },

        }

        childList = {            
            "head": ["L_eye_1", "R_eye_1", "hair", "L_ear", "R_ear"],
            "L_eye_1": ["L_eye_2", "L_eye_3"],
            "R_eye_1": ["R_eye_2", "R_eye_3"],

            "neck": ["head"],
            "shoulder": ["neck", "L_arm_1", "R_arm_1"],

            "L_arm_1": ["L_arm_joint_1", "L_arm_2"],
            "L_arm_2": ["L_arm_joint_2", "L_hand"],

            "R_arm_1": ["R_arm_joint_1", "R_arm_2"],
            "R_arm_2": ["R_arm_joint_2", "R_hand"],

            "body": ["shoulder", "pelvis", "skirt", "tail"],
            "core": ["body"],
            "bound": ["core"],

            "pelvis": ["L_leg_1", "R_leg_1"],

            "L_leg_1": ["L_leg_joint_1", "L_leg_2"],
            "L_leg_2": ["L_leg_joint_2", "L_foot"],

            "R_leg_1": ["R_leg_joint_1", "R_leg_2"],
            "R_leg_2": ["R_leg_joint_2", "R_foot"],
        }
        parentDict = {
            "head": "neck",
            "hair": "head",
            "L_ear": "head",
            "R_ear": "head",

            "L_eye_1": "head",
            "L_eye_2": "L_eye_1",
            "L_eye_3": "L_eye_2",
            "R_eye_1": "head",
            "R_eye_2": "R_eye_1",
            "R_eye_3": "R_eye_2",

            "neck": "shoulder",
            "shoulder": "body",
            
            "L_arm_1": "shoulder",
            "L_arm_2": "L_arm_1",
            "L_hand": "L_arm_2",
            "L_arm_joint_1": "L_arm_1",
            "L_arm_joint_2": "L_arm_2",

            "R_arm_1": "shoulder",
            "R_arm_2": "R_arm_1",
            "R_hand": "R_arm_2",
            "R_arm_joint_1": "R_arm_1",
            "R_arm_joint_2": "R_arm_2",

            "body": "core",
            "bound": None,
            "core": "bound",

            "pelvis": "body",
            "skirt": "body",
            "tail": "body",

            "L_leg_1": "pelvis",
            "L_leg_2": "L_leg_1",
            "L_foot": "L_leg_2",
            "L_leg_joint_1": "L_leg_1",
            "L_leg_joint_2": "L_leg_2",

            "R_leg_1": "pelvis",
            "R_leg_2": "R_leg_1",
            "R_foot": "R_leg_2",
            "R_leg_joint_1": "R_leg_1",
            "R_leg_joint_2": "R_leg_2",
        }

        self.speed = 0.01 * 2
        self.direction = Point([random.random()-0.5 for _ in range(3)]).normalize()

        scale = 0.12
        r = 0.911
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = (4.179 + 0.5 * r) * scale
        print(self.bound_center, self.bound_radius)
        self.species_id = 2
        obj = {}
        queue = ["bound"]

        self.components = dict()

        while len(queue):
            part = queue.pop(0)
            parent = parentDict[part]

            if parent == "bound":
                center = ((parts[part]["point"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1] + (0.021+0.3*r))*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2] - 0.47)*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1] + (0.021+0.3*r))*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2] - 0.47)*scale)
            elif parent: 
                center = ((parts[part]["point"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            else:
                center = ((parts[part]["point"][0])*scale, 
                          parts[part]["point"][1] *scale, 
                          (parts[part]["point"][2])*scale)
                origin = ((parts[part]["origin"][0])*scale, 
                          parts[part]["origin"][1]*scale, 
                          (parts[part]["origin"][2])*scale)

            scaling = [val*scale for val in parts[part]["scale"]]
            if parts[part]["shape"] == "cylinder":
                obj[part] = Cylinder(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "cone":
                obj[part] = Cone(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "coneLP":
                obj[part] = Cone(Point(center), shaderProg, scaling, parts[part]["color"], True, origin = Point(origin))
            elif parts[part]["shape"] == "sphere":
                obj[part] = Sphere(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "cube":
                obj[part] = Cube(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "hair":
                obj[part] = Hair(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))

            if "rotation_axis" in parts[part].keys():
                obj[part].changeRotationAxis(*parts[part]["rotation_axis"])
            
            for rotation in parts[part]["initial_rotation"]:
                if rotation["axis"] == "u":
                    # obj[part].rotate(rotation["deg"], obj[part].uAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].uAxis)
                elif rotation["axis"] == "v":
                    # obj[part].rotate(rotation["deg"], obj[part].vAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].vAxis)
                elif rotation["axis"] == "w":
                    # obj[part].rotate(rotation["deg"], obj[part].wAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].wAxis)

            if parent:
                obj[parent].addChild(obj[part])
            else:
                self.addChild(obj[part])

            self.components[part] = obj[part]

            if part in childList:
                for child in childList[part]:
                    queue.append(child)

        self.components["bound"].quat = Quaternion(1, 0, 0, 0)

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints
        
        self.t += 1

        t = self.t % 30

        if t < 10:
            self.components["L_leg_1"].setCurrentAngle(30 - 3 * t, self.components["L_leg_1"].vAxis)
            self.components["L_leg_2"].setCurrentAngle(0, self.components["L_leg_2"].vAxis)
            self.components["L_foot"].setCurrentAngle(30 - 3 * t, self.components["L_foot"].vAxis)
        elif t < 20:
            self.components["L_leg_1"].setCurrentAngle(0, self.components["L_leg_1"].vAxis)
            self.components["L_leg_2"].setCurrentAngle(3 * t - 30, self.components["L_leg_2"].vAxis)
            self.components["L_foot"].setCurrentAngle(0, self.components["L_foot"].vAxis)
        else:
            self.components["L_leg_1"].setCurrentAngle(3 * t - 60, self.components["L_leg_1"].vAxis)
            self.components["L_leg_2"].setCurrentAngle(90 - 3 * t, self.components["L_leg_2"].vAxis)
            self.components["L_foot"].setCurrentAngle(3 * t - 60, self.components["L_foot"].vAxis)

        t = t + 7.5 if t < 22.5 else t - 22.5

        if t < 7.5:
            self.components["L_arm_1"].setCurrentAngle(3 * t, self.components["L_arm_1"].vAxis)
            self.components["L_arm_2"].setCurrentAngle(-22.5 + 3 * t, self.components["L_arm_2"].vAxis)
            self.components["R_arm_1"].setCurrentAngle(-3 * t, self.components["R_arm_1"].vAxis)
            self.components["R_arm_2"].setCurrentAngle(-30 - 3 * t, self.components["R_arm_2"].vAxis)
        elif t < 22.5:
            self.components["L_arm_1"].setCurrentAngle(45 - 3 * t, self.components["L_arm_1"].vAxis)
            self.components["L_arm_2"].setCurrentAngle(22.5 - 3 * t, self.components["L_arm_2"].vAxis)
            self.components["R_arm_1"].setCurrentAngle(-45 + 3 * t, self.components["R_arm_1"].vAxis)
            self.components["R_arm_2"].setCurrentAngle(-67.5 + 3 * t, self.components["R_arm_2"].vAxis)
        else:
            self.components["L_arm_1"].setCurrentAngle(3 * t - 90, self.components["L_arm_1"].vAxis)
            self.components["L_arm_2"].setCurrentAngle(3 * t - 112.5, self.components["L_arm_2"].vAxis)
            self.components["R_arm_1"].setCurrentAngle(-3 * t + 90, self.components["R_arm_1"].vAxis)
            self.components["R_arm_2"].setCurrentAngle(67.5 - 3 * t, self.components["R_arm_2"].vAxis)

        t = t + 7.5 if t < 22.5 else t - 22.5

        if t < 10:
            self.components["R_leg_1"].setCurrentAngle(30 - 3 * t, self.components["R_leg_1"].vAxis)
            self.components["R_leg_2"].setCurrentAngle(0, self.components["R_leg_2"].vAxis)
            self.components["R_foot"].setCurrentAngle(30 - 3 * t, self.components["R_foot"].vAxis)
        elif t < 20:
            self.components["R_leg_1"].setCurrentAngle(0, self.components["R_leg_1"].vAxis)
            self.components["R_leg_2"].setCurrentAngle(3 * t - 30, self.components["R_leg_2"].vAxis)
            self.components["R_foot"].setCurrentAngle(0, self.components["R_foot"].vAxis)
        else:
            self.components["R_leg_1"].setCurrentAngle(3 * t - 60, self.components["R_leg_1"].vAxis)
            self.components["R_leg_2"].setCurrentAngle(90 - 3 * t, self.components["R_leg_2"].vAxis)
            self.components["R_foot"].setCurrentAngle(3 * t - 60, self.components["R_foot"].vAxis)

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        direction = Point((0, 0, 0))
        for component in components:
            if component.species_id == 1:
                temp = component.currentPos - self.currentPos
                if temp.norm() > 0.1 * self.bound_radius and temp.norm() < self.bound_radius + component.bound_radius:
                    # print(temp.norm(), self.name, component.name)
                    self.collision_list += [component]
                    component.collision_list += [self]
                elif temp.norm() < 3.6 * self.bound_radius:
                    direction += temp * (1/temp.norm())

        if len(self.collision_list) != 0:
            self.collide(vivarium)
        elif direction.norm() > 0 and self.ignore_time == 0:
            # print(self.direction)
            self.direction = direction.normalize()

        self.ignore_time = max(0, self.ignore_time - 1)

        # self.speed = 0
        # self.speed = 0.02 + self.t/1000

        # self.direction = Point((np.cos(self.t/300), np.sin(self.t/300), 3**0.5)).normalize()
        nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)

        hitXright = nextPosition.coords[0] > tank_dimensions[0] / 2 - self.bound_radius
        hitXleft = nextPosition.coords[0] < (-tank_dimensions[0] / 2) + self.bound_radius
        hitYtop = nextPosition.coords[1] > tank_dimensions[1] / 2 - self.bound_radius
        hitYbottom = nextPosition.coords[1] < (-tank_dimensions[1] / 2) + self.bound_radius
        hitZfront = nextPosition.coords[2] > tank_dimensions[2] / 2 - self.bound_radius
        hitZback = nextPosition.coords[2] < (-tank_dimensions[2] / 2) + self.bound_radius
        if hitXright or hitXleft:
            self.direction.coords[0] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)
        if hitYtop or hitYbottom:
            self.direction.coords[1] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)
        if hitZfront or hitZback:
            self.direction.coords[2] *= -1
            nextPosition = self.currentPos + self.bound_center + (self.direction * self.speed)
            self.credibility = 100
            # print(self.currentPos, nextPosition.coords)

        nextPosition = self.currentPos + (self.direction * self.speed)
        self.to_q = Quaternion()

        if self.direction.coords[0] >= 0:
            rotation_axis = self.uAxis.cross3d(self.direction).normalize()
            if rotation_axis.norm() == 0:
                rotation_axis = Point((0, 1, 0))

            theta = np.arccos(self.uAxis.dot(self.direction))
            self.to_q = Quaternion(np.cos(theta/2), *([np.sin(theta/2)*val for val in rotation_axis]))
        else:
            u, v, w = self.direction
            theta = theta = np.pi/2
            if v:
                theta = np.arctan((1-u)/v)
            cos_phi = (u-1)/np.sin(theta)**2 + 1
            sin_phi = -w/np.sin(theta)
            if cos_phi > 1:
                cos_phi = 1
            if cos_phi < -1:
                cos_phi = -1
            phi = np.arccos(cos_phi)
            n = Point()

            if sin_phi >= 0:
                n = Point((np.cos(theta), np.sin(theta), 0))
            else:
                n = Point((-np.cos(theta), -np.sin(theta), 0))

            self.to_q = Quaternion(np.cos(phi/2), *([np.sin(phi/2)*val for val in n]))

        # print(self.direction.coords, rotation_axis.coords, q.s, q.v)
        self.slerp()
        self.setCurrentPosition(nextPosition)

    def collide(self, vivarium):
        direction = Point((0, 0, 0))
        for component in self.collision_list:
            if component.species_id == 2:
                self.ignore_time = 30
                direction += (self.currentPos - component.currentPos).normalize()
            elif component.species_id == 1:
                if component in vivarium.components:
                    vivarium.delObjInTank(component)

        if direction.norm() > 0:
            self.direction = direction.normalize()

        self.collision_list = []
        
    def check(self):
        q = self.components["bound"].quat.multiply(self.to_q)

        # print(q.s, q.v)

        if q.s < 0:
            self.to_q.s = -self.to_q.s
            self.to_q.v = [-self.to_q.v[i] for i in range(3)]

    def slerp(self):
        self.check()

        q1 = self.components["bound"].quat.conjugate()
        q2 = self.to_q
        q = Quaternion()
        cos = q1.s * q2.s + Point(q1.v).dot(Point(q2.v))
        if cos > 1:
            cos = 1
        elif cos < -1:
            cos = -1
        theta = np.arccos(cos)

        if theta != 0:
            u = min(np.pi/15/theta, 1)
            q = Quaternion()
            q.s = (np.sin((1-u) * theta) * q1.s + np.sin(u * theta) * q2.s) / np.sin(theta)
            q.v[0] = (np.sin((1-u) * theta) * q1.v[0] + np.sin(u * theta) * q2.v[0]) / np.sin(theta)
            q.v[1] = (np.sin((1-u) * theta) * q1.v[1] + np.sin(u * theta) * q2.v[1]) / np.sin(theta)
            q.v[2] = (np.sin((1-u) * theta) * q1.v[2] + np.sin(u * theta) * q2.v[2]) / np.sin(theta)
            
            p = Quaternion(0, 1, 0, 0)
            p = q.multiply(p.multiply(q.conjugate()))

            # self.direction = Point(p.v)

            q = q.conjugate()
        else:
            q = q1.conjugate()


        self.components["bound"].setQuaternion(q)
        # print(q1.s, q1.v, q.s, q.v, q2.s, q2.v)
        # if u == 0:
            # print(q1.s, q1.v, q.s, q.v, q2.s, q2.v, u)
            # print(self.direction)

class Mochi(Component, EnvironmentObject):
    """
    A Linkage with animation enabled and is defined as an object in environment
    """
    components = None

    def __init__(self, parent, position, shaderProg):
        super(Mochi, self).__init__(position)

        self.collision_list = []
        self.ignore_time = 0

        parts = {
            "mochi": {
                "shape": "sphere",
                "point": (0, 0, 0),
                "scale": [1, 1, 1],
                "color": Ct.WHITE,
                "initial_rotation": [],
                "origin": (0, 0, 0),
                },
        }

        childList = {
        }
        parentDict = {
            "mochi": None,
        }

        scale = 0.04
        r = 0.911
        self.bound_center = Point((0, 0, 0))
        self.bound_radius = r * scale
        # print(self.bound_center, self.bound_radius)
        self.species_id = 3
        obj = {}
        queue = ["mochi"]

        self.components = dict()

        while len(queue):
            part = queue.pop(0)
            parent = parentDict[part]

            if parent == "bound":
                center = ((parts[part]["point"][0]-parts[parent]["point"][0]-0.625)*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1]-(5*(3**0.5)/4+2.1-0.1*r)/2)*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0]-0.625)*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1]-(5*(3**0.5)/4+2.1-0.1*r)/2)*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            elif parent: 
                center = ((parts[part]["point"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            else:
                center = ((parts[part]["point"][0])*scale, 
                          parts[part]["point"][1] *scale, 
                          (parts[part]["point"][2])*scale)
                origin = ((parts[part]["origin"][0])*scale, 
                          parts[part]["origin"][1]*scale, 
                          (parts[part]["origin"][2])*scale)

            scaling = [val*scale for val in parts[part]["scale"]]
            if parts[part]["shape"] == "sphere":
                obj[part] = Sphere(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "cube":
                obj[part] = Cube(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))

            if "rotation_axis" in parts[part].keys():
                obj[part].changeRotationAxis(*parts[part]["rotation_axis"])
            
            for rotation in parts[part]["initial_rotation"]:
                if rotation["axis"] == "u":
                    # obj[part].rotate(rotation["deg"], obj[part].uAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].uAxis)
                elif rotation["axis"] == "v":
                    # obj[part].rotate(rotation["deg"], obj[part].vAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].vAxis)
                elif rotation["axis"] == "w":
                    # obj[part].rotate(rotation["deg"], obj[part].wAxis)
                    obj[part].setDefaultAngle(rotation["deg"], obj[part].wAxis)

            if parent:
                obj[parent].addChild(obj[part])
            else:
                self.addChild(obj[part])

            self.components[part] = obj[part]

            if part in childList:
                for child in childList[part]:
                    queue.append(child)

    def animationUpdate(self):
        ##### TODO 2: Animate your creature!
        # Requirements:
        #   1. Set reasonable joints limit for your creature
        #   2. The linkages should move back and forth in a periodic motion, as the creatures move about the vivarium.
        #   3. Your creatures should be able to move in 3 dimensions, not only on a plane.

        # create periodic animation for creature joints

        ##### BONUS 6: Group behaviors
        # Requirements:
        #   1. Add at least 5 creatures to the vivarium and make it possible for creatures to engage in group behaviors,
        #   for instance flocking together. This can be achieved by implementing the
        #   [Boids animation algorithms](http://www.red3d.com/cwr/boids/) of Craig Reynolds.

        self.update()

    def stepForward(self, components, tank_dimensions, vivarium):

        ##### TODO 3: Interact with the environment
        # Requirements:
        #   1. Your creatures should always stay within the fixed size 3D "tank". You should do collision detection
        #   between the creature and the tank walls. When it hits the tank walls, it should turn and change direction to stay
        #   within the tank.
        #   2. Your creatures should have a prey/predator relationship. For example, you could have a bug being chased
        #   by a spider, or a fish eluding a shark. This means your creature should react to other creatures in the tank.
        #       1. Use potential functions to change its direction based on other creatures’ location, their
        #       inter-creature distances, and their current configuration.
        #       2. You should detect collisions between creatures.
        #           1. Predator-prey collision: The prey should disappear (get eaten) from the tank.
        #           2. Collision between the same species: They should bounce apart from each other. You can use a
        #           reflection vector about a plane to decide the after-collision direction.
        #       3. You are welcome to use bounding spheres for collision detection.

        self.direction = Point((0, max(self.currentPos.coords[1] ** 2 - 4, -1), 0)) * 0.008
        nextPosition = self.currentPos + self.bound_center + self.direction

        hitXright = nextPosition.coords[0] > tank_dimensions[0] / 2 - self.bound_radius
        hitXleft = nextPosition.coords[0] < (-tank_dimensions[0] / 2) + self.bound_radius
        hitYtop = nextPosition.coords[1] > tank_dimensions[1] / 2 - self.bound_radius
        hitYbottom = nextPosition.coords[1] < (-tank_dimensions[1] / 2) + self.bound_radius
        hitZfront = nextPosition.coords[2] > tank_dimensions[2] / 2 - self.bound_radius
        hitZback = nextPosition.coords[2] < (-tank_dimensions[2] / 2) + self.bound_radius
        if hitXright or hitXleft or hitYtop or hitYbottom or hitZfront or hitZback:
            vivarium.delObjInTank(self)

        self.setCurrentPosition(nextPosition)

