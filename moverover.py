#!/usr/bin/env python

# Lego Rover running on JSON
# coded by Jurgen van der Vlist
# for NASA SpaceApps Challenge 2013

import thread
import nxt.locator
import math
import json
import pprint
import time
from nxt.sensor import *
from nxt.motor import *
from optparse import OptionParser


parser = OptionParser()
parser.add_option("-f", "--file", dest="filename",
                  help="read GCode from file", metavar="FILE")
(options, args) = parser.parse_args()

nxt_scale = 0.2


def move_motor(motor, speed, degrees):
    direction = 0
    if degrees < 0:
        direction = -1
    else:
        direction = 1
    if direction != 0:
        motor.turn(direction * speed, nxt_scale * abs(degrees))


def move_rover(start_position, target_position):
    distance = distance_on_mars_in_meters(start_position["x"], start_position["y"], target_position["x"], target_position["y"])
    try:
        print "move from " + str(start_position) + " to " + str(target_position)
        motor_x.turn(10, nxt_scale * abs(360 * distance))
        time.sleep(.5)
    except Exception, e:
        print "Motor X failed " + str(e)
    # thread.start_new_thread(move_motor, (motor_x, speed, x))
    # thread.start_new_thread(move_motor, (motor_y, speed, y))

def distance_on_mars_in_meters(lat1, long1, lat2, long2):
    degrees_to_radians = math.pi / 180.0

    # phi = 90 - latitude
    phi1 = (90.0 - lat1) * degrees_to_radians
    phi2 = (90.0 - lat2) * degrees_to_radians

    # theta = longitude
    theta1 = long1 * degrees_to_radians
    theta2 = long2 * degrees_to_radians

    # Compute spherical distance from spherical coordinates.
    cos = (math.sin(phi1) * math.sin(phi2) * math.cos(theta1 - theta2) + math.cos(phi1) * math.cos(phi2))
    arc = math.acos(cos)
    return arc * 338.6  # multiply by mars' radius to get meters


def file_to_list():
    if options.filename:
        print "opening file " + str(options.filename)
        try:
            f = open(options.filename, 'r')
            return json.load(f)
        except Exception, e:
            print "file error " + str(e)
    else:
        print "Nothing to read. Please enter a filename with the -f option"


def main():
    positions = file_to_list()
    if positions:
        start_position = positions[0]
        for position in positions[1:]:
            move_rover(start_position, position)
            start_position = position
    else:
        print "no path found"



try:
    b = nxt.locator.find_one_brick()
    motor_x = Motor(b, PORT_A)
    main()
except Exception, e:
    print "could not connect to Brick " + str(e)

