Name: Mutiraj Laksanawisit (U44887379)
Collaborators: None
Class: CAS CS 480
Programming Assignment 2: 3D Modeling & Transformations

Summary:

TODO 1: Use XYZ Euler

Pre TODO 2: 

In "Shapes.py"; Change "limb" variable for "origin" (as used in Blender). If origin is None, we assume that the part is a limb and put the origin at the end of the shape.

center refers to the translational origin of the shape and origin refers to the rotational origin of the shape.

TODO 2:

Main Variable Used:

	parts: A dictionary which the key is the part's name (eg. head, neck, L_arm_1) and the value is another dictionary which contains information about the part.

	parts' value: A dictionary that contains shape, point (center), origin, scale, color, initial_rotation (Default Angle), and rotation_axis (If needed) of the part. The value of shape, point, origin, scale, and initial_rotation is the same as one in Reference/Flandre.blend

	core in parts: core is the component of the model that has no size. It's only purpose is to rotate the axis from Blender to line up with the axis from python.

	childList: A dictionary which the key is the part's name and the value is the list of that part's children's name. The part that has no child will not be a key in this dictionary.

	parentDict: A dictionary which the key is the part's name and the value is the part's parent's name. core's parent is None.

	scale: A global scaling that is applied to all parts. Use for quick scaling of the model.

	obj: A dictionary which the key is the part's name and the value is that part's object from Shape.py

	queue: A queue in which we define the model using BFS from the core of the model.

Extra Info:

	A numbered parts are indexed based on how far they are from the core of the model. For example L_arm_1 is closer to the core than L_arm_2.

TODO 3: N/A

TODO 4:

Main Variable Used:

	rotation_limits: A dictionary which the key is the part's name and the value is the part's rotational limit in form of [(neg_u_lim, pos_u_lim), (neg_v_lim, pos_v_lim), (neg_w_lim, pos_w_lim)]. The limit of the rotation for u-axis will be default_u_angle + neg_u_lim and default_u_angle + pos_u_lim. The same goes for v and w-axis too!

TODO 5:

Multi-Select:

	Main Variable Used:

		select_obj_parts: A list containing the parts that are selected.

		keybinds: A dictionary where the key is the keybind and the value is the corresponding components. (The keybinds will be presented in the last section of this README.

	Minor Changes to existing variables/ methods:

		select_color is now softred, softgreen, and softblue to avoid having the same color as some components.

		Pressing "R" no longer reset the axis of the component.

		Interrupt_Scroll is now support multi-select feature

Test Case:

	Main Variable Used:
		
		test_case_index: store the index of the current test case (0 - 5 where 0 is default).

		test_cases: A list of dictionaries where each dictionary contains the info of the test case (The 0th test case is empty).
		
		test_cases' dictionary: A dictionary which the key is the part's name and the value is the rotation angle in u, v, and w-axis respectively. The rotation angle is applied after the inital_rotation (default angle)

	The reference for each test case is located in the Reference folder.

TODO 6:

	Main Variable Used:

		x,  y: the location of the mouse

		size_x, size_y: the size of the window

		default_eye_direction: a unit vector that represents the default direction of the eyes

		current_mouse_direction: a unit vector that represents the direction of mouse with respect to the center of the screen

		rotation_axis: a unit vector that represents the direction of the rotational axis. Its direction is the same as the cross product of default_eye_direction and current_mouse_direction

		sin_eye, cos_eye: a sine and cosine value of the angle of rotation respectively.

		sin_half_eye, cos_half_eye: a sine and cosine value of half the angle of rotation respectively.

		eye_Quaternion: a quaternion that represents the rotation of the eyes.

Extra:

	Keybinds:

If possible, the uppercase version of the keybinds are binding to the right-side components

"a": ["body"],
"b": ["shoulder"],
"c": ["neck"],
"d": ["head"],
"e": ["L_arm_1"],
"f": ["L_arm_2"],
"g": ["L_hand"],
"h": ["pelvis"],
"i": ["L_leg_1"],
"j": ["L_leg_2"],
"k": ["L_foot"],
"l": ["L_wing_1"],
"m": ["L_wing_2"],
"n": ["L_wing_3"],
"u": ["L_wing_upper_accessory_1", "L_wing_lower_accessory_1"], 
"v": ["L_wing_upper_accessory_2", "L_wing_lower_accessory_2"], 
"w": ["L_wing_upper_accessory_3", "L_wing_lower_accessory_3"], 
"x": ["L_wing_upper_accessory_4", "L_wing_lower_accessory_4"], 
"y": ["L_wing_upper_accessory_5", "L_wing_lower_accessory_5"], 



