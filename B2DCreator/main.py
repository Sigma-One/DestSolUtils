#! /usr/bin/env python

import tkinter # Main UI
import time    # Needed for logging
import math    # sqrt()

# Sigma-One's usual logging lambdas
LOG_DBUG = lambda s : print(time.strftime("[%d%m%y-%H%M%S]") + "\033[95m [DBUG]\033[0m: " + str(s)) # Debug
LOG_INFO = lambda s : print(time.strftime("[%d%m%y-%H%M%S]") + "\033[92m [INFO]\033[0m: " + str(s)) # Info
LOG_WARN = lambda s : print(time.strftime("[%d%m%y-%H%M%S]") + "\033[93m [WARN]\033[0m: " + str(s)) # Warning
LOG_FAIL = lambda s : print(time.strftime("[%d%m%y-%H%M%S]") + "\033[91m [FAIL]\033[0m: " + str(s)) # Failure


quit = False


class Main(object):
  """Main(object)
  Contains most of the program
  """
  
  def __init__(self):
    """Main.__init__()
    Initializes some variables, calls the GUI init, and starts the main loop
    """
    
    LOG_INFO("Initializing...")
    
    self.root = tkinter.Tk()
    
    self.quit = False
    
    self.shapes = [[]]
    self.current_shape = 0
    self.current_node = None
    
    self.tk_init()
    
    LOG_INFO("Starting...")
    self.mainloop()
  
  
  def tk_init(self):
    """Main.tk_init()
    Configures the GUI, creating widgets and adding callbacks
    """
    
    # Create canvas
    self.canvas = tkinter.Canvas(self.root, width=512, height=512, relief=tkinter.GROOVE, background="#a0a0a0")
    self.canvas.grid(columnspan=(600), rowspan=500)
    self.canvas.pack(side=tkinter.LEFT)

    # Create frame for various buttons
    self.control_root = tkinter.Frame(self.root, width=128)
    self.control_root.pack(side=tkinter.LEFT)

    # "Add Mesh" Button
    self.button_new_shape = tkinter.Button(self.control_root, text="Add Mesh", command=self.add_shape)
    self.button_new_shape.pack()

    # Bind callbacks for various canvas events
    self.canvas.bind("<Motion>", self.canvas_motion            )
    self.canvas.bind("<ButtonPress-1>", self.canvas_click_begin)
    self.canvas.bind("<ButtonRelease-1>", self.canvas_click_end)
    self.canvas.bind("<Button-3>", self.canvas_rclick          )

    LOG_DBUG("Tkinter layout ready")


  def mainloop(self):
    """Main.mainloop()
    Main loop, mostly handles drawing
    """
    
    while not self.quit:
      # Clear canvas
      self.canvas.delete("all")
      for shape in self.shapes:
        for node in shape:
          # Choose mesh colour based on selected shape
          if self.shapes.index(shape) == self.current_shape:
            node_fill = "#006600"
          else:
            node_fill = "#660000"
          
          # Draw nodes
          self.canvas.create_line(node[0], node[1], shape[shape.index(node) - 1][0], shape[shape.index(node) - 1][1], fill=node_fill, width=2)
          self.canvas.create_oval(node[0]-5, node[1]-5, node[0]+5, node[1]+5, fill=node_fill, outline="")
      
      self.root.update()
  
  
  def test_for_node(self, pos):
    """
    Tests if position is close to a node
    
    Args:
    * pos (tuple) : Position to test against
    Returns:
    * shape (list ) : The shape a node was found in
    * node  (tuple) : The node found
    * None  (N/A  ) : Only returned if no node found in range
    """
    
    for shape in self.shapes:
      for node in shape:
        if (math.sqrt((pos[0] - node[0]) ** 2 + (pos[1] - node[1]) ** 2)) < 5:
          LOG_DBUG("Node found at " + str(node))
          return shape, node
    
    return None, None
  
  
  def add_node(self, pos):
    """
    Adds a new node to the current shape, at position pos
    
    Args:
    * pos (tuple) : Position for new node
    """
    
    LOG_DBUG("Adding node at " + str(pos))
    self.shapes[self.current_shape].append(pos)
  
  
  def add_shape(self):
    """
    Adds a new shape and selects it
    """
    
    self.shapes.append([])
    self.current_shape = len(self.shapes) - 1
  
  
  def canvas_click_begin(self, event):
    """
    Called if mouse1 is pressed on the canvas
    Selects node for dragging, or adds a new one
    
    Args:
    * event (Event) : Event object from tkinter
    """
  
    pos = (event.x, event.y)
    shape, node = self.test_for_node(pos)
    if node:
      self.current_node = shape.index(node)
      LOG_DBUG("Selected node: " + str(self.current_node))
      self.current_shape = self.shapes.index(shape)
      LOG_DBUG("Selected shape: " + str(self.current_shape))
      
    else:
      self.add_node(pos)
  
  
  def canvas_click_end(self, event):
    """
    Called if mouse1 is released on the canvas
    Clears selected node
    
    Args:
    * event (Event) : Event object from tkinter
    """
    
    self.current_node = None
  
  
  def canvas_motion(self, event):
    """
    Called if mouse is moved on the canvas
    Moves selected node
    
    Args:
    * event (Event) : Event object from tkinter
    """
    
    pos = (event.x, event.y)
    if self.current_node != None:
      self.shapes[self.current_shape][self.current_node] = pos
  
  
  def canvas_rclick(self, event):
    """
    Called if mouse3 is pressed on the canvas
    Removes clicked node
    
    Args:
    * event (Event) : Event object from tkinter
    """
    pos = (event.x, event.y)
    shape, node = self.test_for_node(pos)
    if node:
      LOG_DBUG("Removing node at " + str(node))
      shape.remove(node)



main = Main()
