#! /usr/bin/env python3


import json
from tkinter import filedialog


def dumpNodes(shapes):

  # Ask user for file to export to
  filename = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="~")
  if not filename:
    # If no file provided, just stop
    return


  print(shapes)


  json_root = []

  rigid_body = {}
  polygons = []


  for i in range(len(shapes)):
    json_root.append([])
    for j in shapes[i]:

      pos_dict = {}

      pos_dict["x"] = j.pos[0]
      pos_dict["y"] = j.pos[1]
      polygons.append([pos_dict])


  rigidBody["polygons"] = polygons
  json_root.append(rigidBody)


  with open(filename, "w") as export_file:
    json.dump(json_root, export_file, indent=2, sort_keys=True)
