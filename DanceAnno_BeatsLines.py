import tkinter as tk

class BeatsLines(tk.Tk):
    """
    Plot Beats Lines like annotation
    """

    def __init__(self, myMainGUI, color):
        """
        Initialize instance of class. They are not edible solely but the can be slided in time all together.

        :param myMainGUI: the DanceAnno_MainGUI instance
        :param color: the color of the beats lines
        :return:
        """

        self.myMainGUI = myMainGUI
        self.color = color

    def plot(self, root, canvas_SG, beats, Fs, length_signal_samples):
        """
        Plot the beats lines

        :param root: The window of the GUI
        :param canvas_SG: The list of canvases (containing each signal) to plot within
        :param beats: Beats and Labels in a dictionary (btime, blabel in self.beats.items())
        :param Fs: Sampling rate
        :param length_signal_samples: length of signal
        :return:
        """

        self.root = root
        self.canvas_SG = canvas_SG
        self.length_signal_samples = length_signal_samples
        self.beats = beats
        self.Fs = Fs

        # This data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "item": None}

        # Get the width of the canvas which is the same among canvases
        cavnw = self.canvas_SG[0].winfo_width()

        # Beat counter
        iBeat = 0

        # create movable objects
        for btime, blabel in self.beats.items():

            # Beat time (in samples)
            sampL = btime * self.Fs

            # Beat x coordinate in canvas
            xCanvas = int( float(sampL)/self.length_signal_samples * cavnw)

            # Create the beat line
            self._create_token(xCanvas, str(iBeat), blabel)

            # increment beat counter
            iBeat += 1

        # Add bindings for clicking, dragging and releasing over any object with the 'beattoken' tag
        for i in range(len(self.canvas_SG)):
            self.canvas_SG[i].tag_bind("beattoken", "<ButtonPress-1>", self.OnTokenButtonPress)
            self.canvas_SG[i].tag_bind("beattoken", "<ButtonRelease-1>", self.OnTokenButtonRelease)
            self.canvas_SG[i].tag_bind("beattoken", "<B1-Motion>", self.OnTokenMotion)
            self.canvas_SG[i].tag_bind("beattoken", "<Enter>", self.OnTokenEnter)
            self.canvas_SG[i].tag_bind("beattoken", "<Leave>", self.OnTokenLeave)
            self.canvas_SG[i].bind("v", self.OnTokenVisible)

    # Create beat line and beat label
    def _create_token(self, xCanvas, identificationCode, description):
        """
        Create the beat line and text element

        :param xCanvas: the x to plot the elements
        :param identificationCode: sequential identification number
        :param description: the beat label
        :return:
        """

        # Get the width of the canvas
        cavnh = self.canvas_SG[0].winfo_height()

        # iterate over canvases to plot the beat lines and texts
        for i in range(len(self.canvas_SG)):
            self.canvas_SG[i].create_line(xCanvas, 0, xCanvas, cavnh, fill= self.color,
                                        tags=('beattoken', identificationCode + '_line', 'all_resize'))

            self.canvas_SG[i].create_text(xCanvas, cavnh*4/5, text = description, font=("Arial", 6, "normal"),
                                        fill= self.color, anchor='w',
                                        tags=('beattoken', identificationCode + '_text', description, 'all_resize'))

    def OnTokenButtonPress(self, event):
        """
        Detect if a beat object is pressed to select all items for dragging

        :param event: x,y of event is used to find the nearest element
        :return:
        """

        # Unbind main GUI buttons
        self.myMainGUI.unbindButtons()

        # Store drag data
        self._drag_data = {"x": event.x, "item": self.canvas_SG[0].find_closest(self.canvas_SG[0].canvasx(event.x),
                                                                                self.canvas_SG[0].canvasy(event.y))[0]}

    def OnTokenButtonRelease(self, event):
        """
        End drag of an object. Reset the drag information.

        :param event: ignore
        :return:
        """
        self._drag_data = {"x": 0, "item": None}

        # Rebind the main GUI buttons because they are unbinded while dragging the beats
        self.myMainGUI.root.after(200, self.myMainGUI.bindButtons)

    def OnTokenVisible(self, event):
        """
        Changing the visibility of the beats objects on 'v' button pressed.

        :param event: ignore
        :return:
        """

        for j in range(len(self.canvas_SG)):
            items = self.canvas_SG[j].find_withtag('beattoken')  # it's the same for lines and text
            for i in items:
                # Get the state and reverse it
                state = self.canvas_SG[j].itemcget(i,'state')
                if state == 'normal':
                    self.canvas_SG[j].itemconfig(i, state='hidden')
                else:
                    self.canvas_SG[j].itemconfig(i, state='normal')


    def OnTokenMotion(self, event):
        """
        Drag all beat lines and texts.

        :param event: x to move left or right all together
        :return:
        """

        # if Playline is holded then ignore
        if self.myMainGUI.myPlayLine.isPlayLineHold:
               return

        # calculate x difference
        delta_x = event.x - self._drag_data["x"]

        # Move all beats objects (lines and texts)
        for i in range(len(self.canvas_SG)):
            for it in self.canvas_SG[i].find_withtag('beattoken'):
                self.canvas_SG[i].move(it, delta_x, 0)

        # record the new position
        self._drag_data["x"] = event.x

    def OnTokenEnter(self, event):
        self.root.config(cursor="crosshair")

    def OnTokenLeave(self, event):
        self.root.config(cursor="")
