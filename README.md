# TurtleSim Snake Game

This is a fun implementation of the classic snake game on the turtlesim simulator used to learn Robot operating system (ROS). 

This game uses the **turtlesim** and **turtlesim_teleop** packages to move a **snake turtle** in order to capture the **target turtle**, upon catching the target turtle, a new turtle appears in the screen as the new target and the captured turtle will now be a part of the snake turtle. This process repeats with every capture of the target turtle.

![](data/turtlesim_snake_game.gif)

## Usage

To run the game, clone the package in your catkin workspace, and use the launch file below.

```console
roslaunch turtle_snake_game start.launch
```



## ROS Node Graph

![](data/rosgraph1.png)

