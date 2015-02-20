Spaceship Artificial Intelligence
=================================

This models two fighting spaceships in a field of obstacles. 

**Run `main.py` to start.**

The two spaceships will fly around avoiding each other and other obstacles as well as avoiding going too far off the map. One day I may extend this to make the spaceships actually shoot each other and perform other more interesting tasks as well. 

It would be very interesting to see if the spaceships can be made to go on certain paths perhaps trying to fight each other while also playing for a certain goal.

**Note:** The script ray tracing is not very sophisticated. It does not account for any bounding boxes and treats every object as a point only. Thus it may look like the spaceships are running into obstacles when in fact they are avoiding them entirely. I didn't want to render the spaceships or the obstacles too small, but the smaller they are, the more they will resemble the way I'm modeling them.

![Spaceship AI](http://i.imgur.com/C761Lg3.png)

The **RED** line is the ray being cast by the spaceship. The **BLUE** line is the desired angle calculated by the AI based on the obstacles in its way. 

