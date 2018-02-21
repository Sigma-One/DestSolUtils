import json
import tkinter
from tkinter import filedialog

sticky_we = tkinter.W+tkinter.E


item_json_descriptions = None
item_json = None

left_column = None
right_column = None

with open("ItemCreator/gunJsonDescriptions.json") as file:
    gun_json_descriptions = json.load(file)
with open("ItemCreator/clipJsonDescriptions.json") as file:
    clip_json_descriptions = json.load(file)
with open("ItemCreator/armorJsonDescriptions.json") as file:
    armor_json_descriptions = json.load(file)
with open("ItemCreator/shieldJsonDescriptions.json") as file:
    shield_json_descriptions = json.load(file)

with open("ItemCreator/defaultGun.json") as file:
    gun_json = json.load(file)
with open("ItemCreator/defaultClip.json") as file:
    clip_json = json.load(file)
with open("ItemCreator/defaultArmor.json") as file:
    armor_json = json.load(file)
with open("ItemCreator/defaultShield.json") as file:
    shield_json = json.load(file)

#item_type = None

class Application(tkinter.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.item_type = None
        self.temp_window = None
        self.entries = {}
        self.checkboxes = {}
        self.pack(anchor="n")

        # Create menubar
        self.menubar_widgets()

        self.choose_type()
        #self.create_widgets()

    def create_widgets(self):

        self.entries = {}
        self.frame.destroy()

        global left_column
        global right_column
        global item_json_descriptions
        global item_json

        # create columns
        left_column = tkinter.Frame(self, width=400, height=360)
        left_column.grid(row=0, column=0, sticky=tkinter.N)
        right_column = tkinter.Frame(self, width=400, height=360)
        right_column.grid(row=0, column=1, sticky=tkinter.N)

        print("Type Set: ", self.item_type)

        # Int/Float/String fields

        if self.item_type == "gun":

            item_json_descriptions = gun_json_descriptions

            self.entry_widgets(left_column, "maxAngleVar", 4, 0)
            self.entry_widgets(left_column, "angleVarDamp", 3, 1)
            self.entry_widgets(left_column, "angleVarPerShot", 7, 2)
            self.entry_widgets(left_column, "timeBetweenShots", 10, 3)
            self.entry_widgets(left_column, "reloadTime", 3, 4)
            self.entry_widgets(left_column, "price", 3, 5)
            self.entry_widgets(left_column, "gunLength", 4, 6)
            self.entry_widgets(left_column, "clipName", 10, 7)
            self.entry_widgets(left_column, "displayName", 10, 8)

            self.checkbox_widgets(right_column, "lightOnShot", 0)
            self.array_widgets(right_column, "shootSounds", 1)
            self.array_widgets(right_column, "reloadSounds", 2)

        elif self.item_type == "shield":

            item_json_descriptions = shield_json_descriptions

            self.entry_widgets(left_column, "maxLife", 3, 0)
            self.entry_widgets(left_column, "idleTime", 3, 1)
            self.entry_widgets(left_column, "regenSpd", 3, 2)
            self.entry_widgets(left_column, "bulletDmgFactor", 10, 3)
            self.entry_widgets(left_column, "energyDmgFactor", 3, 4)
            self.entry_widgets(right_column, "explosionDmgFactor", 3, 5)
            self.entry_widgets(right_column, "price", 4, 6)
            self.entry_widgets(right_column, "displayName", 10, 7)
            self.entry_widgets(right_column, "absorbSound", 10, 8)
            self.entry_widgets(right_column, "absorbSoundPitch", 3, 8)

        elif self.item_type == "armor":

            item_json_descriptions = armor_json_descriptions

            self.entry_widgets(left_column, "price", 3, 0)
            self.entry_widgets(left_column, "perc", 3, 1)
            self.entry_widgets(left_column, "displayName", 10, 2)

            self.array_widgets(right_column, "bulletHitSounds", 0)
            self.array_widgets(right_column, "energyHitSounds", 1)
            self.entry_widgets(left_column, "baseSoundPitch", 3, 2)

        elif self.item_type == "clip":

            item_json_descriptions = clip_json_descriptions

            self.entry_widgets(left_column, "price", 3, 0)
            self.entry_widgets(left_column, "displayName", 10, 1)
            self.entry_widgets(left_column, "plural", 10, 2)
            self.entry_widgets(left_column, "iconName", 10, 3)

            self.entry_widgets(right_column, "size", 3, 0)
            self.checkbox_widgets(right_column, "infinite", 1)

        else:
            print("How did you even choose an invalid type?")


        # Default values for entry fields
        self.insert_default_values()

    def choose_type(self):
        try:
            right_column.destroy()
            left_column.destroy()
        except AttributeError:
            print("No column(s)")

        self.frame = tkinter.Frame(self)
        self.frame.grid()

        def choose(chosen_type):
            global item_json
            self.item_type = chosen_type
            if self.item_type == "gun":
                item_json = gun_json

            elif self.item_type == "clip":
                item_json = clip_json

            if self.item_type == "shield":
                item_json = shield_json

            elif self.item_type == "armor":
                item_json = armor_json

            self.create_widgets()

        tkinter.Button(self.frame, command=lambda: choose("shield"), text="Shield").grid(row=0, sticky=sticky_we)
        tkinter.Button(self.frame, command=lambda: choose("gun"), text="Gun").grid(row=1, sticky=sticky_we)
        tkinter.Button(self.frame, command=lambda: choose("armor"), text="Armor").grid(row=2, sticky=sticky_we)
        tkinter.Button(self.frame, command=lambda: choose("clip"), text="Clip").grid(row=3, sticky=sticky_we)

    # right column items

    # Checkbox widgets
    def checkbox_widgets(self, column, param_name, frame_row):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=frame_row, column=0, sticky=sticky_we, padx=1, pady=1)

        self.checkboxes[param_name] = tkinter.IntVar()

        tkinter.Label(frame, text=item_json_descriptions[param_name]).grid(row=0, column=0)

        tkinter.Checkbutton(frame, variable=self.checkboxes[param_name]).grid(row=0, column=1)

    # array widgets
    def array_widgets(self, column, param_name, frame_row):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=frame_row, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame, text=item_json_descriptions[param_name]).grid(row=0, column=0)
        tkinter.Button(frame, command=lambda: self.array_builder(param_name), text="...").grid(row=0, column=1)

    # left column items

    # entry fields for different properties
    def entry_widgets(self, column, param_name, entry_width, frame_row):
        frame = tkinter.Frame(column, width=400, borderwidth=1, relief="ridge")
        frame.grid(row=frame_row, column=0, sticky=sticky_we, padx=1, pady=1)

        tkinter.Label(frame, text=item_json_descriptions[param_name]).grid(row=0, column=0)

        self.entries[param_name] = tkinter.Entry(frame, width=entry_width)
        self.entries[param_name].grid(row=0, column=1)

    # other widgets

    # menubar
    def menubar_widgets(self):
        menubar = tkinter.Menu()
        self.master.config(menu=menubar)

        file_menu = tkinter.Menu(menubar)
        edit_menu = tkinter.Menu(menubar)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        file_menu.add_command(label="Import Item", command=loadItemJSON)
        file_menu.add_command(label="Export Item", command=dumpItemJSON)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=exit)

        edit_menu.add_command(label="Change Type | WARNING: Clears all fields!", command=self.choose_type)

    # array maker
    def array_builder(self, field_name):
        def save_exit(field_name, listbox):
                item_json[field_name] = listbox.get(0, tkinter.END)

        self.array_window = tkinter.Toplevel(self)
        self.array_window.minsize(200, 150)
        self.array_window.resizable(False, False)
        self.array_window.attributes('-topmost', 'true')

        left_column = tkinter.Frame(self.array_window)
        left_column.grid(row=0, column=0, pady=5)
        right_column = tkinter.Frame(self.array_window)
        right_column.grid(row=0, column=1, pady=5)

        self.listbox = tkinter.Listbox(left_column)
        self.listbox.grid(row=0, column=0, padx=5)

        self.input_field = tkinter.Entry(right_column)
        self.input_field.grid(row=0, column=0, padx=5, columnspan=2)
        tkinter.Button(right_column, command=lambda: self.listbox.insert(tkinter.END, self.input_field.get()), text="Add").grid(row=1, column=0, sticky=sticky_we)
        tkinter.Button(right_column, command=lambda: self.listbox.delete(tkinter.ACTIVE), text="Remove").grid(row=1, column=1, sticky=sticky_we)
        tkinter.Button(right_column, command=lambda: save_exit(field_name, self.listbox), text="Save").grid(row=2, column=0, sticky=sticky_we)
        tkinter.Button(right_column, command=lambda: self.array_window.destroy(), text="Close").grid(row=2, column=1, sticky=sticky_we)

    # inserts default values into fields
    def insert_default_values(self):
        global item_json
        for key in self.entries.keys():
            self.entries[key].delete(0)
            self.entries[key].insert(0, item_json[key])

def loadItemJSON():

    global item_json
    name = filedialog.askopenfilename(filetypes=[("JSON files", ".json"), ("All Files", "*")], parent=app, initialdir="~")
    # for whatever reason, filedialogs returns either () or "" on Cancel
    if name == () or name == "":
        return

    with open(name) as file:
        jsonFile = json.load(file)


    if jsonFile.keys() == gun_json.keys():
        app.item_type = "gun"
        print("Item file detected: Gun")
    elif jsonFile.keys() == clip_json.keys():
        app.item_type = "clip"
        print("Item file detected: Clip")
    elif jsonFile.keys() == armor_json.keys():
        app.item_type = "armor"
        print("Item file detected: Armor")
    elif jsonFile.keys() == shield_json.keys():
        app.item_type = "shield"
        print("Item file detected: Shield")

    item_json = jsonFile
    app.create_widgets()


def dumpItemJSON():
    global item_json
    # for whatever reason, filedialogs returns either () or "" on Cancel
    export_file_name = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], initialdir="~", parent=app)
    if export_file_name == "" or export_file_name == ():
        return
    app_entries = {k: v.get() for k, v in app.entries.items()}
    item_json.update(app_entries)

    for box in app.checkboxes.keys():
        item_json[box] = app.checkboxes[box].get() == 1

    with open(export_file_name, "w") as export_file:
        json.dump(item_json, export_file, indent=2, sort_keys=True)


app = Application()
app.master.title("DestinationSol Item Creator")
app.master.minsize(800, 360)
app.master.resizable(False, False)
app.mainloop()
