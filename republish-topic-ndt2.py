#! /usr/bin/python3.8
from rospy import init_node, loginfo, Publisher, Rate, Subscriber, spin, ROSInterruptException
from threading import Thread
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from time import time

t_period = .01
t_prev = time()

motor_vel = Float32MultiArray()
motor_vel.data = [0,0,0,0,0,0,0,0]

motor_vel_up_simulink = Twist()
motor_vel_down_simulink = Twist()

init_node('republish_node', anonymous=True)
loginfo("Creating node to republish topics")

pub_motor_vel = Publisher(
    '/ndt2/cmd/motor_vel', Float32MultiArray, queue_size=1)

def send_motor_vel():
    global motor_vel, motor_vel_up_simulink, motor_vel_down_simulink

    motor_vel.data = [motor_vel_up_simulink.linear.x,
                      motor_vel_up_simulink.linear.y,
                      motor_vel_up_simulink.linear.z,
                      motor_vel_up_simulink.angular.x,
                      motor_vel_down_simulink.linear.x,
                      motor_vel_down_simulink.linear.y,
                      motor_vel_down_simulink.linear.z,
                      motor_vel_down_simulink.angular.x]

    pub_motor_vel.publish(motor_vel)

def listen():
    Rate(100)
    Subscriber('/ndt2/cmd_simulink/motor_vel_up', Twist, callback_motor_vel_up, queue_size=1)
    Subscriber('/ndt2/cmd_simulink/motor_vel_down', Twist, callback_motor_vel_down, queue_size=1)
    spin()
    
def callback_motor_vel_up(data):
    global motor_vel_up_simulink

    motor_vel_up_simulink = data
    pass

def callback_motor_vel_down(data):
    global motor_vel_down_simulink

    motor_vel_down_simulink = data
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