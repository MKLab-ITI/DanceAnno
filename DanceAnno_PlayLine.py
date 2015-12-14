# Playline
class PlayLine:
    """
    The class to construct the all the playlines of the canvases
    """

    def __init__(self, root, myMainGUI, canvas_SG, playLine, indexFrames, length_signal_samples):
        """
        Initialize the variables

        :param root: The window root
        :param myMainGUI: The DanceAnno_MainGUI instance
        :param canvas_SG: A list containing all the canvases where playline is plotted
        :param playLine: An object to put the playlines handlers
        :param indexFrames: A list of integers indicating the frames as found in the folder of frame data
        :param length_signal_samples: length of samples in the signal
        :return:
        """

        self.root = root
        self.myMainGUI = myMainGUI
        self.canvas_SG = canvas_SG
        self.playLine = playLine
        self.indexFrames = indexFrames
        self.nTotalFrames = len(indexFrames)
        self.length_signal_samples = length_signal_samples

        # Is the user holding the playline by left mouse button hold down on a playline
        self.isPlayLineHold = False

        # this data is used to keep track of an item being dragged
        self._drag_data = {"x": 0, "item": None}

        # create the playlines (movable lines)
        for i in range(self.myMainGUI.nSignals):
            self.playLine[i] = self.canvas_SG[i].create_line(0, 0, 0, self.canvas_SG[i].winfo_height(),
                                    fill="#ff00ff", width=1, tags=('plline', 'SG'+str(i), 'playline', 'all_resize'))

        # Bind buttons to functionalities
        for i in range(self.myMainGUI.nSignals):
            self.canvas_SG[i].tag_bind("playline", "<ButtonPress-1>", self.OnTokenButtonPressPlayLine)
            self.canvas_SG[i].tag_bind("playline", "<ButtonRelease-1>", self.OnTokenButtonReleasePlayLine)
            self.canvas_SG[i].tag_bind("playline", "<B1-Motion>", self.OnTokenMotionPlayLine)
            self.canvas_SG[i].tag_bind("playline", "<Enter>", self.OnTokenEnterPlayLine)
            self.canvas_SG[i].tag_bind("playline", "<Leave>", self.OnTokenLeavePlayLine)

    def OnTokenButtonPressPlayLine(self, event):
        #:param event: left mouse press-hold on playline to drag line

        # disable the primary bindings of buttons in the canvas
        self.myMainGUI.unbindButtons()

        self.isPlayLineHold = True
        self._drag_data = {"x": event.x, "item": self.playLine[0]}

    def OnTokenButtonReleasePlayLine(self, event):

        self.isPlayLineHold = False
        self._drag_data = {"x": 0, "item": None}

        # enable the primary bindings of buttons in the canvas
        self.myMainGUI.root.after(200, self.myMainGUI.bindButtons)

    def OnTokenMotionPlayLine(self, event):
        """
        Drag playline functionality

        :param event: hold and move playline
        :return:
        """

        if self._drag_data["item"]!= None and self.isPlayLineHold:

            # Find Video Endline
            id_el = self.canvas_SG[0].find_withtag('VIDEOENDLINE')
            x_VIDEOENDLINE = self.canvas_SG[0].coords(id_el)[0]

            # Find Start line
            id_sl = self.canvas_SG[0].find_withtag('STARTLINE')
            x_STARTLINE = self.canvas_SG[0].coords(id_sl)[0]

            # Calculate movement length
            delta_x = self.canvas_SG[0].canvasx(event.x) - self._drag_data["x"]

            # Execute change as long as the movement is within Startline and EndVideoLine
            if delta_x + self._drag_data["x"] >= x_STARTLINE and delta_x + self._drag_data["x"] <= x_VIDEOENDLINE :

                for i in range(self.myMainGUI.nSignals):
                    self.canvas_SG[i].move( self._drag_data["item"], delta_x, 0)

                # record the new position
                self._drag_data["x"] = self.canvas_SG[0].coords(self.playLine[0])[0]

                # Find the index of Frame that correspond to this change
                self.iFrame = round(abs((self._drag_data["x"]- x_STARTLINE) / (x_VIDEOENDLINE - x_STARTLINE)) * self.nTotalFrames)

                # Update the video frame
                self.myMainGUI.updateVideoFrame(self.iFrame)

    def updatePlayLine(self, iFrame):
        """
        Update the Playline from the iFrame (when the a related play button is pressed)
        :param iFrame: The iFrame to move the playline
        :return:
        """

        id_el = self.canvas_SG[0].find_withtag('VIDEOENDLINE')
        x_VIDEOENDLINE = self.canvas_SG[0].coords(id_el)[0]

        id_sl = self.canvas_SG[0].find_withtag('STARTLINE')
        x_STARTLINE = self.canvas_SG[0].coords(id_sl)[0]

        delta_x = float(x_VIDEOENDLINE - x_STARTLINE) / self.nTotalFrames

        x_playLine_in_Canvas = self.canvas_SG[0].coords(self.playLine[0])[0]
        new_x_playLine_in_Canvas = iFrame * delta_x + x_STARTLINE

        moveX = new_x_playLine_in_Canvas - x_playLine_in_Canvas

        if new_x_playLine_in_Canvas >= x_STARTLINE and new_x_playLine_in_Canvas <= x_VIDEOENDLINE:
            for i in range(self.myMainGUI.nSignals):
                self.canvas_SG[i].move(self.playLine[i], moveX, 0)

    def OnTokenEnterPlayLine(self, event):
        """
        Change cursor icon on hover

        :param event: no use
        :return:
        """
        self.root.config(cursor="crosshair")

    def OnTokenLeavePlayLine(self, event):
        """
        Change to normal cursor

        :param event: ignore
        :return:
        """
        self.root.config(cursor="")