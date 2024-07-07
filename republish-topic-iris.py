#! /usr/bin/python3.8
from rospy import init_node, loginfo, Publisher, Rate, Subscriber, spin, ROSInterruptException
from threading import Thread
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from time import time

# Initializations
t_period = .005
t_prev = time()

motor_vel = Float32MultiArray()         # defining  variable
motor_vel.data = [0,0,0,0]              # Initialize motor_vel

motor_vel_simulink = Twist()              #  defining  variable

init_node('republish_node', anonymous=True)        # initialized the current node
loginfo("Creating node to republish topics")        # Print through ROS

pub_motor_vel = Publisher('/iris/cmd/motor_vel', Float32MultiArray, queue_size=1)


def send_motor_vel():                               # def of a function
    global motor_vel, motor_vel_simulink

    motor_vel.data = [motor_vel_simulink.linear.x,
                      motor_vel_simulink.linear.y,
                      motor_vel_simulink.linear.z,
                      motor_vel_simulink.angular.x]

    pub_motor_vel.publish(motor_vel)

def listen():                                          # ??
    Rate(100) 
    Subscriber('/iris/cmd_simulink/motor_vel', Twist, callback_motor_vel, queue_size=1)
    spin()
    
def callback_motor_vel(data):                         # 
    global motor_vel_simulink

    motor_vel_simulink = data
    pass

if __name__ == '__main__':
    try:
        thread_listen = Thread(target=listen)
        thread_listen.start()
        
        while True:
            try:
                if (time() - t_prev) < t_period:
                    pass
                else:
                    send_motor_vel()
                    t_prev = time()
            except KeyboardInterrupt:
                thread_listen.join()
                pass

    except ROSInterruptException:
        pass