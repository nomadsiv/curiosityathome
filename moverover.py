#!/usr/bin/env python

# Lego Rover running on JSON
# coded by Jurgen van der Vlist
# for NASA SpaceApps Challenge 2013

import thread
import nxt.locator
import math
from nxt.sensor import *
from nxt.motor import *
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="read GCode from file", metavar="FILE")
(options, args) = parser.parse_args()

nxt_scale = 1


def move_motor(motor, speed, degrees):
    direction = 0
    if degrees < 0:
        direction = -1
    else:
        direction = 1
    if direction != 0:
        motor.turn(direction * speed, nxt_scale * abs(degrees))


def move_rover(speed, x, y):
    thread.start_new_thread(move_motor, (motor_x, speed, x))
    thread.start_new_thread(move_motor, (motor_y, speed, y))
    
def distance_on_mars_in_meters(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi/180.0
        
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
        
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
        
    # Compute spherical distance from spherical coordinates.
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
    return arc * 338.6 # multiply by mars' radius to get meters
    

def file_to_list():
    if options.filename:
        print "opening file " + str(options.filename)
        try:
            f = open(options.filename, 'r')
            return [i for i in f.readlines()]

        except Exception, e:
            print "file error " + str(e)
    else:
        print "Nothing to read. Please enter a filename with the -f option"


def main():
    positions = file_to_list()
    if positions:
        # print positions
        # origin = positions[0]
        print "moving rover test"
        # move_rover(100, 100, 100)
        move_motor(motor_x, 10, 100)
        move_motor(motor_y, 10, 300)
        # move_motor(motor_x, 100, 100)
        # for position in positions[1:]:
        #   move_rover(10, 100, 10)
    else:
        print "no positions found"

try:
    b = nxt.locator.find_one_brick()
    motor_x = Motor(b, PORT_A)
    motor_y = Motor(b, PORT_B)
    motor_z = Motor(b, PORT_C)
    main()
except Exception, e:
    print "please connect a Brick, or install Ubuntu"

