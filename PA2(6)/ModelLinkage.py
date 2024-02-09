"""
Model our creature and wrap it in one class.
First version on 09/28/2021

:author: micou(Zezhou Sun)
:version: 2021.2.1

----------------------------------

Modified by Daniel Scrivener 09/2023
"""

from Component import Component
from Point import Point
import ColorType as Ct
from Shapes import Cube
from Shapes import Cone
from Shapes import Cylinder
from Shapes import Sphere
import numpy as np


class ModelLinkage(Component):
    """
    Define our linkage model
    """

    ##### TODO 2: Model the Creature
    # Build the class(es) of objects that could utilize your built geometric object/combination classes. E.g., you could define
    # three instances of the cyclinder trunk class and link them together to be the "limb" class of your creature. 
    #
    # In order to simplify the process of constructing your model, the rotational origin of each Shape has been offset by -1/2 * dz,
    # where dz is the total length of the shape along its z-axis. In other words, the rotational origin lies along the smallest 
    # local z-value rather than being at the translational origin, or the object's true center. 
    # 
    # This allows Shapes to rotate "at the joint" when chained together, much like segments of a limb. 
    #
    # In general, you should construct each component such that it is longest in its local z-direction: 
    # otherwise, rotations may not behave as expected.
    #
    # Please see Blackboard for an illustration of how this behavior works.

    components = None
    contextParent = None

    def __init__(self, parent, position, shaderProg, display_obj=None):
        super().__init__(position, display_obj)
        self.contextParent = parent

        parts = {
            "head": {
                "shape": "sphere",
                "point": (0, 0, 2.8435),
                "scale": [1, 1, 1],
                "color": Ct.SKIN,
                "initial_rotation": [],
                "origin": (0, 0, 1.934),
                },
            "hat": {
                "shape": "sphere",
                "point": (0, 0, 3.682),
                "scale": [1.1, 1.1, 0.6],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": -15, "axis": "v"}],
                "origin": (0, 0, 2.8435),
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
                "color": Ct.WHITE,
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
                "color": Ct.RED,
                "initial_rotation": [],
                "origin": (0, 0, 0.47),
                },
            "core": {
                "shape": "sphere",
                "point": (0, 0, 0.47),
                "scale": [0, 0, 0],
                "color": Ct.RED,
                "initial_rotation": [{"deg": -90, "axis": "u"}, {"deg": -90, "axis": "v"}],
                "origin": (0, 0, 0.47),
                },

            "L_wing_1": {
                "shape": "cylinder",
                "point": (-0.5, 0.25, 1.734),
                "origin": (-0.5, 0.25, 1.15),
                "scale": [0.1, 0.1, 0.6],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -75, "axis": "u"}],
                }, 
            "L_wing_2": {
                "shape": "cylinder",
                "point": (-0.5, 0.25, 2.61),
                "origin": (-0.5, 0.25, 2.318),
                "scale": [0.1, 0.1, 0.3],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": 45, "axis": "u"}],
                }, 
            "L_wing_3": {
                "shape": "cylinder",
                "point": (-0.5, 0.25, 3.865),
                "origin": (-0.5, 0.25, 2.892),
                "scale": [0.1, 0.1, 1],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -70, "axis": "u"}],
                }, 
            "L_wing_tip": {
                "shape": "cone",
                "point": (-0.5, 0.25, 5.045),
                "origin": (-0.5, 0.25, 4.838),
                "scale": [0.095, 0.095, 0.2],
                "color": Ct.BLACK,
                "initial_rotation": [],
                },

            "L_wing_joint_1": {
                "shape": "sphere",
                "point": (-0.5, 0.25, 2.318),
                "origin": (-0.5, 0.25, 2.318),
                "scale": [0.11, 0.11, 0.11],
                "color": Ct.BLACK,
                "initial_rotation": [],
                }, 
            "L_wing_joint_2": {
                "shape": "sphere",
                "point": (-0.5, 0.25, 2.892),
                "origin": (-0.5, 0.25, 2.892),
                "scale": [0.11, 0.11, 0.11],
                "color": Ct.BLACK,
                "initial_rotation": [],
                }, 

            "L_wing_upper_accessory_1": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 1.862),
                "origin": (-0.5, 0.25, 2.318),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.PURPLE,
                "initial_rotation": [{"deg": 30, "axis": "w"}],
                "rotation_axis": [Point([0, 0, 1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "L_wing_upper_accessory_2": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 2.462),
                "origin": (-0.5, 0.25, 2.918),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.BLUE,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, 1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "L_wing_upper_accessory_3": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 3.102),
                "origin": (-0.5, 0.25, 3.558),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.GREEN,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, 1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "L_wing_upper_accessory_4": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 3.742),
                "origin": (-0.5, 0.25, 4.198),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.YELLOW,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, 1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "L_wing_upper_accessory_5": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 4.382),
                "origin": (-0.5, 0.25, 4.838),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.RED,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, 1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },

            "L_wing_lower_accessory_1": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 1.039),
                "origin": (-0.5, 0.25, 1.245),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.PURPLE,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "L_wing_lower_accessory_2": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 1.639),
                "origin": (-0.5, 0.25, 1.845),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.BLUE,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "L_wing_lower_accessory_3": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 2.279),
                "origin": (-0.5, 0.25, 2.485),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.GREEN,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "L_wing_lower_accessory_4": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 2.919),
                "origin": (-0.5, 0.25, 3.125),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.YELLOW,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "L_wing_lower_accessory_5": {
                "shape": "coneLP",
                "point": (-0.5, 0.2886, 3.559),
                "origin": (-0.5, 0.25, 3.765),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.RED,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },

            "R_wing_1": {
                "shape": "cylinder",
                "point": (-0.5, -0.25, 1.734),
                "origin": (-0.5, -0.25, 1.15),
                "scale": [0.1, 0.1, 0.6],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -75, "axis": "u"}, {"deg": 180, "axis": "w"}],
                "rotation_axis": [Point([1, 0, 0]), Point([0, 1, 0]), Point([0, 0, -1])],
                }, 
            "R_wing_2": {
                "shape": "cylinder",
                "point": (-0.5, -0.25, 2.61),
                "origin": (-0.5, -0.25, 2.318),
                "scale": [0.1, 0.1, 0.3],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": 45, "axis": "u"}],
                "rotation_axis": [Point([1, 0, 0]), Point([0, -1, 0]), Point([0, 0, 1])],
                }, 
            "R_wing_3": {
                "shape": "cylinder",
                "point": (-0.5, -0.25, 3.865),
                "origin": (-0.5, -0.25, 2.892),
                "scale": [0.1, 0.1, 1],
                "color": Ct.BLACK,
                "initial_rotation": [{"deg": -70, "axis": "u"}],
                "rotation_axis": [Point([1, 0, 0]), Point([0, 1, 0]), Point([0, 0, -1])],
                }, 
            "R_wing_tip": {
                "shape": "cone",
                "point": (-0.5, -0.25, 5.045),
                "origin": (-0.5, -0.25, 4.838),
                "scale": [0.095, 0.095, 0.2],
                "color": Ct.BLACK,
                "initial_rotation": [],
                },

            "R_wing_joint_1": {
                "shape": "sphere",
                "point": (-0.5, -0.25, 2.318),
                "origin": (-0.5, -0.25, 2.318),
                "scale": [0.11, 0.11, 0.11],
                "color": Ct.BLACK,
                "initial_rotation": [],
                }, 
            "R_wing_joint_2": {
                "shape": "sphere",
                "point": (-0.5, -0.25, 2.892),
                "origin": (-0.5, -0.25, 2.892),
                "scale": [0.11, 0.11, 0.11],
                "color": Ct.BLACK,
                "initial_rotation": [],
                }, 

            "R_wing_upper_accessory_1": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 1.862),
                "origin": (-0.5, -0.25, 2.318),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.PURPLE,
                "initial_rotation": [{"deg": 30, "axis": "w"}],
                "rotation_axis": [Point([0, 0, -1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "R_wing_upper_accessory_2": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 2.462),
                "origin": (-0.5, -0.25, 2.918),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.BLUE,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, -1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "R_wing_upper_accessory_3": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 3.102),
                "origin": (-0.5, -0.25, 3.558),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.GREEN,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, -1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "R_wing_upper_accessory_4": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 3.742),
                "origin": (-0.5, -0.25, 4.198),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.YELLOW,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, -1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },
            "R_wing_upper_accessory_5": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 4.382),
                "origin": (-0.5, -0.25, 4.838),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.RED,
                "initial_rotation": [{"deg": 100, "axis": "w"}],
                "rotation_axis": [Point([0, 0, -1]), Point([0, 1, 0]), Point([1, 0, 0])],
                },

            "R_wing_lower_accessory_1": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 1.039),
                "origin": (-0.5, -0.25, 1.245),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.PURPLE,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "R_wing_lower_accessory_2": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 1.639),
                "origin": (-0.5, -0.25, 1.845),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.BLUE,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "R_wing_lower_accessory_3": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 2.279),
                "origin": (-0.5, -0.25, 2.485),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.GREEN,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "R_wing_lower_accessory_4": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 2.919),
                "origin": (-0.5, -0.25, 3.125),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.YELLOW,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },
            "R_wing_lower_accessory_5": {
                "shape": "coneLP",
                "point": (-0.5, -0.2886, 3.559),
                "origin": (-0.5, -0.25, 3.765),
                "scale": [0.15, 0.15, 0.2],
                "color": Ct.RED,
                "initial_rotation": [{"deg": 180, "axis": "u"}, {"deg": 180, "axis": "w"}],
                },

            "pelvis": {
                "shape": "cone",
                "point": (0, 0, -0.71),
                "origin": (0, 0, -0.71),
                "scale": [0.66, 0.66, 0.2],
                "color": Ct.WHITE,
                "initial_rotation": [{"deg": 180, "axis": "u"}],
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
            "head": ["L_eye_1", "R_eye_1", "hat"],
            "L_eye_1": ["L_eye_2", "L_eye_3"],
            "R_eye_1": ["R_eye_2", "R_eye_3"],

            "neck": ["head"],
            "shoulder": ["neck", "L_arm_1", "R_arm_1"],

            "L_arm_1": ["L_arm_joint_1", "L_arm_2"],
            "L_arm_2": ["L_arm_joint_2", "L_hand"],

            "R_arm_1": ["R_arm_joint_1", "R_arm_2"],
            "R_arm_2": ["R_arm_joint_2", "R_hand"],

            "body": ["shoulder", "pelvis", "L_wing_1", "R_wing_1"],
            "core": ["body"],

            "L_wing_1": ["L_wing_2"],
            "L_wing_2": ["L_wing_joint_1", "L_wing_3", "L_wing_upper_accessory_1"],
            "L_wing_3": ["L_wing_joint_2", "L_wing_tip", "L_wing_upper_accessory_2", "L_wing_upper_accessory_3", "L_wing_upper_accessory_4", "L_wing_upper_accessory_5"],
            "L_wing_upper_accessory_1": ["L_wing_lower_accessory_1"],
            "L_wing_upper_accessory_2": ["L_wing_lower_accessory_2"],
            "L_wing_upper_accessory_3": ["L_wing_lower_accessory_3"],
            "L_wing_upper_accessory_4": ["L_wing_lower_accessory_4"],
            "L_wing_upper_accessory_5": ["L_wing_lower_accessory_5"],

            "R_wing_1": ["R_wing_2"],
            "R_wing_2": ["R_wing_joint_1", "R_wing_3", "R_wing_upper_accessory_1"],
            "R_wing_3": ["R_wing_joint_2", "R_wing_tip", "R_wing_upper_accessory_2", "R_wing_upper_accessory_3", "R_wing_upper_accessory_4", "R_wing_upper_accessory_5"],
            "R_wing_upper_accessory_1": ["R_wing_lower_accessory_1"],
            "R_wing_upper_accessory_2": ["R_wing_lower_accessory_2"],
            "R_wing_upper_accessory_3": ["R_wing_lower_accessory_3"],
            "R_wing_upper_accessory_4": ["R_wing_lower_accessory_4"],
            "R_wing_upper_accessory_5": ["R_wing_lower_accessory_5"],

            "pelvis": ["L_leg_1", "R_leg_1"],

            "L_leg_1": ["L_leg_joint_1", "L_leg_2"],
            "L_leg_2": ["L_leg_joint_2", "L_foot"],

            "R_leg_1": ["R_leg_joint_1", "R_leg_2"],
            "R_leg_2": ["R_leg_joint_2", "R_foot"],
        }
        parentDict = {
            "head": "neck",
            "hat": "head",

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
            "core": None,

            "L_wing_1": "body",
            "L_wing_2": "L_wing_1",
            "L_wing_3": "L_wing_2",
            "L_wing_tip": "L_wing_3",
            "L_wing_joint_1": "L_wing_2",
            "L_wing_joint_2": "L_wing_3",
            "L_wing_upper_accessory_1": "L_wing_2",
            "L_wing_upper_accessory_2": "L_wing_3",
            "L_wing_upper_accessory_3": "L_wing_3",
            "L_wing_upper_accessory_4": "L_wing_3",
            "L_wing_upper_accessory_5": "L_wing_3",
            "L_wing_lower_accessory_1": "L_wing_upper_accessory_1",
            "L_wing_lower_accessory_2": "L_wing_upper_accessory_2",
            "L_wing_lower_accessory_3": "L_wing_upper_accessory_3",
            "L_wing_lower_accessory_4": "L_wing_upper_accessory_4",
            "L_wing_lower_accessory_5": "L_wing_upper_accessory_5",

            "R_wing_1": "body",
            "R_wing_2": "R_wing_1",
            "R_wing_3": "R_wing_2",
            "R_wing_tip": "R_wing_3",
            "R_wing_joint_1": "R_wing_2",
            "R_wing_joint_2": "R_wing_3",
            "R_wing_upper_accessory_1": "R_wing_2",
            "R_wing_upper_accessory_2": "R_wing_3",
            "R_wing_upper_accessory_3": "R_wing_3",
            "R_wing_upper_accessory_4": "R_wing_3",
            "R_wing_upper_accessory_5": "R_wing_3",
            "R_wing_lower_accessory_1": "R_wing_upper_accessory_1",
            "R_wing_lower_accessory_2": "R_wing_upper_accessory_2",
            "R_wing_lower_accessory_3": "R_wing_upper_accessory_3",
            "R_wing_lower_accessory_4": "R_wing_upper_accessory_4",
            "R_wing_lower_accessory_5": "R_wing_upper_accessory_5",

            "pelvis": "body",

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

        scale = 0.5
        obj = {}
        queue = ["core"]

        self.componentList = []
        self.componentDict = dict()

        while len(queue):
            part = queue.pop(0)
            parent = parentDict[part]

            if parent: 
                center = ((parts[part]["point"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["point"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["point"][2]-parts[parent]["point"][2])*scale)
                origin = ((parts[part]["origin"][0]-parts[parent]["point"][0])*scale, 
                          (parts[part]["origin"][1]-parts[parent]["point"][1])*scale, 
                          (parts[part]["origin"][2]-parts[parent]["point"][2])*scale)
            else:
                center = (parts[part]["point"][0]*scale, 
                          parts[part]["point"][1]*scale, 
                          parts[part]["point"][2]*scale)
                origin = (parts[part]["origin"][0]*scale, 
                          parts[part]["origin"][1]*scale, 
                          parts[part]["origin"][2]*scale)

            scaling = [val*scale for val in parts[part]["scale"]]
            if parts[part]["shape"] == "cylinder":
                obj[part] = Cylinder(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "cone":
                obj[part] = Cone(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))
            elif parts[part]["shape"] == "coneLP":
                obj[part] = Cone(Point(center), shaderProg, scaling, parts[part]["color"], True, origin = Point(origin))
            elif parts[part]["shape"] == "sphere":
                obj[part] = Sphere(Point(center), shaderProg, scaling, parts[part]["color"], origin = Point(origin))

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

            self.componentList.append(obj[part])
            self.componentDict[part] = obj[part]

            if part in childList:
                for child in childList[part]:
                    queue.append(child)

        ##### TODO 4: Define creature's joint behavior
        # Requirements:
        #   1. Set a reasonable rotation range for each joint,
        #      so that creature won't intersect itself or bend in unnatural ways
        #   2. Orientation of joint rotations for the left and right parts should mirror each other.

        rotation_limits = {
            "head": [(-30, 30), (-30, 30), (-45, 45)],
            "neck": [(-15, 15), (-15, 15), (-45, 45)],
            "hat": [(0, 0), (0, 0), (0, 0)],
            "core": [(0, 0), (0, 0), (0, 0)],
            "body": [(-360, 360), (-360, 360), (-360, 360)],
            "shoulder": [(0, 0), (0, 0), (-30, 30)],
            "pelvis": [(0 ,0), (0, 0), (-90, 90)],

            "L_arm_1": [(-180, 180), (-180, 180), (0, 0)],
            "L_arm_2": [(-180, 0), (-180, 0), (-90, 90)],
            "L_hand": [(0, 0), (0, 180), (-45, 45)],

            "R_arm_1": [(-180, 180), (-180, 180), (0, 0)],
            "R_arm_2": [(-180, 0), (-180, 0), (-90, 90)],
            "R_hand": [(0, 0), (0, 180), (-45, 45)],

            "L_leg_1": [(-90, 90), (-90, 150), (-90, 90)],
            "L_leg_2": [(-135, 45), (0, 180), (0, 0)],
            "L_foot": [(0, 0), (0, 90), (-45, 45)],

            "R_leg_1": [(-90, 90), (-90, 150), (-90, 90)],
            "R_leg_2": [(-135, 45), (0, 180), (0, 0)],
            "R_foot": [(0, 0), (0, 90), (-45, 45)],

            "L_wing_1": [(-75, 45), (0, 0), (0, 90)],
            "L_wing_2": [(-60, 30), (-90, 90), (0, 0)],
            "L_wing_3": [(-70, 100), (0, 0), (-90, 90)],
            "L_wing_tip": [(0, 0), (0, 0), (0, 0)],

            "R_wing_1": [(-75, 45), (0, 0), (0, 90)],
            "R_wing_2": [(-60, 30), (-90, 90), (0, 0)],
            "R_wing_3": [(-70, 100), (0, 0), (-90, 90)],
            "R_wing_tip": [(0, 0), (0, 0), (0, 0)],

            "L_wing_upper_accessory_1": [(-360, 360), (0, 0), (-75, 105)],
            "L_wing_upper_accessory_2": [(-360, 360), (0, 0), (-105, 75)],
            "L_wing_upper_accessory_3": [(-360, 360), (0, 0), (-105, 75)],
            "L_wing_upper_accessory_4": [(-360, 360), (0, 0), (-105, 75)],
            "L_wing_upper_accessory_5": [(-360, 360), (0, 0), (-105, 75)],

            "R_wing_upper_accessory_1": [(-360, 360), (0, 0), (-75, 105)],
            "R_wing_upper_accessory_2": [(-360, 360), (0, 0), (-105, 75)],
            "R_wing_upper_accessory_3": [(-360, 360), (0, 0), (-105, 75)],
            "R_wing_upper_accessory_4": [(-360, 360), (0, 0), (-105, 75)],
            "R_wing_upper_accessory_5": [(-360, 360), (0, 0), (-105, 75)],

            "L_wing_lower_accessory_1": [(0, 0), (0, 0), (0, 0)],
            "L_wing_lower_accessory_2": [(0, 0), (0, 0), (0, 0)],
            "L_wing_lower_accessory_3": [(0, 0), (0, 0), (0, 0)],
            "L_wing_lower_accessory_4": [(0, 0), (0, 0), (0, 0)],
            "L_wing_lower_accessory_5": [(0, 0), (0, 0), (0, 0)],

            "R_wing_lower_accessory_1": [(0, 0), (0, 0), (0, 0)],
            "R_wing_lower_accessory_2": [(0, 0), (0, 0), (0, 0)],
            "R_wing_lower_accessory_3": [(0, 0), (0, 0), (0, 0)],
            "R_wing_lower_accessory_4": [(0, 0), (0, 0), (0, 0)],
            "R_wing_lower_accessory_5": [(0, 0), (0, 0), (0, 0)],

            "L_arm_joint_1": [(0, 0), (0, 0), (0, 0)],
            "L_arm_joint_2": [(0, 0), (0, 0), (0, 0)],
            "R_arm_joint_1": [(0, 0), (0, 0), (0, 0)],
            "R_arm_joint_2": [(0, 0), (0, 0), (0, 0)],
            "L_wing_joint_1": [(0, 0), (0, 0), (0, 0)],
            "L_wing_joint_2": [(0, 0), (0, 0), (0, 0)],
            "R_wing_joint_1": [(0, 0), (0, 0), (0, 0)],
            "R_wing_joint_2": [(0, 0), (0, 0), (0, 0)],
            "L_leg_joint_1": [(0, 0), (0, 0), (0, 0)],
            "L_leg_joint_2": [(0, 0), (0, 0), (0, 0)],
            "R_leg_joint_1": [(0, 0), (0, 0), (0, 0)],
            "R_leg_joint_2": [(0, 0), (0, 0), (0, 0)],
        }

        for part, limit in rotation_limits.items():
            obj[part].setRotateExtent(obj[part].uAxis, obj[part].default_uAngle + limit[0][0], obj[part].default_uAngle + limit[0][1])
            obj[part].setRotateExtent(obj[part].vAxis, obj[part].default_vAngle + limit[1][0], obj[part].default_vAngle + limit[1][1])
            obj[part].setRotateExtent(obj[part].wAxis, obj[part].default_wAngle + limit[2][0], obj[part].default_wAngle + limit[2][1])

