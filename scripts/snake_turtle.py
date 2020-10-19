#!/usr/bin/env python

import rospy
from turtlesim.msg import Pose
from turtlesim.srv import Spawn
from turtlesim.srv import SetPen
from geometry_msgs.msg import Twist
from geometry_msgs.msg import TransformStamped
import random
import math

turtle1_pose = Pose()
turtlelist = []
lastTurtle = 1
nextturtleIndex = 1

class mySpawner:
    def __init__(self, tname):
        self.turtle_name = tname
        self.state = 1
        rospy.wait_for_service('/spawn')
        try:
            client = rospy.ServiceProxy('/spawn', Spawn)
            x = random.randint(1, 10)
            y = random.randint(1, 10)
            theta = random.uniform(1, 3.14)
            name = tname
            _nm = client(x, y, theta, name)
            rospy.loginfo("Turtle Created [%s] [%f] [%f]", name, x, y)
            rospy.Subscriber(self.turtle_name + '/pose', Pose, self.turtle_poseCallback)
            self.pub = rospy.Publisher(self.turtle_name + '/cmd_vel', Twist, queue_size=10)
            self.turtle_to_follow = 1
            self.turtle_pose = Pose()
            rospy.wait_for_service("/" + tname + '/set_pen')
            try:
                client = rospy.ServiceProxy("/" + tname + '/set_pen', SetPen)
                client(0,0,0,0,1)
            except rospy.ServiceException as e:
                print("Service call failed: %s"%e)
        except rospy.ServiceException as e:
            print("Service tp spawn a turtle failed. %s", e)
    
    def turtle_poseCallback(self, data):
        self.turtle_pose = data
    
    def turtle_velocity(self, msg):
        self.pub.publish(msg)


def turtle1_poseCallback(data):
    global turtle1_pose
    global lastTurtle
    global turtlelist
    global nextturtleIndex
    turtle1_pose.x = round(data.x, 4)
    turtle1_pose.y = round(data.y, 4)
    turtle1_pose.theta = round(data.theta, 4)

    for i in range(len(turtlelist)):
        twist_data = Twist()
        diff = math.sqrt(pow((turtle1_pose.x - turtlelist[i].turtle_pose.x) , 2) + pow((turtle1_pose.y - turtlelist[i].turtle_pose.y), 2))
        ang = math.atan2(turtle1_pose.y - turtlelist[i].turtle_pose.y, turtle1_pose.x - turtlelist[i].turtle_pose.x) - turtlelist[i].turtle_pose.theta
        
        if(ang <= -3.14) or (ang > 3.14):
            ang = ang / math.pi

        if (turtlelist[i].state == 1):
            if diff < 1.0:
                turtlelist[i].state = 2
                turtlelist[i].turtle_to_follow = lastTurtle
                lastTurtle = i + 2
                rospy.loginfo("Turtle Changed [%s] [%f] [%f]", turtlelist[i].turtle_name, diff, ang)
                nextturtleIndex += 1
                turtlelist.append(mySpawner("turtle" + str(nextturtleIndex)))
        else:
            parPose = turtle1_pose
            if(turtlelist[i].turtle_to_follow != 1):
                parPose = turtlelist[turtlelist[i].turtle_to_follow - 2].turtle_pose
            
            diff = math.sqrt(pow((parPose.x - turtlelist[i].turtle_pose.x) , 2) + pow((parPose.y - turtlelist[i].turtle_pose.y), 2))
            goal = math.atan2(parPose.y - turtlelist[i].turtle_pose.y, parPose.x - turtlelist[i].turtle_pose.x)
            ang = math.atan2(math.sin(goal - turtlelist[i].turtle_pose.theta), math.cos(goal - turtlelist[i].turtle_pose.theta))

            if(ang <= -3.14) or (ang > 3.14):
                ang = ang / (2*math.pi)
            
            if(diff < 0.8):
                twist_data.linear.x = 0 
                twist_data.angular.z = 0
            else:
                twist_data.linear.x = 2.5 * diff                
                twist_data.angular.z = 20 * ang
                  
            turtlelist[i].turtle_velocity(twist_data)
            turtlelist[i].oldAngle = ang    

 

def spawn_turtle_fn():
    global nextturtleIndex
    rospy.init_node('snake_turtle', anonymous=True)
    rospy.Subscriber('/turtle1/pose', Pose, turtle1_poseCallback)
    rospy.wait_for_service("/turtle1/set_pen")
    try:
        client = rospy.ServiceProxy('/turtle1/set_pen', SetPen)
        client(0,0,0,0,1)
    except rospy.ServiceException as e:
        print("Service call failed: %s"%e)
    
    nextturtleIndex += 1
    turtlelist.append(mySpawner("turtle" + str(nextturtleIndex)))
    # for i in range(2,10):
    #     turtlelist.append(mySpawner("turtle" + str(i)))
        
    rospy.spin()

if __name__ == "__main__":
    spawn_turtle_fn()