import json
import tkinter
from tkinter import filedialog


class Application(tkinter.Frame):
    def __init__(self, master=None):
        super(Application, self).__init__(master)
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hibutton = tkinter.Button(self)
        self.hibutton["text"] = "Load Hull JSON"
        self.hibutton["command"] = loadHullJSON
        self.hibutton.pack(side="top")


def loadHullJSON():
    name = filedialog.askopenfilename(
        filetypes=[("All Files", "*"), ("JSON files", ".json")],
        parent=app,
        initialdir="~")
    # for whatever reason, askopenfilename returns either () or "" on Cancel
    if name == () or name == "":
        return
    hull_json = json.load(open(name))


app = Application()
app.master.title("DestinationSol Hull Creator")
app.master.minsize(800, 600)
app.master.resizable(False, False)
app.mainloop()
