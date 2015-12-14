from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image, ImageOps

class ResizingSignalCanvas(Canvas):
    """
    A subclass of Canvas for dealing with resizing of main Window.
    """

    def __init__(self, parent, **kwargs):
        """
        Initialize Canvas

        :param parent: The parent object (the Frame of the MainGUI)
        :param kwargs: input arguments for decorating (width = 400, height = 60,bg="white", highlightthickness=0)
        :return:
        """

        Canvas.__init__(self,parent,**kwargs)

        # Set on_resize function when the canvas size should reconfigured
        self.bind("<Configure>", self.on_resize)

        # Get the "natural" width and the height of the canvas. The natural size is the minimal size needed to display
        # the widget’s contents, including padding, borders, etc.
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        #self.addtag_above(self, "canvas")

    def on_resize(self, event):
        """
        On resizing canvas

        :param event: get the new event width and height (of the canvas)
        :return:
        """

        # Determine the ratio of old width/height to new width/height
        wscale = float(event.width)/self.width
        hscale = float(event.height)/self.height

        # Assign the new to the old one
        self.width = event.width
        self.height = event.height

        # resize the canvas
        self.config(width=self.width, height=self.height)

        # rescale all the objects tagged with the "all_resize" tag
        self.scale("all_resize", 0, 0, wscale, hscale)

        # Set the bounding box for scrolling
        self.config(scrollregion = self.bbox("all_resize"))


class ResizingVideoCanvas(ttk.Frame):
    """
    A subclass of ttk.Frame for dealing with resizing frames based on window resize. Inside the frame, the canvas is
    set where image is drawn.
    """

    def __init__(self, master, mirrorizeFrame):
        """
        Initialize the Frame

        :param master: myFrame
        :param mirrorizeFrame: Option to mirrorize the image
        :return:
        """

        # Initialize the parent class
        Frame.__init__(self, master)

        # Set option to mirrorize the image
        self.mirrorizeFrame = mirrorizeFrame

        # Set a float to store the original aspect. Value of aspect is set inside DanceAnno_MainGUI.
        self.aspect = 0

        # Place the frame to the original frame to a certain position
        self.grid(column=2, row=0,  columnspan=1, rowspan=2, sticky=(N, S, E, W), pady=5, padx=25)

        # Construct the canvas where image is displayed
        self.displayCanvas = Canvas(self, bd=0, highlightthickness=0)
        self.displayCanvas.grid(row=0, column=0, sticky=W + E + N + S)

        # Set on resize function
        self.bind("<Configure>", self.resize)

    def resize(self, event):

        # target size
        size = (event.width, event.height)

        if self.aspect > 0:

            # resize image based on target size
            resizedImage = self.original.resize(size, Image.ANTIALIAS)

            if self.mirrorizeFrame.get() == 1:
                resizedImage = ImageOps.mirror(resizedImage)

            # transform the resizedImage to the PhotoImage
            self.image = ImageTk.PhotoImage(resizedImage)

            # Delete previous and put new image
            self.displayCanvas.delete("IMG")
            self.displayCanvas.create_image(0, 0, image=self.image, anchor=NW, tags="IMG")