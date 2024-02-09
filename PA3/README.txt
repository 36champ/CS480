Name: Mutiraj Laksanawisit (U44887379)
Collaborators: None
Class: CAS CS 480
Programming Assignment 3: 3D Vivarium

Summary:

TODO 1: Predator/Prey Models

Predator: Tewi Inaba (Tewi Class)
Prey: Earth Rabbit (Rabbit Class)
Food: Mochi (Mochi Class)

Press "p" to spawn in a Rabbit

TODO 2: Model animation

Predator: Walking Animation (Constant Speed)
Prey: Jump Animation (Non-Constant Speed)
Food: No Animation (Non-Constant Speed)

TODO 3: Collision Detection & Reaction

Predator-Prey Collision: Predator eats Prey
Prey-Prey Collision: Bounce off each other and ignore all potential function for 30 frames
Prey-Food Collision: Prey eats Food

Predator-Prey Reaction: Predator chases Preys and Preys evade Predator using potential function. Predator has more sight than Preys so sometimes Predator will notice the Preys but not the other way around. To compensate, Preys are faster than Predator on average.
Prey-Food Reaction: Preys are attacted to food if they can see the food. This potential function is stronger than that of the flock behavior but weaker than that of the Predator evasion.

TODO 4: Creature orientation

Using SLERP with a limit of 12 degrees of rotation per frame

TODO 5: Feed your creatures with food

Food is spawned at y = 1.8 and falls down with the increasing speed before reaching its terminal velocity and then slows down as it approaches the bottom of the tank

TODO 6: Flocking behavior

If two rabbits are close to each other, their direction influences each other. Credibility defines how much weigh the direction is. Rabbit gains credibility by running into the wall so that it is only the rabbit in the flock that run into the wall.

EXTRA: Fun Facts

Tewi Inaba (因幡　てゐ Inaba Tewi) is the leader of the many youkai rabbits that live at and guard Eientei. She is also considered to be the leader of all the earth rabbits; it's said that there is not a single youkai rabbit unknown to her, and that all of them will only ever listen to her.

In the Touhou Project, Rabbits (兎 usagi) living in Gensokyo seem to be able to cast attack magic naturally. Also, a rabbit can become a type of youkai after existing for a long period of time, gaining sentience and increased abilities in the process.