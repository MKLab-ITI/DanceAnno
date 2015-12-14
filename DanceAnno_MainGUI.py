import os
from itertools import chain, product
import copy

from tkinter import *
from tkinter.messagebox import showerror, showinfo, askokcancel
from tkinter.filedialog import asksaveasfile

from PIL import ImageTk, Image, ImageOps

# These are in Utils folder
import sys
sys.path.append(os.path.join('.', 'Utils' ))
import writesvl
import writetxt

# These are in current path
import DanceAnno_PlotSignals        # functions to plot the signals
from DanceAnno_AnnFunctions import PlotAnnotation
from DanceAnno_BeatsLines import BeatsLines
import DanceAnno_PlayLine
import DanceAnno_MainGUI_layout # Layout configuration
import DanceAnno_ResizingCanvases



class DanceAnno:
    def __init__(self, myLoader):
        """

        :param myLoader: The data stems from DataAnno_Loader.py
            myLoader
                .signalsSelected[key]  : Dictionary of selection of signals {'Neck':1, 'Torso':0,...}, where 1 is selected
                .signals_wrapper   : Dictionary of signals {'Neck':[...], 'Torso':[....],...}
                .Fs   :   Kinect sampling rate
        :return:
        """

        # construct the root frame and its widgets
        DanceAnno_MainGUI_layout.layout(self)

        # time zoom
        self.tzoom = 1

        # data object
        self.myLoader = myLoader

        # current frame that the playline is indicating
        self.currFrame = 0

        # Status variables
        self.isPlaying = False
        self.isPaused = False
        self.isRewinded = False

        # Number of signals = 3 * selected signals
        self.nSignals = 3 * sum(v.get() == 1  for v in myLoader.signalsSelected.values())

        # Names of signals ['Left foot', 'Right foot']
        self.sgNames = [s for s in self.myLoader.signalsSelected.keys() if self.myLoader.signalsSelected[s].get() == 1]

        # Frame containing the images
        self.frame_video = DanceAnno_ResizingCanvases.ResizingVideoCanvas( self.myframe, self.mirrorizeFrame )

        # Canvas Widget for each signal
        self.canvas_SG = self.nSignals*[0]

        for i in range(self.nSignals):
            self.canvas_SG[i] = DanceAnno_ResizingCanvases.ResizingSignalCanvas(self.myframe, width = 400, height = 60,
                                                                                bg="white", highlightthickness=0)

            self.canvas_SG[i].configure(scrollregion = self.canvas_SG[i].bbox("all_resize"))
            self.canvas_SG[i].bind("<ButtonPress-1>", self.scroll_start)
            self.canvas_SG[i].bind("<ButtonRelease-1>", self.scroll_stop)
            self.canvas_SG[i].bind("<B1-Motion>", self.scroll_move)
            self.canvas_SG[i].bind("<MouseWheel>", self.onWheel)
            self.canvas_SG[i].bind("<Left>", self.leftarrowpress_callback)
            self.canvas_SG[i].bind("<Right>", self.rightarrowpress_callback)
            self.canvas_SG[i].bind("<Up>", self.uparrowpress_callback)
            self.canvas_SG[i].bind("<Down>", self.downarrowpress_callback)
            self.canvas_SG[i].bind('<Motion>', self.mousemotion)

        self.canvas_SG[0].focus_set() # This enables the buttons

        # Names of the axes ['left foot x','l f y','l f z','r f x','r f y','r f z']
        self.labels_axes = list(map(' '.join, chain(product(self.sgNames,['x','y','z']))))

        # Place the widgets in the window
        DanceAnno_MainGUI_layout.placement(self)

        # Wait a little and then initialize the variables
        self.root.after(200, self.initializeGUIVars)

        # Ignite GUI
        self.root.mainloop()

    # = Initilize GUI variables =
    def initializeGUIVars(self):

        # Handler for Playline widget
        self.playLine = self.nSignals*[0]

        # Handler for Music Beats Lines (widget)
        self.beatsLines = self.nSignals*[self.myLoader.nBeats*[0]]

        # Minimum of each signal in Y axis
        self.MinSG = self.nSignals*[0]

        # Maximum of each signal in Y axis
        self.MaxSG = self.nSignals*[0]

        # x y z line colors repeated for each joint
        self.colors = self.nSignals*['red','green','blue']

        # Number of video frames in total
        self.nTotalFrames = len(self.myLoader.indexFrames)

        # Plot signals and axis labels
        for i in range(self.nSignals):

            # length of the signal in samples
            self.Ls = len(self.myLoader.signals_wrapper[self.sgNames[i//3]][0])

            # Plot signal
            self.MinSG[i], self.MaxSG[i] = DanceAnno_PlotSignals.plotSignalJointDim(self.canvas_SG[i],
                                                              self.myLoader.signals_wrapper[self.sgNames[i//3]][i % 3],
                                                              self.colors[i], self.sgNames[i//3])
            # Plot labels for x and y
            DanceAnno_PlotSignals.plotXLabels(self.canvas_SG[i], self.Ls, self.myLoader.Fs, i, self.nTotalFrames)

            DanceAnno_PlotSignals.plotYLabels(self.canvas_SG[i], self.MinSG[i], self.MaxSG[i])

        # Handler for Play lines (array each per signal canvas)
        self.myPlayLine = DanceAnno_PlayLine.PlayLine(self.root, self, self.canvas_SG, self.playLine,
                                                      self.myLoader.indexFrames, self.myLoader.length_signal_samples)

        # Update also the video
        if self.nTotalFrames > 0:
            self.updateVideoFrame(0)

        # Init first level annotation if available (color, button to generate annotation, level indicator)
        self.myPlotAnnotationA = PlotAnnotation(self, '#0f00af', "<ButtonPress-3>", 'A')

        # Init second level annotation if available
        self.myPlotAnnotationB = PlotAnnotation(self, '#0ff00f', "b", 'B')

        # Now plot them
        self.myPlotAnnotationA.plot(self.myLoader.annotationSecs, self.myLoader.labels, self.canvas_SG,
                                   self.myLoader.Fs, self.root, self.myLoader.length_signal_samples)

        self.myPlotAnnotationB.plot(self.myLoader.annotationSecsB, self.myLoader.labelsB, self.canvas_SG,
                                   self.myLoader.Fs, self.root, self.myLoader.length_signal_samples)

        # Plot also the music beats lines if any given
        if self.myLoader.nBeats > 0:
            self.myBeatsLines = BeatsLines(self, '#777777')
            self.myBeatsLines.plot(self.root, self.canvas_SG,
                                                self.myLoader.beats,
                                                self.myLoader.Fs,
                                                self.myLoader.length_signal_samples)

        # Set the bounding box for scrolling
        for i in range(self.nSignals):
            self.canvas_SG[i].config(scrollregion = self.canvas_SG[i].bbox("all_resize"))


    # = Update the frame in Video frame widget =
    def updateVideoFrame(self, iFrame):

        if iFrame >= len(self.myLoader.indexFrames):
                return

        try:
            # Show the frame number and the time stamp of the frame
            self.str_time_info.set( str(self.myLoader.indexFrames[iFrame]) + " Frame" + "\n" + str(self.myLoader.indexFrames[iFrame]/25) + " secs" )

            # set global current frame to the frame of the video
            self.currFrame = iFrame

            # construct the image filename by concatenation
            fileiter = os.path.join(self.myLoader.dname, self.myLoader.prefixname +
                                               str(self.myLoader.indexFrames[iFrame]) + self.myLoader.videof_ext)

            # load the image
            self.frame_video.original = Image.open(fileiter)

            # image size
            size = (self.frame_video.winfo_width(), self.frame_video.winfo_height())

            # resize to current window size
            resized_image = self.frame_video.original.resize(size, Image.ANTIALIAS)

            # mirrorize the image if user wishes to
            if self.mirrorizeFrame.get() == 1:
                resized_image = ImageOps.mirror(resized_image)

            # convert image to suitable format for Tk
            self.frame_video.image = ImageTk.PhotoImage(resized_image)

            self.frame_video.aspect  = size[1] / size[0]

            # put the image to the widget
            self.frame_video.displayCanvas.create_image(0, 0, image = self.frame_video.image, anchor=NW, tags="IMG")

            # force to update the widget
            self.frame_video.update()
        except Exception as e:
            print("Unexpected update videoFrame error:", sys.exc_info()[0], sys.exc_info(), " indexFrame:", self.myLoader.indexFrames[iFrame],
                  " currFrame", self.currFrame,
                   " n", len(self.myLoader.indexFrames), " last", self.myLoader.indexFrames[-1])

    # = Play button =
    def playForwardFunctionality(self):
        self.play(1)

    def playBackwardFunctionality(self):
        self.play(-1)

    def play(self, step_frame):
        if self.isPlaying:
            self.pauseFunctionality()
            return

        self.isPlaying = True
        self.isPaused = False
        self.isRewinded = False

        if step_frame == 1:
            end_frame = len(self.myLoader.indexFrames)
        elif step_frame == -1:
            end_frame = -1

        start_frame = copy.deepcopy(self.currFrame)

        for i in range(start_frame, end_frame, step_frame):
            if self.isPlaying:
                self.currFrame = i
                self.updateVideoFrame(i)
                self.myPlayLine.updatePlayLine(i)
                #time.sleep(1/Fs)

        return

    # Stop button
    def stopFunctionality(self):
        self.isPlaying = False
        self.isPaused = False
        self.isRewinded= True

        self.currFrame = 0
        self.updateVideoFrame(self.currFrame)
        self.myPlayLine.updatePlayLine(self.currFrame)
        return

    # Pause button
    def pauseFunctionality(self):
        self.isPlaying = False
        self.isPaused   = True
        self.isRewinded= False

    # Frame Left
    def frameleftFunctionality(self):

        self.bt_frameleft.config(state=DISABLED)
        self.isPlaying = True
        self.isPaused   = True
        self.isRewinded= False
        if self.currFrame > 0:
            self.currFrame = self.currFrame - 1
            self.updateVideoFrame(self.currFrame)
            self.myPlayLine.updatePlayLine(self.currFrame)

        self.bt_frameleft.config(state=NORMAL)
        return

    #-------- Frame Right --------
    def framerightFunctionality(self):

        self.bt_frameright.config( state = DISABLED )
        self.isPlaying = True
        self.isPaused   = True
        self.isRewinded= False
        if self.currFrame < len(self.myLoader.indexFrames) -1:
            self.currFrame = self.currFrame + 1
            self.updateVideoFrame(self.currFrame)
            self.myPlayLine.updatePlayLine(self.currFrame)

        self.bt_frameright.config(state=NORMAL)
        return

    # - Scroll start -
    def scroll_start(self,event):

        for dim in range(self.nSignals):
            self.canvas_SG[dim].scan_mark(event.x, 0)

    # - Scroll stop -
    def scroll_stop(self, event):
        return

    # - Scroll move -
    def scroll_move(self,event):

        for dim in range(self.nSignals):
            self.canvas_SG[dim].scan_dragto(event.x, 0, gain=1)

    #--------- on Wheel -------------------------------
    def onWheel(self,event):

        d = event.delta

        id_el = self.canvas_SG[0].find_withtag('ENDLINE')

        x_ENDLINE = self.canvas_SG[0].coords(id_el)[0]

        id_sl = self.canvas_SG[0].find_withtag('STARTLINE')
        x_STARTLINE = self.canvas_SG[0].coords(id_sl)[0]

        # prevent coordinates width of canvas to becoming smaller than the window width of canvas
        if x_ENDLINE - x_STARTLINE < self.canvas_SG[0].winfo_width() and d <= 0:
            return
        else:
            if d < 0:
                amt = 0.95
            else:
                amt = 1.05

        for dim in range(self.nSignals):
            self.canvas_SG[dim].scale("all_resize", self.canvas_SG[dim].canvasx(self.mouse_x), 0, amt, 1)
            self.canvas_SG[dim].config(scrollregion = self.canvas_SG[dim].bbox("all_resize"))

    #----- pan left --------
    def panLeft(self):
        for dim in range(self.nSignals):
            self.canvas_SG[dim].xview_scroll(-1, UNITS)
        return

    #----- pan right --------
    def panRight(self):
        for dim in range(self.nSignals):
            self.canvas_SG[dim].xview_scroll(1, UNITS)
        return

    #----- zoom in -----------
    def zoomIn(self):
        amt = 1.05
        for dim in range(self.nSignals):
            self.canvas_SG[dim].scale("all_resize", 0, 0, amt, 1)

        return

    #------ zoom out ---------
    def zoomOut(self):
        amt = 1/1.05

        for dim in range(self.nSignals):
            self.canvas_SG[dim].scale("all_resize", 0, 0, amt, 1)

        return

    # Keypress callbacks --------

    # up arrow = frame left
    def uparrowpress_callback(self, event):
        self.frameleftFunctionality()

    # down arrow = frame right
    def downarrowpress_callback(self, event):
        self.framerightFunctionality()

    # right arrow = play forward
    def rightarrowpress_callback(self, event):

        if self.isPlaying:
            self.pauseFunctionality()
        else:
            self.playForwardFunctionality()

    # left arrow = play backward
    def leftarrowpress_callback(self, event):

        if self.isPlaying:
            self.pauseFunctionality()
        else:
            self.playBackwardFunctionality()

    # Unbind - Bind buttons to functionalities is useful because sometimes functionalities overlap
    # Bind the keyboard and mouse keys to functionalities
    def bindButtons(self):
        for dim in range(self.nSignals):
            self.canvas_SG[dim].bind("<ButtonPress-1>", self.scroll_start)
            self.canvas_SG[dim].bind("<ButtonRelease-1>", self.scroll_stop)
            self.canvas_SG[dim].bind("<B1-Motion>", self.scroll_move)
            self.canvas_SG[dim].bind("<MouseWheel>", self.onWheel)
            self.canvas_SG[dim].bind("<Left>", self.leftarrowpress_callback)
            self.canvas_SG[dim].bind("<Right>", self.rightarrowpress_callback)
            self.canvas_SG[dim].bind("<Up>", self.uparrowpress_callback)
            self.canvas_SG[dim].bind("<Down>", self.downarrowpress_callback)
            self.canvas_SG[dim].bind('<Motion>', self.mousemotion)

    # Unbind the buttons from the functionalities
    def unbindButtons(self):
        for dim in range(self.nSignals):
            self.canvas_SG[dim].unbind("<ButtonPress-1>")
            self.canvas_SG[dim].unbind("<ButtonRelease-1>")
            self.canvas_SG[dim].unbind("<B1-Motion>")
            self.canvas_SG[dim].unbind("<MouseWheel>")
            self.canvas_SG[dim].unbind("<Left>")
            self.canvas_SG[dim].unbind("<Right>")
            self.canvas_SG[dim].unbind("<Up>")
            self.canvas_SG[dim].unbind("<Down>")
            self.canvas_SG[dim].unbind('<Motion>')

    # register mouse position so that zoom in or out (by mouse wheel) is down with respect to current mouse position
    def mousemotion(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    # Open another performance
    def newSession(self):

        if askokcancel("Close", "Are you sure?"):
            self.root.destroy()
            os.system("python DanceAnno_Application.py")

        return

    # Exit
    def close_window(self):
        if askokcancel("Exit", "Are you sure?"):
            self.root.destroy()

    # Instant image update for the mirrorize frame functionality
    def refreshVideoFrame(self):
        self.updateVideoFrame(self.currFrame)

    # Show help window
    def showHelp(self):
        showinfo("Help", open('Graphics/help.txt').read())

    # Save Annotation Functionality
    # TODO: change tags so that there are not so many text comparisons
    def saveAnnotation(self):

        annotation_result = []

        # Canvas x coordinate for the starting and ending line
        x_STARTLINE = self.canvas_SG[0].coords(self.canvas_SG[0].find_withtag('STARTLINE'))[0]
        x_ENDLINE = self.canvas_SG[0].coords(self.canvas_SG[0].find_withtag('ENDLINE'))[0]

        # iterate through all annotation objects (segmentation lines and texts)
        for item in self.canvas_SG[0].find_withtag("anntoken"):

            # get all tags for this item
            tags = self.canvas_SG[0].gettags(item)

            # if the item is a segmentation line
            if any("_line" in s for s in tags): # A and B might have 1_line tag

                sequential_segmentation_index = tags[1][0:tags[1].rfind('_')] # from 5_line get 5

                # Canvas x coordinate for this item
                x_incanvas = self.canvas_SG[0].coords(item)[0]

                # Convert x coordinate to frame index
                v = int( (x_incanvas -x_STARTLINE) / (x_ENDLINE - x_STARTLINE) * self.Ls)

                # A for first level annotation, B for second level annotation
                levelId = tags[2]

                # Find the text tag for the current line item
                text_items = self.canvas_SG[0].find_withtag( sequential_segmentation_index + '_text' )

                # iterate all text items containing 5_text (it may one or two depending on the annotation levels)
                for itemPerLevel in text_items:
                    # if the item refers to the current annotation level then get the tag that is its label
                    if self.canvas_SG[0].gettags(itemPerLevel)[2] == levelId:
                        label = self.canvas_SG[0].gettags(itemPerLevel)[3]

                # append sample index, label, and annotation level indicator to a list of lists
                annotation_result.append([v, label, levelId])

        annotation_result = sorted(annotation_result)

        # print annotation result
        print("\n")
        for row in annotation_result:
            print(row)

        debug_Flag = False

        if debug_Flag:
            print("not saving in debug mode")
        else:
            # Dialogue for selecting file
            candidateSaveName = self.myLoader.dname[self.myLoader.dname.rfind("\\")+1:-8] + 'DanceAnnotationTool'
            candidateSaveName = candidateSaveName[candidateSaveName.rfind("/")+1:]
            candidateSaveName = candidateSaveName[0].upper() + candidateSaveName[1:]

            if self.myLoader.db == 'salsa':
                fhandler_saveanno = asksaveasfile(mode='w', initialdir="Data\\SVL", initialfile=candidateSaveName, defaultextension=".svl",
                                             filetypes=(
                                                        ("SVL (only one level of annotation)", "*.svl"),
                                                        ("Raw txt", "*.txt"),
                                                        ("All Files", "*.*")
                                                       )
                                                 )

            elif self.myLoader.db == 'calus':
                fhandler_saveanno = asksaveasfile(mode='w', initialdir="Data\\Calus", initialfile=candidateSaveName, defaultextension=".txt",
                                             filetypes=(
                                                        ("Raw txt", "*.txt"),
                                                        ("SVL (only one level of annotation)", "*.svl"),
                                                        ("All Files", "*.*")
                                                        )
                                                  )

            # Save to file
            if fhandler_saveanno is None: # asksaveasfile return `None` if dialog closed with "cancel".
                return #showerror("Message", "No such file")
            else:
                dummy, fextension = os.path.splitext(fhandler_saveanno.name)
                if fextension == '.txt':
                    writetxt.convertData_and_Save(fhandler_saveanno, annotation_result)
                    fhandler_saveanno.close()
                elif fextension == '.svl':
                    writesvl.convertData_and_Save(fhandler_saveanno, annotation_result, self.myLoader.Fs)
                    fhandler_saveanno.close()
                else:
                    showerror("Error","Unsupported file extension for output")
        return