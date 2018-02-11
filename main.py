import json
import tkinter
from tkinter import filedialog
from tkinter import messagebox

export_file_name = ""
default_hull_json = {"size": 1.0, "maxLife": 10, "lightSrcPos": [],
                     "hasBase": False, "forceBeaconPos": [], "doorPos": [],
                     "type": "std", "engine": None, "ability": {},
                     "displayName": "---", "price": 0, "hirePrice": 0,
                     "gunSlots": [], "particleEmitters": []}
hull_json = default_hull_json.copy()
hull_json_descriptions = {"size": "How big do you want your ship to be (float)",
                          "maxLife": "Total amount of health the ship has (int)",
                          "lightSrcPos": "",
                          "hasBase": "",
                          "forceBeaconPos": "",
                          "doorPos": "",
                          "type": "Hull type: one of `std`, `big`, `station`",
                          "engine": "Fully qualified engine name, blank for "
                                    "none (str)",
                          "ability": "",
                          "displayName": "Name of the ship (str)",
                          "price": "Price of the ship (int)",
                          "hirePrice": "Price of the ship to hire (int)",
                          "gunSlots": "",
                          "particleEmitters": ""}
b2d_file = {}
b2d_json_label_text = "Open b2d file to use for physics,\nnone is loaded now"


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack(anchor="n")
        self.entries = {}
        self.create_widgets()

    def create_widgets(self):
        left_column = tkinter.Frame(self, width=400, height=600)
        left_column.pack(side="left", anchor="nw", ipadx=5)
        right_column = tkinter.Frame(self, width=400, height=600)
        right_column.pack(side="right", anchor="ne", ipadx=5)

        # Load pre-created JSON
        self.load_hull_json_widgets(left_column)

        # Load box2d file
        self.load_b2d_file_widgets(left_column)

        # Export/Exit buttons
        self.export_exit_widgets(right_column)

        # Int/Float/String fields
        self.entry_widgets(left_column, "size", 4)
        self.entry_widgets(left_column, "maxLife", 3)
        self.entry_widgets(left_column, "type", 7)
        self.entry_widgets(left_column, "displayName", 10)
        self.entry_widgets(left_column, "price", 3)
        self.entry_widgets(left_column, "hirePrice", 3)
        self.engine_widgets(left_column, 15)

        # MaxLife
        self.insert_default_values()

    def entry_widgets(self, column, param_name, entry_width):
        frame = tkinter.Frame(column,
                              width=400,
                              borderwidth=1,
                              relief="ridge")
        frame.pack(side="top", pady=2)
        tkinter.Label(frame, text=hull_json_descriptions[param_name]).pack(
            side="left", padx=5, pady=5)
        self.entries[param_name] = tkinter.Entry(frame,
                                                 width=entry_width)
        self.entries[param_name].pack(side=tkinter.RIGHT, padx=5, pady=5)

    def engine_widgets(self, column, entry_width):
        frame = tkinter.Frame(column,
                              width=400,
                              borderwidth=1,
                              relief="ridge")
        frame.pack(side="top", pady=2)
        tkinter.Label(frame, text=hull_json_descriptions["engine"]).pack(
            side="left", padx=5, pady=5)
        self.engine_entry = tkinter.Entry(frame, width=entry_width)
        self.engine_entry.pack(side=tkinter.RIGHT, padx=5, pady=5)

    def insert_default_values(self):
        for key in self.entries.keys():
            self.entries[key].delete(0)
            self.entries[key].insert(0, hull_json[key])

    def export_exit_widgets(self, right_column):
        export_exit_frame = tkinter.Frame(right_column,
                                          width=400,
                                          borderwidth=1,
                                          relief="ridge")
        export_exit_frame.pack(side="bottom", pady=2)
        tkinter.Button(export_exit_frame,
                       text="Export",
                       command=dumpHullJSON).pack(side="left", padx=5, pady=5)
        tkinter.Button(export_exit_frame,
                       text="Exit",
                       command=exit).pack(side="right", padx=5, pady=5)

    def load_b2d_file_widgets(self, left_column):
        load_b2d_json_frame = tkinter.Frame(left_column,
                                            width=400,
                                            borderwidth=1,
                                            relief="ridge")
        load_b2d_json_frame.pack(side="top", pady=2)
        self.load_b2d_json_label = tkinter.Label(load_b2d_json_frame,
                                                 text=b2d_json_label_text)
        self.load_b2d_json_label.pack(side="left", padx=5, pady=5)
        tkinter.Button(load_b2d_json_frame,
                       text="Load b2d file",
                       command=loadB2DFile).pack(side="right", padx=5, pady=5)

    def load_hull_json_widgets(self, left_column):
        load_hull_json_frame = tkinter.Frame(left_column,
                                             width=400,
                                             borderwidth=1,
                                             relief="ridge")
        load_hull_json_frame.pack(side="top", pady=2)
        tkinter.Label(load_hull_json_frame,
                      text="Open JSON to base this on").pack(side="left",
                                                             padx=5,
                                                             pady=5)
        tkinter.Button(load_hull_json_frame,
                       text="Load Hull JSON",
                       command=loadHullJSON).pack(side="right", padx=5, pady=5)


def loadHullJSON():
    global hull_json, export_file_name, default_hull_json
    name = filedialog.askopenfilename(
        filetypes=[("JSON files", ".json"), ("All Files", "*")],
        parent=app,
        initialdir="~")
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if name == () or name == "":
        return
    hull_json = {**default_hull_json, **json.load(open(name))}
    if messagebox.askyesno("Use as output?",
                           "Do you wish to set the selected file as file to "
                           "write the created JSON later into?"):
        export_file_name = name


def loadB2DFile():
    global b2d_file
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
    global export_file_name, hull_json, b2d_file
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if export_file_name == "" or export_file_name == ():
        export_file_name = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            initialdir="~",
            parent=app
        )
        if export_file_name == "" or export_file_name == ():
            return
        app_entries = {k: v.get() for k, v in app.entries.items()}
        hull_json.update(b2d_file)
        hull_json.update(app_entries)
        hull_json["engine"] = app.engine_entry.get()
        if "rigidBody" not in hull_json:
            if not messagebox.askyesno(
                    message="There is no physics mesh active. For making the "
                            "ship usable, please import a b2d physics mesh "
                            "using the button `Load b2d file`. You may still "
                            "choose to continue with exporting the hull file; "
                            "to make it usable, you will, however, still have "
                            "to include the physics mesh. Do you wish to "
                            "continue?"):
                return
    with open(export_file_name, "w") as export_file:
        json.dump(hull_json,
                  export_file,
                  indent=2,
                  sort_keys=True)


app = Application()
app.master.title("DestinationSol Hull Creator")
app.master.minsize(800, 600)
app.master.resizable(False, False)
app.mainloop()
