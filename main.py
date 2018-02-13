import json
import tkinter
from tkinter import filedialog
from tkinter import messagebox

sticky_we = tkinter.W+tkinter.E

default_hull_json = {"size": 1.0, "maxLife": 10, "lightSrcPos": [],
                     "hasBase": False, "forceBeaconPos": [], "doorPos": [],
                     "type": "std", "engine": None, "ability": {},
                     "displayName": "---", "price": 0, "hirePrice": 0,
                     "gunSlots": [], "particleEmitters": []}
hull_json = default_hull_json.copy()
hull_json_descriptions = {"size": "How big do you want your ship to be (float)",
                          "maxLife": "Total amount of health the ship has (int)",
                          "lightSrcPos": "Positions of lights on the ship",
                          "hasBase": "hasBase (???)",
                          "forceBeaconPos": "Positions of beacons on the ship",
                          "doorPos": "Positions of the doors",
                          "type": "Hull type: one of `std`, `big`, `station`",
                          "engine": "Fully qualified engine name, blank for "
                                    "none (str)",
                          "ability": "Select ability your ship will have",
                          "displayName": "Name of the ship (str)",
                          "price": "Price of the ship (int)",
                          "hirePrice": "Price of the ship to hire (int)",
                          "gunSlots": "Gun slots on the ship",
                          "particleEmitters": "ParticleEmitters on your ship"}
b2d_file = {}
b2d_json_label_text = "Open b2d file to use for physics,\nnone is loaded now"


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)

        self.temp_window = None
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
        self.tempPosString = tkinter.StringVar()
        self.posarrays_name = ""
        self.gunSlots_isUnderneathHull = tkinter.BooleanVar()
        self.gunSlots_allowsRotation = tkinter.BooleanVar()
        self.gunSlots_entry_selected = 0
        self.particleEmitter_angleOffset = tkinter.StringVar()
        self.particleEmitter_effectFile = tkinter.StringVar()
        self.particleEmitter_size = tkinter.StringVar()
        self.particleEmitter_tex = tkinter.StringVar()
        self.particleEmitter_tint = tkinter.StringVar()
        self.particleEmitter_floatsUp = tkinter.BooleanVar()
        self.particleEmitter_trigger = tkinter.StringVar()
        self.particleEmitter_hasLight = tkinter.BooleanVar()

    def configure_ability_on_load(self):
        if "type" in hull_json["ability"]:
            self.ability_type.set(hull_json["ability"]["type"])
            self.ability_configurer()
            self.ability_property_value.set(str(hull_json["ability"][self.ability_property_name.get()]))
            self.ability_recharge_time.set(str(hull_json["ability"]["rechargeTime"]))
        else:
            self.ability_type.set("None")

    def create_widgets(self):
        left_column = tkinter.Frame(self, width=400, height=600)
        left_column.grid(row=0, column=0, sticky=tkinter.N)
        right_column = tkinter.Frame(self, width=400, height=600)
        right_column.grid(row=0, column=1, sticky=tkinter.N)

        # Load pre-created JSON
        self.load_hull_json_widgets(left_column)

        # Load box2d file
        self.load_b2d_file_widgets(left_column)

        # Export/Exit buttons
        self.export_exit_widgets(right_column)

        # Int/Float/String fields
        self.entry_widgets(left_column, "size", 4, 0)
        self.entry_widgets(left_column, "maxLife", 3, 1)
        self.entry_widgets(left_column, "type", 7, 2)
        self.entry_widgets(left_column, "displayName", 10, 3)
        self.entry_widgets(left_column, "price", 3, 4)
        self.entry_widgets(left_column, "hirePrice", 3, 5)
        self.engine_widgets(left_column, 15, 6)

        # Default values for entry fields
        self.insert_default_values()

        # hasBase
        self.hasBase_widgets(right_column)

        # ability
        self.ability_widgets(right_column)

        # arrays od position strings
        self.posarrays_widgets(right_column, "lightSrcPos", 3)
        self.posarrays_widgets(right_column, "forceBeaconPos", 4)
        self.posarrays_widgets(right_column, "doorPos", 5)

        self.gunSlots_widgets(right_column)
        self.particleEmitters_widgets(right_column)

    # right column items

    # particleEmitters
    def particleEmitters_widgets(self, column):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=7, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame, text=hull_json_descriptions["particleEmitters"]).grid(row=0, column=0)
        tkinter.Button(frame, text="...", command=self.particleEmitters_window).grid(row=0, column=1)

    def particleEmitters_window(self):
        if self.temp_window is not None:
            return
        self.temp_window = tkinter.Toplevel(self, width=400)
        self.temp_window.protocol('WM_DELETE_WINDOW', self.gunSlots_window_exit)
        self.temp_window.attributes('-topmost', 'true')
        frame_top = tkinter.Frame(self.temp_window)
        frame_top.grid(row=0, column=0, pady=5)
        frame_bottom = tkinter.Frame(self.temp_window)
        frame_bottom.grid(row=1, column=0, pady=5)
        self.listbox = tkinter.Listbox(frame_top)
        self.listbox.grid(row=0, column=0, padx=5)
        frame_top_right = tkinter.Frame(frame_top)
        frame_top_right.grid(row=0, column=1, padx=5)
        frame_temp = tkinter.Frame(frame_top_right, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=0, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="Position").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.tempPosString, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_top_right, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=1, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="trigger").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_trigger, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_top_right, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=2, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="angleOffset").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_angleOffset, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_top_right, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=3, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Checkbutton(frame_temp, text="hasLight", variable=self.particleEmitter_hasLight).grid(row=0, column=0)
        frame_particle_def = tkinter.Frame(frame_top_right, width=400, borderwidth=1, relief="ridge")
        frame_particle_def.grid(row=3, column=0, sticky=sticky_we, padx=1, pady=1, ipadx=5, ipady=5)
        tkinter.Label(frame_particle_def, text="Particle thingies:").grid(row=0, column=0)
        frame_temp = tkinter.Frame(frame_particle_def, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=1, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="effectFile").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_effectFile, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_particle_def, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=2, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="size").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_size, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_particle_def, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=3, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="tex").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_tex, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_particle_def, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=4, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame_temp, text="tint").grid(row=0, column=0)
        tkinter.Entry(frame_temp, textvariable=self.particleEmitter_tint, width=10).grid(row=0, column=1)
        frame_temp = tkinter.Frame(frame_particle_def, width=400, borderwidth=1, relief="ridge")
        frame_temp.grid(row=4, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Checkbutton(frame_temp, text="floatsUp", ).grid(row=0, column=0)
        frame_top_right = tkinter.Frame(frame_top_right)
        frame_top_right.grid(row=4, column=0)
        tkinter.Button(frame_top_right, command=self.particleEmitters_save, text="Save").grid(row=0, column=0, padx=3)
        tkinter.Button(frame_top_right, command=self.particleEmitters_load, text="Select").grid(row=0, column=1)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.insert(tkinter.END, "0.5 0.5"), text="Add").grid(row=0, column=0)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.delete(tkinter.ACTIVE), text="Remove").grid(row=0, column=1)
        tkinter.Button(frame_bottom, command=self.particleEmitters_window_exit, text="Exit").grid(row=0, column=2)

    def particleEmitters_save(self):
        if self.listbox.size() == 0:
            return
        hull_json["particleEmitters"][self.particleEmitters_entry_selected] = {
            "position": self.tempPosString.get(),
            "trigger": self.particleEmitter_trigger.get(),
            "angleOffset": self.particleEmitter_angleOffset.get(),
            "hasLight": self.particleEmitter_hasLight.get(),
            "particle": {
                "effectFile": self.particleEmitter_effectFile.get(),
                "size": self.particleEmitter_size.get(),
                "tex": self.particleEmitter_tex.get(),
                "floatsUp": self.particleEmitter_floatsUp.get(),
                "tint": self.particleEmitter_tint.get()
        }}
        self.listbox.delete(self.gunSlots_entry_selected)
        self.listbox.insert(self.gunSlots_entry_selected, self.tempPosString.get())

    def particleEmitters_load(self):
        if self.listbox.size() == 0:
            return
        self.particleEmitters_entry_selected = self.listbox.index(tkinter.ACTIVE)
        while self.particleEmitters_entry_selected + 1 > len(hull_json["particleEmitters"]):
            hull_json["particleEmitters"].append({"position": "0.5 0.5", "trigger": "engine", "angleOffset": "0.0", "hasLight": False,
                                          "particle": {
                                              "effectFile": "FILE",
                                              "size": "0",
                                              "tex": "TEXTURE",
                                              "floatsUp": False,
                                              "tint": "TINT"
                                          }})
        item = hull_json["particleEmitters"][self.particleEmitters_entry_selected]
        self.tempPosString.set(item["position"])
        self.particleEmitter_trigger.set(item["trigger"])
        self.particleEmitter_angleOffset.set(item["angleOffset"])
        self.particleEmitter_hasLight.set(item["hasLight"])
        self.particleEmitter_effectFile.set(item["particle"]["effectFile"])
        self.particleEmitter_size.set(item["particle"]["size"])
        self.particleEmitter_tex.set(item["particle"]["tex"])
        self.particleEmitter_floatsUp.set(item["particle"]["floatsUp"])
        self.particleEmitter_tint.set(item["particle"]["tint"])

    def particleEmitters_window_exit(self):
        self.listbox.destroy()
        self.temp_window.destroy()
        self.temp_window = None

    # gunSlots
    def gunSlots_widgets(self, column):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=6, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame, text=hull_json_descriptions["gunSlots"]).grid(row=0, column=0)
        tkinter.Button(frame, text="...", command=self.gunSlots_window).grid(row=0, column=1)


    def gunSlots_window(self):
        if self.temp_window is not None:
            return
        self.temp_window = tkinter.Toplevel(self, width=400)
        self.temp_window.protocol('WM_DELETE_WINDOW', self.gunSlots_window_exit)
        self.temp_window.attributes('-topmost', 'true')
        frame_top = tkinter.Frame(self.temp_window)
        frame_top.grid(row=0, column=0, pady=5)
        frame_bottom = tkinter.Frame(self.temp_window)
        frame_bottom.grid(row=1, column=0, pady=5)
        self.listbox = tkinter.Listbox(frame_top)
        self.listbox.grid(row=0, column=0, padx=5)
        frame_top_right = tkinter.Frame(frame_top)
        frame_top_right.grid(row=0, column=1, padx=5)
        tkinter.Entry(frame_top_right, width=10, textvariable=self.tempPosString).grid(row=0, column=0, columnspan=2, pady=3)
        tkinter.Checkbutton(frame_top_right, text="isUnderneathHull", variable=self.gunSlots_isUnderneathHull).grid(row=1, column=0, columnspan=2, pady=3)
        tkinter.Checkbutton(frame_top_right, text="allowsRotation", variable=self.gunSlots_allowsRotation).grid(row=2, column=0, columnspan=2, pady=3)
        tkinter.Button(frame_top_right, command=self.gunSlots_save, text="Save").grid(row=3, column=0, padx=3)
        tkinter.Button(frame_top_right, command=self.gunSlots_load, text="Select").grid(row=3, column=1)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.insert(tkinter.END, "0.5 0.5"), text="Add").grid(row=0, column=0)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.delete(tkinter.ACTIVE), text="Remove").grid(row=0, column=1)
        tkinter.Button(frame_bottom, command=self.gunSlots_window_exit, text="Exit").grid(row=0, column=2)

    def gunSlots_save(self):
        if self.listbox.size() == 0:
            return
        hull_json["gunSlots"][self.gunSlots_entry_selected]["isUnderneathHull"] = self.gunSlots_isUnderneathHull.get()
        hull_json["gunSlots"][self.gunSlots_entry_selected]["allowsRotation"] = self.gunSlots_allowsRotation.get()
        hull_json["gunSlots"][self.gunSlots_entry_selected]["position"] = self.tempPosString.get()
        self.listbox.delete(self.gunSlots_entry_selected)
        self.listbox.insert(self.gunSlots_entry_selected, self.tempPosString.get())

    def gunSlots_load(self):
        if self.listbox.size() == 0:
            return
        self.gunSlots_entry_selected = self.listbox.index(tkinter.ACTIVE)
        while self.gunSlots_entry_selected + 1 > len(hull_json["gunSlots"]):
            hull_json["gunSlots"].append({"position": "0.5 0.5", "isUnderneathHull": False, "allowsRotation": True})
        item = hull_json["gunSlots"][self.gunSlots_entry_selected]
        self.gunSlots_isUnderneathHull.set(item["isUnderneathHull"])
        self.gunSlots_allowsRotation.set(item["allowsRotation"])
        self.tempPosString.set(item["position"])

    def gunSlots_window_exit(self):
        self.listbox.destroy()
        self.temp_window.destroy()
        self.temp_window = None

    # hasBase(?) checkbox
    def hasBase_widgets(self, right_column):
        frame = tkinter.Frame(right_column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=0, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Checkbutton(frame, text=hull_json_descriptions["hasBase"], variable=self.hasBase).grid(row=0, column=0)

    # ability chooser button
    def ability_widgets(self, right_column):
        frame = tkinter.Frame(right_column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=1, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame, text=hull_json_descriptions["ability"]).grid(row=0, column=0)
        tkinter.Button(frame, text="...", command=self.ability_chooser).grid(row=0, column=1)

    # exit and export buttons
    def export_exit_widgets(self, right_column):
        export_exit_frame = tkinter.Frame(right_column, width=400, borderwidth=1, relief="ridge")
        export_exit_frame.grid(row=2, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Button(export_exit_frame, text="Export", command=dumpHullJSON).grid(row=0, column=0)
        tkinter.Button(export_exit_frame, text="Exit", command=exit).grid(row=0, column=1)

    # left column items

    # entry fields for different hull properties
    def entry_widgets(self, column, param_name, entry_width, frame_row):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=frame_row, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame, text=hull_json_descriptions[param_name]).grid(row=0, column=0)

        self.entries[param_name] = tkinter.Entry(frame, width=entry_width)
        self.entries[param_name].grid(row=0, column=1)

    # entry fields for engine properties
    def engine_widgets(self, column, entry_width, frame_row):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=frame_row, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame, text=hull_json_descriptions["engine"]).grid(row=0, column=0)

        self.engine_entry = tkinter.Entry(frame, width=entry_width)
        self.engine_entry.grid(row=0, column=1)

    # button for loading b2d json file
    def load_b2d_file_widgets(self, left_column):
        load_b2d_json_frame = tkinter.Frame(left_column, width=400, borderwidth=1, relief="ridge")
        load_b2d_json_frame.grid(row=7, column=0, sticky=sticky_we, padx=1, pady=1)

        self.load_b2d_json_label = tkinter.Label(load_b2d_json_frame, text=b2d_json_label_text)
        self.load_b2d_json_label.grid(row=0, column=0)

        tkinter.Button(load_b2d_json_frame, text="Load b2d file", command=loadB2DFile).grid(row=0, column=1)

    # button for loading hull json file for editing
    def load_hull_json_widgets(self, left_column):
        load_hull_json_frame = tkinter.Frame(left_column, width=400, borderwidth=1, relief="ridge")
        load_hull_json_frame.grid(row=8, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(load_hull_json_frame, text="Open JSON for editing").grid(row=0, column=0)
        tkinter.Button(load_hull_json_frame, text="Load Hull JSON", command=loadHullJSON).grid(row=0, column=1)

    def ability_chooser(self):
        if self.temp_window is not None:
            return
        self.temp_window = tkinter.Toplevel(self, width=400)
        self.temp_window.protocol('WM_DELETE_WINDOW', self.ability_save_and_exit)
        self.temp_window.attributes('-topmost', 'true')
        frame_ability_chooser = tkinter.Frame(self.temp_window)
        frame_ability_chooser.grid(row=0, column=0)
        frame_one = tkinter.Frame(frame_ability_chooser, width=400, borderwidth=1, relief="ridge")
        frame_one.grid(row=0, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.OptionMenu(frame_one, self.ability_type, "None", "sloMo", "teleport", "knockBack", "emWave", "unShield").grid(row=0, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Button(frame_one, text="Select ability", command=self.ability_configurer).grid(row=0, column=1)

        frame_two = tkinter.Frame(frame_ability_chooser, width=400, borderwidth=1, relief="ridge")
        frame_two.grid(row=1, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame_two, textvariable=self.ability_property_name).grid(row=0, column=0)
        tkinter.Entry(frame_two, width=4, textvariable=self.ability_property_value).grid(row=0, column=1)

        frame_rechargetime = tkinter.Frame(frame_ability_chooser, width=400, borderwidth=1, relief="ridge")
        frame_rechargetime.grid(row=2, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame_rechargetime, text="Recharge time").grid(row=0, column=0)
        tkinter.Entry(frame_rechargetime, width=4, textvariable=self.ability_recharge_time).grid(row=0, column=1)

        frame_exit_save = tkinter.Frame(frame_ability_chooser, width=400, borderwidth=1, relief="ridge")
        frame_exit_save.grid(row=3, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Button(frame_exit_save, text="Save and Exit", command=self.ability_save_and_exit).grid(row=3, column=0)

    def ability_configurer(self):
        self.ability_property_name.set({"teleport": "angle",
                                        "sloMo": "factor",
                                        "knockBack": "force",
                                        "emWave": "duration",
                                        "unShield": "amount",
                                        "None": "ability property"}[self.ability_type.get()])

    def ability_save_and_exit(self):
        if self.ability_type.get() != "None":
            hull_json["ability"]["type"] = self.ability_type.get()
            hull_json["ability"][self.ability_property_name.get()] = \
                int(self.ability_property_value.get())
            hull_json["ability"]["rechargeTime"] = \
                int(self.ability_recharge_time.get())
        self.temp_window.destroy()
        self.temp_window = None

    def insert_default_values(self):
        for key in self.entries.keys():
            self.entries[key].delete(0)
            self.entries[key].insert(0, hull_json[key])

    def posarrays_widgets(self, column, param_name, row):
        frame = tkinter.Frame(column, width=400, borderwidth=1,
                              relief=tkinter.RIDGE)
        frame.grid(row=row, column=0, sticky=sticky_we, padx=1, pady=1)
        tkinter.Label(frame, text=hull_json_descriptions[param_name]).grid(
            row=0, column=0)
        tkinter.Button(frame, command=lambda: self.posarrays_window(param_name),
                       text="...").grid(row=0, column=1)

    def posarrays_window(self, name):
        if self.temp_window is not None:
            return
        self.posarrays_name = name
        self.temp_window = tkinter.Toplevel(self, width=400)
        self.temp_window.protocol('WM_DELETE_WINDOW', self.posarrays_window_save_and_exit)
        self.temp_window.attributes('-topmost', 'true')
        frame_top = tkinter.Frame(self.temp_window)
        frame_top.grid(row=0, column=0, pady=5)
        frame_bottom = tkinter.Frame(self.temp_window)
        frame_bottom.grid(row=1, column=0, pady=5)
        self.listbox = tkinter.Listbox(frame_top)
        self.listbox.grid(row=0, column=0, padx=5)
        frame_top_right = tkinter.Frame(frame_top)
        frame_top_right.grid(row=0, column=1, padx=5)
        tkinter.Entry(frame_top_right, width=10, textvariable=self.tempPosString).grid(row=0, column=0, columnspan=2, pady=5)
        tkinter.Button(frame_top_right, command=self.posarrays_window_entrytolistbox, text="Save").grid(row=1, column=0, padx=3)
        tkinter.Button(frame_top_right, command=self.posarrays_window_listboxtoentry, text="Select").grid(row=1, column=1)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.insert(tkinter.END, "0.5 0.5"), text="Add").grid(row=0, column=0)
        tkinter.Button(frame_bottom, command=lambda: self.listbox.delete(tkinter.ACTIVE), text="Remove").grid(row=0, column=1)
        tkinter.Button(frame_bottom, command=self.posarrays_window_save_and_exit, text="Exit").grid(row=0, column=2)

    def posarrays_window_entrytolistbox(self):
        index = self.listbox.index(tkinter.ACTIVE)
        self.listbox.insert(index, self.tempPosString.get())
        self.listbox.delete(index + 1)
        self.listbox.selection_set(index)

    def posarrays_window_listboxtoentry(self):
        self.tempPosString.set(self.listbox.get(tkinter.ACTIVE))

    def posarrays_window_save_and_exit(self):
        hull_json[self.posarrays_name] = self.listbox.get(0, tkinter.END)
        self.listbox.destroy()
        self.temp_window.destroy()
        self.temp_window = None


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
