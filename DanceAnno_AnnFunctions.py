import tkinter as tk
import DanceAnno_InputDialog

class PlotAnnotation(tk.Tk):
    """
    Plot annotation lines. Two levels of annotation are supported, A and B. Each level is denoted by an instance of this
    class with different levelId
    """

    def __init__(self, myMainGUI, color, create_button, levelId):
        """
        Initialize parameters

        :param myMainGUI: The instance of the DanceAnno_MainGUI
        :param color: Color to give to the segmentation lines
        :param create_button: Mouse or Keyboard button that generates the segmentation line
        :param levelId: 'A' for first levelId and 'B' for second levelId
        :return:
        """

        self.myMainGUI = myMainGUI
        self.color = color
        self.create_button = create_button
        self.levelId = levelId

    def plot(self, annotationSecs, labels, canvas_SG, Fs, root, length_signal_samples):
        """
        Plot segmentation lines from previous annotation (annotationSecs, labels). The changes that will be made are
        taken from the canvas elements.

        :param annotationSecs: annotation timestamps
        :param labels: labels per annotation timestamp
        :param canvas_SG: list of canvases
        :param Fs: Sampling rate
        :param root: root of the window
        :param length_signal_samples: Total length of signal
        :return:
        """

        self.annotationSecs = annotationSecs

        # labels are only when annotation is already loaded. Otherwise labels are taken from tags
        self.labels = labels
        self.iStep = 0

        self.canvas_SG = canvas_SG
        self.Fs = Fs
        self.root = root
        self.length_signal_samples = length_signal_samples

        # this data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "item": None}

        # The width of the canvas
        cavnw = self.canvas_SG[0].winfo_width()

        # create the segmentation lines
        if (annotationSecs is not None):
            for i in range(len(annotationSecs)):

                xCanvas = int( float(annotationSecs[i] * Fs)/self.length_signal_samples * cavnw)

                self._create_token( xCanvas, str(i), self.labels[i])

            # the last step index where user can add steps
            self.iStep = len(annotationSecs)

        # Add bindings to canvas for clicking, dragging and releasing over any object with the "anntoken" tag
        for i in range(len(self.canvas_SG)):
            self.canvas_SG[i].tag_bind("anntoken", "<ButtonPress-1>", self.OnTokenButtonPress)
            self.canvas_SG[i].tag_bind("anntoken", "<ButtonRelease-1>", self.OnTokenButtonRelease)
            self.canvas_SG[i].tag_bind("anntoken", "<B1-Motion>", self.OnTokenMotion)
            self.canvas_SG[i].tag_bind("anntoken", "<Enter>", self.OnTokenEnter)
            self.canvas_SG[i].tag_bind("anntoken", "<Leave>", self.OnTokenLeave)
            self.canvas_SG[i].bind("d", self.OnTokenDelete)
            self.canvas_SG[i].bind(self.create_button, self.OnTokenButtonPressB)

    def _create_token(self, xCanvas, identificationCode, description):
        """
        Create segmentation line and text label

        :param xCanvas: x coordinate in the canvas to plot the line
        :param identificationCode: number indicating the index of segmentation line
        :param description: the annotation actually
        :return:
        """

        # Canvas height
        cavnh = self.canvas_SG[0].winfo_height()

        # Iterate over canvases to plot the line and the text
        for dim in range(len(self.canvas_SG)):

            # Line
            self.canvas_SG[dim].create_line(xCanvas, 0, xCanvas, cavnh, fill=self.color,
                                            tags=('anntoken', identificationCode + '_line', 'anntoken_' + self.levelId, 'all_resize'))
            # Text
            self.canvas_SG[dim].create_text(xCanvas + 1, cavnh * 1 / 2, text = description, font=("Arial", 6, "normal"), fill= self.color, anchor='w',
                                            tags=('anntoken', identificationCode + '_text', 'anntoken_' + self.levelId, description, 'all_resize'))

    def OnTokenButtonPress(self, event):
        """
        On left mouse press over segmentation line make it selected

        :param event: detect x and y of the mouse
        :return:
        """
        x = self.canvas_SG[0].canvasx(event.x)
        y = self.canvas_SG[0].canvasy(event.y)

        # Find the closest segmentation line on the x and y of the mouse click
        self._drag_data = {"x": event.x, "item": self.canvas_SG[0].find_closest(x, y)[0]}

    def OnTokenButtonPressB(self, event):
        """
        Right mouse click generates a new segmentation line or renames the closest one if exists

        :param event: event used to find the x and y of the mouse click
        :return:
        """

        # Find the x and y in the canvas that was clicked
        x = self.canvas_SG[0].canvasx(event.x)
        y = self.canvas_SG[0].canvasy(event.y)

        # Find closest item
        item = self.canvas_SG[0].find_closest(x, y)[0]

        if self.canvas_SG[0].gettags(item)[0] != 'anntoken':
            # Create a new segmentation line
            self._create_token(x, str(self.iStep), 'Step ' + str(self.iStep + 1))

            # Update the last index
            self.iStep += 1
        else:
            # Rename the old one using a dialogue GUI
            DanceAnno_InputDialog.MyDialog(self.root, "Input", self.canvas_SG, item, self.levelId)

    def OnTokenButtonRelease(self, event):
        """
        End drag of an object. Reset the drag information.

        :param event: ignore
        :return:
        """

        self._drag_data = {"x": 0, "item": None}
        self.myMainGUI.root.after(200, self.myMainGUI.bindButtons)

    def OnTokenDelete(self, event):
        """
        Delete a segmentation line closest to the mouse cursor by pressing 'd' key. The algorithms deletes the line and
        the text simultaneously.

        :param event: ignore
        :return:
        """
        x = self.canvas_SG[0].canvasx(self.myMainGUI.mouse_x)
        y = self.canvas_SG[0].canvasy(self.myMainGUI.mouse_y)

        # Find the item to delete
        itemd = self.canvas_SG[0].find_closest(x, y)[0]

        # Get item tags
        tagslist = self.canvas_SG[0].gettags(itemd)

        # Continue only if the item selected is an annotation object (text or line)
        if 'anntoken' in tagslist:

            # Find its levelId, i.e. either 'anntoken_A' or 'anntoken_B'
            levelId = tagslist[2]

            # Find all annotation texts and lines that match tagslist
            tag_item_text = [stext for stext in tagslist if "_text" in stext] + \
                            [sline for sline in tagslist if "_line" in sline]

            # Find the text tag
            tag_item_text = tag_item_text[0]

            # Isolated the id [id]_text
            pos_of_underscore = tag_item_text.rfind('_')
            id = tag_item_text[0:pos_of_underscore]

            # Iterate over all canvases
            for dim in range(len(self.canvas_SG)):

                # Iterate to match the current levelId (it contains both for A and B levels)
                itemtexts = self.canvas_SG[dim].find_withtag(id + '_text')
                itemlines = self.canvas_SG[dim].find_withtag(id + '_line')

                for itemtext in itemtexts:
                    if self.canvas_SG[dim].gettags(itemtext)[2] == levelId:
                        self.canvas_SG[dim].delete(itemtext)

                for itemline in itemlines:
                    if self.canvas_SG[dim].gettags(itemline)[2] == levelId:
                        self.canvas_SG[dim].delete(itemline)


    def OnTokenMotion(self, event):
        """
        Move Annotation Line

        :param event: Use to calculate the drag
        :return:
        """

        self.myMainGUI.unbindButtons()

        # if Playline is holded then ignore
        if self.myMainGUI.myPlayLine.isPlayLineHold:
               return

        # Calculte difference
        delta_x = event.x - self._drag_data["x"]

        # Get the item to drag
        item = self._drag_data["item"]

        # Get selected item tags
        tags = self.canvas_SG[0].gettags(item)

        # xxx_line or xxx_text
        idtag = tags[1]

        # anntoken_A or anntoken_B
        levelId = tags[2]

        # xxx from xxx_line or xxx_text
        id = idtag[0:idtag.rfind('_')]

        # move text or line (depends which is selected)
        for i in range(len(self.canvas_SG)):

            itemtexts = self.canvas_SG[i].find_withtag(id + '_text')  # it contains both for A and B levels
            itemlines = self.canvas_SG[i].find_withtag(id + '_line')

            for itemtext in itemtexts:
                if self.canvas_SG[0].gettags(itemtext)[2] == levelId:
                    self.canvas_SG[i].move(itemtext, delta_x, 0)

            for itemline in itemlines:
                if self.canvas_SG[0].gettags(itemline)[2] == levelId:
                    self.canvas_SG[i].move(itemline, delta_x, 0)

        # record the new position
        self._drag_data["x"] = event.x

    def OnTokenEnter(self, event):
        # Change cursor icon on hover above item
        self.root.config(cursor="crosshair")

    def OnTokenLeave(self, event):
        # Change cursor icon on hover out of item
        self.root.config(cursor="")