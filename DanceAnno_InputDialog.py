from tkinter import *
from tkinter import ttk


class Dialog(Toplevel):
    """
    Create a simple dialogue to rename an annotation text object
    """

    def __init__(self, parent, title, canvas_SG, item, levelId):
        """
        Initialize the GUI element

        :param parent: root window
        :param title:  Title of the dialogue
        :param canvas_SG: list of canvases to change the annotation text
        :param item: item selected for change
        :param levelId: Level A or B for annotation
        :return:
        """

        self.canvas_SG = canvas_SG
        self.item = item
        self.classId = levelId

        Toplevel.__init__(self, parent)
        self.transient(parent)

        if title:
            self.title(title)

        self.parent = parent

        self.result = None

        body = ttk.Frame(self)
        self.initial_focus = self.body(body)
        body.pack(padx=5, pady=5)

        self.buttonbox()

        self.grab_set()

        if not self.initial_focus:
            self.initial_focus = self

        self.protocol("WM_DELETE_WINDOW", self.cancel)

        self.geometry("+%d+%d" % (parent.winfo_rootx()+50,
                                  parent.winfo_rooty()+50))

        self.initial_focus.focus_set()

        self.wait_window(self)

    #
    # construction hooks

    def body(self, master):
        # create dialog body.  return widget that should have
        # initial focus.  this method should be overridden

        pass

    def buttonbox(self):
        # add standard button box. override if you don't want the
        # standard buttons

        box = ttk.Frame(self)

        w = ttk.Button(box, text="OK", width=10, command=self.ok, default=ACTIVE)
        w.pack(side=LEFT, padx=5, pady=5)
        w = ttk.Button(box, text="Cancel", width=10, command=self.cancel)
        w.pack(side=LEFT, padx=5, pady=5)

        self.bind("<Return>", self.ok)
        self.bind("<Escape>", self.cancel)

        box.pack()

    #
    # standard button semantics

    def ok(self, event=None):
        if not self.validate():
            self.initial_focus.focus_set() # put focus back
            return

        self.withdraw()
        self.update_idletasks()
        self.apply()
        self.cancel()

    def cancel(self, event=None):
        # put focus back to the parent window
        #self.parent.focus_set()
        self.canvas_SG[0].focus_set()
        self.destroy()

    def validate(self):
        return 1 # override

    def apply(self):
        pass # override

class MyDialog(Dialog):

    def body(self, master):
        Label(master, text="Label:").grid(row=0)

        self.e1 = Entry(master)
        self.e1.grid(row=0, column=1)

        return self.e1 # initial focus

    def apply(self):

        # Get the new text from the input text element
        self.newlabel = self.e1.get()

        # Get the past tags of the item
        mytags = self.canvas_SG[0].gettags(self.item)

        # New tags
        #            anntoken    1_text    anntoken_B   label    all_resize
        newtags = (mytags[0], mytags[1], mytags[2], self.newlabel, mytags[4])

        # Apply new text for the item tp all canvases
        for canvas in self.canvas_SG:
            canvas.itemconfig(self.item, text = self.newlabel, tags = newtags)
