import json
import tkinter
from tkinter import filedialog
from tkinter import messagebox

export_file_name = ""
hull_json = {}
b2d_file = {}
b2d_json_label_text = "Open b2d file to use for physics,\nnone is loaded now"


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        left_column = tkinter.Frame(self, width=400, height=600)
        left_column.pack(side="left", anchor="ne")
        right_column = tkinter.Frame(self, width=400, height=600)
        right_column.pack(side="right", anchor="nw")

        # Load pre-created JSON
        self.load_hull_json_widgets(left_column)

        # Load box2d file
        self.load_b2d_file_widgets(left_column)

        #

    def load_b2d_file_widgets(self, left_column):
        load_b2d_json_frame = tkinter.Frame(left_column,
                                            width=400,
                                            borderwidth=1,
                                            relief="ridge")
        load_b2d_json_frame.pack(side="top", pady=2)
        load_b2d_json_button = tkinter.Button(load_b2d_json_frame,
                                              text="Load b2d file",
                                              command=loadB2DFile)
        load_b2d_json_button.pack(side="right", padx=5, pady=5)
        self.load_b2d_json_label = tkinter.Label(load_b2d_json_frame,
                                                 text=b2d_json_label_text)
        self.load_b2d_json_label.pack(side="left", padx=5, pady=5)

    def load_hull_json_widgets(self, left_column):
        load_hull_json_frame = tkinter.Frame(left_column,
                                             width=400,
                                             borderwidth=1,
                                             relief="ridge")
        load_hull_json_frame.pack(side="top", pady=2)
        load_hull_json_button = tkinter.Button(load_hull_json_frame,
                                               text="Load Hull JSON",
                                               command=loadHullJSON)
        load_hull_json_button.pack(side="right", padx=5, pady=5)
        load_hull_json_label = tkinter.Label(load_hull_json_frame,
                                             text="Open JSON "
                                                  "to base this on")
        load_hull_json_label.pack(side="left", padx=5, pady=5)


def loadHullJSON():
    global hull_json, export_file_name
    name = filedialog.askopenfilename(
        filetypes=[("JSON files", ".json"), ("All Files", "*")],
        parent=app,
        initialdir="~")
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if name == () or name == "":
        return
    hull_json = json.load(open(name))
    if messagebox.askyesno("Use as output?",
                           "Do you wish to set the selected file as file to "
                           "write the created JSON later into?"):
        export_file_name = name


def loadB2DFile():
    global b2d_file, b2d_json_label_text
    name = filedialog.askopenfilename(
        filetypes=[("All Files", "*")],
        parent=app,
        initialdir="~")
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if name == () or name == "":
        app.load_b2d_json_label[
            "text"] = "Open b2d file to use for physics,\nnone is loaded now"
        b2d_file = {}
        return
    b2d_file_temp = json.load(open(name))
    if ("rigidBodies" in b2d_file_temp and
            type(b2d_file_temp["rigidBodies"]) is list):
        b2d_file["rigidBody"] = b2d_file_temp["rigidBodies"][0]
        del b2d_file["rigidBody"]["imagePath"]
        del b2d_file["rigidBody"]["name"]
        app.load_b2d_json_label[
            "text"] = "Open b2d file to use for physics,\none is already loaded"
    else:
        messagebox.showwarning(
            message="The file you have chosen is not valid b2d file.")


def dumpHullJSON():
    global export_file_name
    # for whatever reason, filedialogs returns either () or "" on Cancel
    while export_file_name == "" or export_file_name == ():
        export_file_name = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir="~",
            parent=app
        )
    with open(export_file_name, "w") as export_file:
        json.dump(hull_json, export_file, indent=2, sort_keys=True)


app = Application()
app.master.title("DestinationSol Hull Creator")
app.master.minsize(800, 600)
app.master.resizable(False, False)
app.mainloop()
