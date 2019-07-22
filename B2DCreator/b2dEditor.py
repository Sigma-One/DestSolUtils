#! /usr/bin/env python3

import pygame
from tkinter import Tk
from tkinter import filedialog


import jsonUtils


shapes = []
current_shape = 0

WinX = 1280
WinY = 720

shapes.append([])

quit = False
selected = None
Tk().withdraw()


# Define Node class
class Node():
    def __init__(self):
        self.norm_color = (0, 0, 200)
        self.select_color = (0, 100, 0)
        self.clicked = False
        self.color = self.norm_color
        self.pos = (0, 0)
        self.rect = None

    def set_pos(self, pos):
        self.pos = pos

    def set_color(self, color):
        self.color = color
        #print("INFO: Set node ", nodes.index(self), " color to ", self.color)

def set_current_shape(num):
    global current_shape
    current_shape = num

def add_node(pos):
    new_node = Node()
    new_node.set_pos(pos)
    shapes[current_shape].append(new_node)

pygame.init()
screen=pygame.display.set_mode([WinX, WinY], pygame.RESIZABLE)

while not quit:
    #print(pygame.mouse.get_pos())

    # Handle inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True

        # Check if mouse1 clicked on node
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for nodes in shapes:
                    for i in nodes:
                        # Compare event position to each node's position
                        if i.pos[0] - 4 <= event.pos[0] <= i.pos[0] + 4 and i.pos[1] - 4 <= event.pos[1] <= i.pos[1] + 4:
                        # Set clicked node's color and set it as selected
                            i.clicked = True
                            selected = i
                            set_current_shape(shapes.index(nodes))

                if selected == None:
                    add_node(event.pos)

            # Check if mouse2 (3 in pygame terms) clicked on node
            elif event.button == 3:
                    for i in nodes:
                        # Compare event position to each node's position
                        if i.pos[0] - 4 <= event.pos[0] <= i.pos[0] + 4 and i.pos[1] - 4 <= event.pos[1] <= i.pos[1] + 4:
                        # Remove clicked node
                            nodes.remove(i)

        # Set selected node's position to the mouse's
        elif event.type == pygame.MOUSEMOTION:
            if selected != None:
                selected.pos = event.pos

        # De-select node on mouse1 release
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                if selected != None:
                    selected.clicked = False
                selected = None

        # Add node if insert is pressed
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_INSERT:
                add_node((10, 10))

            elif event.key == pygame.K_s:
                jsonUtils.dumpNodes(shapes)

            elif event.key == pygame.K_n:
                shapes.append([])
                #print(current_shape)
                set_current_shape(len(shapes) - 1)
                #print(current_shape)

        elif event.type == pygame.VIDEORESIZE:
            if event.w < event.h:
                event.h = event.w
            screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)

    # Clear the screen
    screen.fill((200, 200, 200))

    #print(len(shapes))

    if len(shapes) > 0:
        # Iterate through nodes to draw them
        for j in range(len(shapes)):
            nodes = shapes[j]

            if j != current_shape:
                color = 1
            else:
                color = 0

            for i in range(len(nodes)):
                node = nodes[i]
                # Draw line between current and previous node if node is not the first one
                if i > 0:
                    pygame.draw.line(screen, node.color, node.pos, nodes[i - 1].pos, 2)

                # Draw line between last and first node
                if len(nodes) > 0 and i == len(nodes) - 1:
                    pygame.draw.line(screen, node.color, nodes[len(nodes) - 1].pos, nodes[0].pos, 2)

                # Draw node circles
                if node.clicked:
                    pygame.draw.circle(screen, node.color, node.pos, 7)
                else:
                    pygame.draw.circle(screen, node.color, node.pos, 4)
                pygame.draw.circle(screen, node.color, node.pos, 8, 2)

                if color == 1:
                    node.set_color(node.norm_color)
                else:
                    node.set_color(node.select_color)


    # Update display
    pygame.display.update()
