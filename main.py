#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import time

# OBJECTS CREATIONS
ev3 = EV3Brick()
left_motor = Motor(Port.A)
right_motor = Motor(Port.D)
mini_motor = Motor(Port.C)
gs = GyroSensor(Port.S3)
cl = ColorSensor(Port.S4)
angular_velocity = 500
color_list = []

# DISTANCES
x = 1.7
x1 = 0.6
x2 = x - x1
x3 = 0.65
y = 0.7
dist_block = 0.3

# FUNCTIONS
def introduce_colors():
    print(color_list)
    while len(color_list) < 3:
        if cl.color() == Color.YELLOW or cl.color() == Color.RED or cl.color() == Color.GREEN or cl.color() == Color.BLUE:
            color_list.append(cl.color())
            ev3.speaker.say(str(cl.color()))
            ev3.speaker.say('color added')
            print(color_list)
            time.sleep(1)
        else:
            ev3.speaker.say('color not good')
    return color_list


def drive_forwards(angular_velocity, time):
    right_motor.run_time(speed = angular_velocity, time = time, wait = False)
    left_motor.run_time(speed = angular_velocity, time = time, wait = True)


def drive_backwards(angular_velocity, time):
    right_motor.run_time(speed = -angular_velocity, time = time, wait = False)
    left_motor.run_time(speed = -angular_velocity, time = time, wait = True)

def check_color():
    color_detected = cl.color()
    if color_detected == color_list[0]:
        #print(f'color detected: {color_detected}')
        color_list.remove(color_detected)
        return True
    else:
        return False 
    
    
# this function calculates the time needed to drive trought the axis
def calculate_time(x, angular_velocity):
    radio = 0.0275 # wheels radio in m
    
    angular_velocity_radians = angular_velocity * math.pi / 180
    linear_velocity = radio * angular_velocity_radians
    
    time = (float(x) / linear_velocity) * 1000 # time in ms that the robot has to drive in the x axis
    #time = (float(x) / angular_velocity) * 20000
    return time


# this fuction makes the robot turn
def turn(direction, angle):
    gs.reset_angle(0)
    if direction == 'l':
        angle = 0 - angle
        start_angle = gs.angle()
        left_motor.run(-100)
        right_motor.run(100)
        while gs.angle() - start_angle > angle:
            pass
        left_motor.hold()
        right_motor.hold()
        time.sleep(1)
        angulo1 = gs.angle() - start_angle
        print(gs.angle() - start_angle)
        gs.reset_angle(0)
        if angulo1 != angle:
            if angulo1 < angle:
                left_motor.run(20)
                right_motor.run(-20)
                while gs.angle() < angle - angulo1:
                    pass
                left_motor.hold()
                right_motor.hold()
                time.sleep(1)
            elif angulo1 > angle:
                left_motor.run(-20)
                right_motor.run(20)
                while -gs.angle() < angle + angulo1:
                    pass
                left_motor.hold()
                right_motor.hold()
                time.sleep(1)
        print(gs.angle())
        
    elif direction == 'r':
        start_angle = gs.angle()
        left_motor.run(100)
        right_motor.run(-100)
        while gs.angle() - start_angle < angle:
            pass
        left_motor.hold()
        right_motor.hold()
        time.sleep(1)
        angulo1 = gs.angle() - start_angle
        print(gs.angle() - start_angle)
        gs.reset_angle(0)
        if angulo1 != angle:
            if angulo1 < angle:
                left_motor.run(20)
                right_motor.run(-20)
                while gs.angle() < angle - angulo1:
                    pass
                left_motor.hold()
                right_motor.hold()
                time.sleep(1)
            elif angulo1 > angle:
                left_motor.run(-20)
                right_motor.run(20)
                while gs.angle() < angle - angulo1:
                    pass
                left_motor.hold()
                right_motor.hold()
                time.sleep(1)
        print(gs.angle())
     
        
def drive_station(t_x, t_y):
    right_motor.run_time(speed = angular_velocity, time = t_x, wait = False)
    left_motor.run_time(speed = angular_velocity, time = t_x, wait = True)
    left_motor.hold()
    right_motor.hold()
    time.sleep(1)
    turn('l', 90)
    time.sleep(1)
    left_motor.hold()
    right_motor.hold()
    time.sleep(1) 
    right_motor.run_time(speed = angular_velocity, time = t_y, wait = False)
    left_motor.run_time(speed = angular_velocity, time = t_y, wait = True)
        
        
def drive_home(t_x, t_y):
    right_motor.run_time(speed = -angular_velocity, time = t_y, wait = False)
    left_motor.run_time(speed = -angular_velocity, time = t_y, wait = True)
    left_motor.hold()
    right_motor.hold()
    time.sleep(1)
    turn('l', 90)
    time.sleep(1)
    left_motor.hold()
    right_motor.hold()
    time.sleep(1)
    right_motor.run_time(speed = angular_velocity, time = t_x, wait = False)
    left_motor.run_time(speed = angular_velocity, time = t_x, wait = True)


def grab_block():
    print('grabbing block')
    mini_motor.run_time(speed = -100, time = 1500)
    
    
def leave_block():
    print('leaving block')
    mini_motor.run_time(speed = 100, time = 1500)
    
    
def block_area1(t_dist_block):
    count = 1
    block_found = False
    while block_found == False and count < 5:
        drive_forwards(angular_velocity, t_dist_block)
        count = count + 1
        time.sleep(2)
        color = check_color()
        if color:
            drive_backwards(angular_velocity, 500)
            turn('l', 90)
            drive_forwards(angular_velocity, 1000)
            grab_block()
            drive_backwards(angular_velocity, 1000)
            turn('r', 90)
            block_found = True
            
        else:
            pass
    for i in range(count-1): 
        drive_backwards(angular_velocity, t_dist_block)


def block_area2(t_dist_block):
    count = 1
    block_found = False
    while block_found == False and count < 5:
        drive_backwards(angular_velocity, t_dist_block)
        count = count + 1
        time.sleep(2)
        color = check_color()
        if color:
            drive_backwards(angular_velocity, 500)
            turn('l', 90)
            drive_forwards(angular_velocity, 1000)
            grab_block()
            drive_backwards(angular_velocity, 1000)
            turn('r', 90)
            block_found = True
        else:
            pass
    for i in range(count-1): 
        drive_forwards(angular_velocity, t_dist_block)

# MAIN CODE
ev3.speaker.beep()

t_x = calculate_time(x, angular_velocity)
t_y = calculate_time(y, angular_velocity)
t_x1 = calculate_time(x1, angular_velocity)
t_x2 = calculate_time(x2, angular_velocity)
t_x3 = calculate_time(x3, angular_velocity)
t_dist_block = calculate_time(dist_block, angular_velocity)


leave_block()
introduce_colors()
drive_forwards(angular_velocity, t_x1)
turn('r', 90)
block_area1(t_dist_block)
turn('l', 90)
drive_station(t_x2, t_y)
leave_block()
drive_home(t_x3, t_y)
turn('r', 90)
block_area2(t_dist_block)
turn('r', 90)
drive_station(t_x3, t_y)
leave_block()
drive_home(t_x3, t_y)
turn('r', 90)
block_area2(t_dist_block)
turn('r', 90)
drive_station(t_x3, t_y)
leave_block()
drive_home(t_x, t_y)

ev3.speaker.beep()
