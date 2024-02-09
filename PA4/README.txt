Name: Mutiraj Laksanawisit (U44887379)
Collaborators: None
Class: CAS CS 480
Programming Assignment 4: Shaded Rendering

Summary:

TODO 1: Generate Triangle Meshes

Each Displayable class is in its own python file named the same as the class.

TODO 2: Normal Rendering

Can be seen in SceneTwo

TODO 3: Illuminate Your Meshes

Is combined with TODO 4

TODO 4: Set Up Lights

Add another parameter in Light struct, lightOn, which indicate whether a specific light is on or off.

Add new parameters 'isAmbient', 'isDiffuse', 'isSpecular' to indicate whether ambient, diffuse, and specular will be shown or not.

Can be seen in SceneFive

Keybind:
'a, A': Toggle Ambient
'd, D': Toggle Diffuse
's, S': Toggle Specular

TODO 5: Create Your Scenes

The scenes are [SceneOne, SceneTwo, SceneFive, SceneThree, SceneFour].

Keybind:
Left Arrow: Previous Scene
Right Arrow: Next Scene
',' or '<': Previous Light
'.' or '>: Next Light
'l' or 'L': Toggle Light

TODO 6: Texture Mapping

Can be seen in SceneThree

TODO 7: Normal Mapping

Can be seen in SceneFour



Extra: Scene Description

SceneOne: Default Scene

SceneTwo: Normal Mapping (No Lighting at all)

SceneFive: Lighting
Lights are [Point Light at (0, 0, 1), Back Infinite Light]

SceneThree: Texture Mapping (With Lighting)
Lights are [Red Point Light at (0, 2, 0), Small Blue Spotlight at (0, -2, 0), Infinite Orange Light]

SceneFour: Normal Mapping (With Lighting)
Lights are [Soft Red Point Light at (0, 2, 0), Medium - Large Soft Blue Spotlight at (0, -2, 0), Front Infinite Light, Back Infinite Light]
