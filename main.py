import json
import tkinter
from tkinter import filedialog
from tkinter import messagebox

default_hull_json = {"size": 1.0, "maxLife": 10, "lightSrcPos": [],
                     "hasBase": False, "forceBeaconPos": [], "doorPos": [],
                     "type": "std", "engine": None, "ability": {},
                     "displayName": "---", "price": 0, "hirePrice": 0,
                     "gunSlots": [], "particleEmitters": []}
hull_json = default_hull_json.copy()
hull_json_descriptions = {"size": "How big do you want your ship to be (float)",
                          "maxLife": "Total amount of health the ship has (int)",
                          "lightSrcPos": "",
                          "hasBase": "hasBase (???)",
                          "forceBeaconPos": "",
                          "doorPos": "",
                          "type": "Hull type: one of `std`, `big`, `station`",
                          "engine": "Fully qualified engine name, blank for "
                                    "none (str)",
                          "ability": "Select ability your ship will have",
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
        self.hasBase = tkinter.IntVar()
        self.pack(anchor="n")
        self.entries = {}
        self.create_widgets()
        self.ability_property_name = tkinter.StringVar()
        self.ability_property_name.set("")
        self.ability_type = tkinter.StringVar()
        self.ability_property_value = tkinter.StringVar()
        self.ability_recharge_time = tkinter.StringVar()
        self.configure_ability_on_load()

    def configure_ability_on_load(self):
        if "type" in hull_json["ability"]:
            self.ability_type.set(hull_json["ability"]["type"])
            self.ability_configurer()
            self.ability_property_value.set(str(hull_json["ability"][
                                                    self.ability_property_name.get()]))
            self.ability_recharge_time.set(str(hull_json["ability"][
                                                   "rechargeTime"]))
        else:
            self.ability_type.set("None")

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

        # Default values for entry fields
        self.insert_default_values()

        # hasBase
        self.hasBase_widgets(right_column)

        # ability
        self.ability_widgets(right_column)

    def ability_widgets(self, right_column):
        frame = tkinter.Frame(right_column,
                              width=400,
                              borderwidth=1,
                              relief="ridge")
        frame.pack(side="top", pady=2)
        tkinter.Label(frame, text=hull_json_descriptions["ability"]).pack(
            side="left", padx=5, pady=5)
        tkinter.Button(frame, text="...", command=self.ability_chooser).pack(
            side="right", padx=5, pady=5)

    def ability_chooser(self):
        self.temp_window = tkinter.Toplevel(self, width=400)
        frame_one = tkinter.Frame(self.temp_window)
        frame_one.pack(side="top", padx=5, pady=5)
        tkinter.OptionMenu(frame_one, self.ability_type, "None", "sloMo",
                           "teleport",
                           "knockBack", "emWave", "unShield").pack(side="left")
        tkinter.Button(frame_one, text="Select ability",
                       command=self.ability_configurer).pack(side="right")
        frame_two = tkinter.Frame(self.temp_window)
        frame_two.pack(side="top", padx=5, pady=5)
        tkinter.Label(frame_two, textvariable=self.ability_property_name).pack(
            side="left")
        tkinter.Entry(frame_two, width=4,
                      textvariable=self.ability_property_value).pack()
        frame_rechargetime = tkinter.Frame(self.temp_window)
        frame_rechargetime.pack(side="top", padx=5, pady=5)
        tkinter.Label(frame_rechargetime, text="Recharge time").pack(
            side="left")
        tkinter.Entry(frame_rechargetime, width=2,
                      textvariable=self.ability_recharge_time).pack(
            side="right")
        tkinter.Button(self.temp_window, text="Save and Exit",
                       command=self.ability_save_and_exit).pack(side="top")

    def ability_configurer(self):
        if self.ability_type.get() == "teleport":
            self.ability_property_name.set("angle")
        elif self.ability_type.get() == "sloMo":
            self.ability_property_name.set("factor")
        elif self.ability_type.get() == "knockBack":
            self.ability_property_name.set("force")
        elif self.ability_type.get() == "emWave":
            self.ability_property_name.set("duration")
        elif self.ability_type.get() == "unShield":
            self.ability_property_name.set("amount")
        elif self.ability_type.get() == "None":
            self.ability_property_name.set("")

    def hasBase_widgets(self, right_column):
        frame = tkinter.Frame(right_column,
                              width=400,
                              borderwidth=1,
                              relief="ridge")
        frame.pack(side="top", pady=2)
        tkinter.Checkbutton(frame,
                            text=hull_json_descriptions["hasBase"],
                            variable=self.hasBase,
                            ).pack(side="left", padx=5, pady=5)

    def ability_save_and_exit(self):
        if self.ability_type.get() != "None":
            hull_json["ability"]["type"] = self.ability_type.get()
            hull_json["ability"][self.ability_property_name.get()] = \
                int(self.ability_property_value.get())
            hull_json["ability"]["rechargeTime"] = \
                int(self.ability_recharge_time.get())
        self.temp_window.destroy()

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
                       command=self.quit).pack(side="right", padx=5, pady=5)

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
    global hull_json, default_hull_json
    name = filedialog.askopenfilename(
        filetypes=[("JSON files", ".json"), ("All Files", "*")],
        parent=app,
        initialdir="~")
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if name == () or name == "":
        return
    hull_json = {**default_hull_json, **json.load(open(name))}
    app.configure_ability_on_load()


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
    global hull_json, b2d_file
    # for whatever reason, filedialogs returns either () or "" on Cancel
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
    hull_json["engine"] = app.engine_entry.get() if app.engine_entry.get(
    ) != "" else None
    hull_json["hasBase"] = app.hasBase.get() == 1
    if "rigidBody" not in hull_json:
        if not messagebox.askyesno(
                message="There is no physics mesh active. For making the "
                        "ship usable, please import a b2d physics mesh "
                        "using the button `Load b2d file`. You may still "
                        "choose to continue with exporting the hull file; "
                        "to make it usable, you will, however, still have "
                        "to include the physics mesh. Do you wish to "
                        "continue?"):
            print("hi")
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
