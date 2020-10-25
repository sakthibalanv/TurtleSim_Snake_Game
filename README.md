# TurtleSim Snake Game

This is a fun implementation of the classic snake game on the turtlesim simulator used to learn Robot operating system (ROS). 

This game uses the **turtlesim** and **turtlesim_teleop** packages to move a **snake turtle** in order to capture the **target turtle**, upon catching the target turtle, a new turtle appears in the screen as the new target and the captured turtle will now be a part of the snake turtle. This process repeats with every capture of the target turtle.

![](data/turtle_snake_gif2.gif)



## Usage

To run the game, clone the package in your catkin workspace, and use the launch file below.

```console
cd ~/catkin_ws/src
git clone https://github.com/sakthibalanv/TurtleSim_Snake_Game.git
cd ~/catkin_ws
catkin_make
source devel/setup.bash
```



```console
roslaunch turtle_snake_game start.launch
```



## ROS Node Graph

![](data/rosgraph1.png)



## Missing Features

* It would be nice to add a collision feature on the snake, like if it self collides or collides with the wall then the game is over.
* Add obstacles for the snake like barriers.
* Speed up the snake every time it eats a turtle, to make it difficult for the players.



## Note

Contributions to improving the existing code or new features and ideas are most welcome.



## Version

Version 1.0.0



## Video Links

### Demo

[![Turtle Snake Game Demo](http://img.youtube.com/vi/ALQ7u93EEtw/0.jpg)](https://www.youtube.com/watch?v=ALQ7u93EEtw)

