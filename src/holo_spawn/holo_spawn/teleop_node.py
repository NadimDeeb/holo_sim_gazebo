#!/usr/bin/env python3

import os
import rclpy
import pygame
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TeleopKeyboard(Node):

    def __init__(self):
        super().__init__("hololens_teleop")

        # Publisher to /cmd_vel with message type Twist
        self.key_stroke = self.create_publisher(Twist, "demo/cmd_vel", 10)

        # Notify that the publisher has been created succesfully
        self.get_logger().info("Publisher to /cmd_vel created")

        # Call node functionality
        self.cmd_publisher()
    
    def cmd_publisher(self):
        # Initialize pygame
        pygame.init()
        screen_height = 200
        screen_width = 200
        screen = pygame.display.set_mode((screen_width,screen_height))
        clock = pygame.time.Clock()
        running = True

        # Create rate for message sent
        rate = self.create_rate(10)

        # Initialize empty message to be send ready to be updated
        twist_msg = Twist()

        # Initialize messages to populate the Twist message
        twist_msg.linear.x = 0.0
        twist_msg.angular.z = 0.0

        # Infinite loop to keep reading keyboard input
        while rclpy.ok():
            # Close pygame when node dies
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

            # Keyboard bindings
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]: # if w pressed, forward
                twist_msg.linear.x = 0.0006
                self.key_stroke.publish(twist_msg)
            elif keys[pygame.K_s]: # if s pressed, backwards
                twist_msg.linear.x = -0.0006
                self.key_stroke.publish(twist_msg)

            if keys[pygame.K_d]: # if d pressed, right
                twist_msg.angular.z = -0.0006
                self.key_stroke.publish(twist_msg)
                twist_msg.angular.z = 0.0 # zero angular in order to not stick
            elif keys[pygame.K_a]: # if a pressed, left
                twist_msg.angular.z = 0.0006
                self.key_stroke.publish(twist_msg)
                twist_msg.angular.z = 0.0 # zero angular in order to not stick
            
            if keys[pygame.K_x]: #if x pressed, stop
                twist_msg.linear.x = 0.0
                twist_msg.angular.z = 0.0
                self.key_stroke.publish(twist_msg)

            rate.sleep

def main(args=None):
    rclpy.init(args=args)
    node = TeleopKeyboard()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()