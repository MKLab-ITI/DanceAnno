# This class loads the data
# 1. Skeleton (.skel or .mat)
# 2. Video (a folder with frames XXXXXX_[index].png or .jpg or .jpeg
#       if you have actual video you can use ffmpeg to split it.
# 3. Choreography (.svl)
# 4. Music beats (.txt)
import os
import DanceAnno_Application

__author__ = 'DIMITRIOS'

from tkinter import *
from tkinter import ttk # ttk is a little more beautiful than tk.
from tkinter.filedialog import askopenfilename, askdirectory
from tkinter.messagebox import showerror
from tkinter import messagebox

sys.path.append( os.path.join('.', 'Utils' ))
import readsvl               # function to read svls
import readtxt               # function to read txts
import readskel              # function to read body skeleton trajectories
# if PyCharm underlines them with red, just ignore (alt+enter -> ignore)

class Loader:
    def __init__(self):

        # This variable will automatic drive the folders selection and it will shorten your clicks
        self.debug_FLAG = False
        self.db = 'salsa' # salsa or calus

        self.debug_fastaccess = 'bertrand_c3_t1'

        # Are the data loaded ?
        self.skeletonLoadedFlag = False
        self.videoLoadedFlag = False
        self.choreoLoadedFlag = False

        # GUI init
        self.root = Tk()
        self.root.configure(background='#000')
        self.root.title("Dance Annotator")

        # ask for permission to close window
        self.root.protocol("WM_DELETE_WINDOW", self.close_window)

        # Window initial dimensions
        w = 900 # The value of the width
        h = 300 # The value of the height of the window

        # Your screen width and height
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()

        # Top left corner of the window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

        # Data

        # Sampling rate of Kinect
        self.Fs = 0

        # Length of the Kinect signals
        self.length_signal_samples = 0

        # Number of music beats (optional)
        self.nBeats = 0

        # Store the index of Video frames (XXXXXXX_[index].jpg)
        self.indexFrames = []
        self.dname = ""  # directory where video frames are located
        self.prefixname = "" # the part before underscore of XXXXX_[index].jpg

        self.annotationSecs = [] # First level annotation
        self.labels = {}
        self.annotationSecsB = [] # Second level annotation
        self.labelsB = {}

        self.beats = {} # Beats indicators

        # Vars to indicate the parsing status of each file
        self.skeletonStatusSTR = StringVar()
        self.skeletonStatusSTR.set("Empty")

        self.videoStatusSTR = StringVar()
        self.videoStatusSTR.set("Empty")

        self.choreoStatusSTR = StringVar()
        self.choreoStatusSTR.set("Empty")

        self.mbeatsStatusSTR = StringVar()
        self.mbeatsStatusSTR.set("Empty")

        # Start the GUI design

        # Coloring style for ttk
        style = ttk.Style()
        style.configure("BW.TFrame", foreground="black", background="white")
        style.configure("BW.TLabel", foreground="black", background="white")
        style.configure("BW.TCheckbutton", foreground="black", background="white")


        # Frame containing the loading functionalities
        self.fr_filedialog = ttk.Frame(self.root, style="BW.TFrame")

        # Frame containing the GUI navigation processes (Continue or Exit)
        self.fr_exitcontinue = ttk.Frame(self.root, style="BW.TFrame")

        # Just some text to explain what we are doing
        self.lbl_explain = ttk.Label(self.fr_filedialog, text="Select the resources to annotate", style="BW.TLabel")

        # --- FILE SELECTION WIDGETS  ----
        # 1 SKELETON
        self.lbl_namelbl_mat_skeleton = ttk.Label(self.fr_filedialog, text="Skeleton Data", style="BW.TLabel")
        self.entry_name_mat = Entry(self.fr_filedialog)
        self.bt_mat_load = Button(self.fr_filedialog, text="...", command=self.loadSkeletonData)
        self.lbl_namelbl_hint_skeleton = ttk.Label(self.fr_filedialog, text=".mat or .skel", style="BW.TLabel")
        self.lbl_namelbl_status_skeleton = ttk.Label(self.fr_filedialog, textvariable=self.skeletonStatusSTR, style="BW.TLabel")

        #self.separatorBtSkel = ttk.Separator(self.fr_filedialog,orient=VERTICAL)

        # 2 VIDEO FRAMES
        self.lbl_namelbl_frames_video = ttk.Label(self.fr_filedialog, text="Folder with frame data", style="BW.TLabel")
        self.entry_name_frames = Entry(self.fr_filedialog)
        self.bt_frames = Button(self.fr_filedialog, text="...", command= self.loadFramesByDirectory)
        self.lbl_namelbl_hint_video = ttk.Label(self.fr_filedialog, text="A folder with jpeg, jpg, or png files", style="BW.TLabel")
        self.lbl_namelbl_status_video = ttk.Label(self.fr_filedialog, textvariable=self.videoStatusSTR, style="BW.TLabel")
        #self.separatorFramesVideo = ttk.Separator(self.fr_filedialog,orient=VERTICAL)

        # 3 CHOREOGRAPHY
        self.lbl_load_choreo = ttk.Label(self.fr_filedialog, text="Load existing choreography (Optional)", style="BW.TLabel")
        self.entry_name_choreo = Entry(self.fr_filedialog)
        self.bt_load_ch = Button(self.fr_filedialog, text="...", command= self.loadChoreography)
        self.lbl_namelbl_hint_choreo = ttk.Label(self.fr_filedialog, text="Provide an existing .txt otherwise a new one will be created", style="BW.TLabel" )
        self.lbl_namelbl_status_choreo = ttk.Label(self.fr_filedialog, textvariable=self.choreoStatusSTR, style="BW.TLabel")

        # 4 Music beats
        self.lbl_load_mbeats = ttk.Label(self.fr_filedialog, text="Load music beats (Optional)", style="BW.TLabel")
        self.entry_name_mbeats = Entry(self.fr_filedialog)
        self.bt_load_mbeats = Button(self.fr_filedialog, text="...", command= self.loadMusicBeats)
        self.lbl_namelbl_hint_mbeats = ttk.Label(self.fr_filedialog, text="Music beats in .txt format", style="BW.TLabel")
        self.lbl_namelbl_status_mbeats = ttk.Label(self.fr_filedialog, textvariable=self.mbeatsStatusSTR, style="BW.TLabel")

        self.bt_continue = Button(self.fr_exitcontinue, text="Continue", command=self.StartAnno, state = DISABLED)
        self.bt_exit = Button(self.fr_exitcontinue, text="Exit", command=self.close_window)

        # --- PLACEMENT OF WIDGETs IN THE ROOT WINDOW -------
        self.fr_filedialog.grid(row=0, column=0, columnspan=4, sticky=(N, S, E, W), padx=5)
        self.fr_exitcontinue.grid(row=1, column=0, columnspan=4, sticky=(E), ipadx=50, padx=5)

        # Explanation
        self.lbl_explain.grid(row=0, column=0, columnspan=4, rowspan=1, sticky=(E,W), padx=5)

        # Labels
        self.lbl_namelbl_mat_skeleton.grid(column=0, sticky=(W), row=1, columnspan=1, rowspan=1, pady=5, padx=5)
        self.entry_name_mat.grid(column=1, sticky=(N, S, E, W), row=1, columnspan=1, rowspan=1, pady=5, padx=5)
        self.bt_mat_load.grid(column=2, sticky=(N, S, E, W), row=1, columnspan=1, rowspan=1,  pady=5, padx=5)
        self.lbl_namelbl_hint_skeleton.grid(column=3, sticky=(W), row=1, columnspan=1, rowspan=1,  padx=5)
        self.lbl_namelbl_status_skeleton.grid(column=4, sticky=(W), row=1, columnspan=1, rowspan=1,  padx=5)
        #self.separatorBtSkel.pack(side="left", fill=Y, padx=5)

        self.lbl_namelbl_frames_video.grid(row=2, column=0, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.entry_name_frames.grid(row=2, column=1, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.bt_frames.grid(row=2, column=2, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.lbl_namelbl_hint_video.grid(row=2, column=3, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.lbl_namelbl_status_video.grid(row=2, column=4, columnspan=1, rowspan=1, sticky=(W), padx=5)
        #self.separatorFramesVideo.pack(side="left", fill=Y, padx=5)

        self.lbl_load_choreo.grid(row=3, column=0, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.entry_name_choreo.grid(row=3, column=1, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.bt_load_ch.grid(row=3, column=2, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.lbl_namelbl_hint_choreo.grid(row=3, column=3, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.lbl_namelbl_status_choreo.grid(row=3, column=4, columnspan=1, rowspan=1, sticky=(W), padx=5)

        self.lbl_load_mbeats.grid(row=4, column=0, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.entry_name_mbeats.grid(row=4, column=1, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.bt_load_mbeats.grid(row=4, column=2, columnspan=1, rowspan=1, sticky=(N, S, E, W), pady=5, padx=5)
        self.lbl_namelbl_hint_mbeats.grid(row=4, column=3, columnspan=1, rowspan=1, sticky=(W), padx=5)
        self.lbl_namelbl_status_mbeats.grid(row=4, column=4, columnspan=1, rowspan=1, sticky=(W), padx=5)


        self.bt_exit.grid(row = 0, column = 3, sticky = (E), pady = 5, padx = 15, ipadx=25)
        self.bt_continue.grid(row = 0, column = 4, sticky = (W), pady = 5, padx = 15, ipadx = 15)

        ttk.Sizegrip().grid(row=6, column=3, sticky=(E))
        #--------------------
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.fr_filedialog.columnconfigure(0, weight=1)
        self.fr_filedialog.columnconfigure(1, weight=1)
        self.fr_filedialog.columnconfigure(2, weight=1, minsize=30)
        self.fr_filedialog.columnconfigure(3, weight=1)
        self.fr_filedialog.columnconfigure(4, weight=1, minsize=100)

        # for i in range(4):
        #     self.fr_filedialog.rowconfigure(i, weight=1)

        self.root.resizable(True, True)

        # If in debugging mode then load automatically the files
        if self.debug_FLAG:
            self.loadSkeletonData()
            self.loadFramesByDirectory()
            self.loadChoreography()
            self.loadMusicBeats()

            self.root.after(1000, self.StartAnno)

        # Ignite GUI
        self.root.mainloop()
        return

    # ---   SKELETON DATA -------
    def loadSkeletonData(self):

        if self.debug_FLAG:
            if self.db == 'salsa':
                fname = 'Data\\Salsa\\performance-trajectories\\' + self.debug_fastaccess + '_kinect_1.mat'
            elif self.db == 'calus':
                fname = 'Data\\Calus\\rec.skel'
        else:

            if self.db == 'salsa':
                fname = askopenfilename(initialdir='Data\\Salsa\\performance-trajectories',
                            filetypes=(("mat file", "*.mat"),("skel file", "*.skel"), ("All files", "*.*") ))
            elif self.db == 'calus':
                fname = askopenfilename(initialdir='Data\\Calus',
                                    filetypes=(("skel file", "*.skel"), ("mat file", "*.mat"), ("All files", "*.*") )) #performance-trajectories

        if fname:
            try:

                self.entry_name_mat.insert(0, "..." + fname[-30:])

                dummy, fextension = os.path.splitext(fname)
                # ------- load skeleton trajectories -----------------------
                if fextension=='.mat':
                    self.signals_wrapper, self.Fs = readskel.readmatlab_wrapper(fname)
                else: # .skel
                    self.signals_wrapper, self.Fs = readskel.skelparser(fname)


                nJoints = len(self.signals_wrapper)
                sigA = next(iter(self.signals_wrapper.values()))
                nTrajects = len(sigA[0])

                self.skeletonStatusSTR.set(str(nTrajects) + " trajects")

                self.skeletonLoadedFlag = True
                self.checkContinueEnable()

                # global Fs, length_signal_samples
                self.length_signal_samples = nTrajects

                # put a separation line
                separatorBtsA = ttk.Separator(self.fr_filedialog, orient=HORIZONTAL)
                separatorBtsA.grid(row=5, column=0, columnspan=5, sticky="WE")

                # show available joints
                self.signalsSelected = {}
                self.chb_joint = {}
                i = 0
                for key,v in sorted(self.signals_wrapper.items()):

                    self.signalsSelected[key] = IntVar()

                    if key in ('Left foot', 'Right foot'):
                        self.signalsSelected[key].set(1)

                    self.chb_joint[key] = ttk.Checkbutton(self.fr_filedialog, text = key, variable = self.signalsSelected[key], style="BW.TCheckbutton")
                    self.chb_joint[key].grid(row=6 + i % 10, column=1+i//10, columnspan=1, rowspan=1, sticky=(W))
                    i += 1

                #make my screen dimensions work
                w = 900 #The value of the width
                h = 300 + 12*22 #The value of the height of the window

                ws = self.root.winfo_screenwidth()#This value is the width of the screen
                hs = self.root.winfo_screenheight()#This is the height of the screen

                # calculate position x, y
                x = (ws/2) - (w/2)
                y = (hs/2) - (h/2)

                self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

                #self.root.mainloop()

            except Exception as e:                      # <- naked except is a bad idea
                self.skeletonLoadedFlag = False
                self.checkContinueEnable()
                print(e)
                showerror("Open Source File", "Failed to read file\n'%s'\n'%s'" % (fname, e))
                return
        return

    #=========== Load directory of frames ======================================
    def loadFramesByDirectory(self):

        if self.debug_FLAG:
            if self.db == 'salsa':
                self.dname = "Data\\Salsa\\Videos\\" + self.debug_fastaccess + "_kinect_1"
            elif self.db == 'calus':
                self.dname = "Data\\Calus\\frames"
        else:
            if self.db == 'salsa':
                self.dname = askdirectory(initialdir='Data\\Salsa\\Videos')
            elif self.db == 'calus':
                self.dname = askdirectory(initialdir='Data\\Calus')

        if self.dname:
            try:
                self.entry_name_frames.insert(0,"..." + self.dname[-30:])
                self.indexFrames = []

                for file in os.listdir(self.dname):

                    dum, self.checkvideof_ext = os.path.splitext(file)

                    if self.checkvideof_ext in ('.jpeg', '.JPG', '.JPEG', '.png', '.bmp', '.PNG', '.BMP'):

                        dum, self.videof_ext = os.path.splitext(file)

                        k = file.rfind("_")
                        l = file.rfind(".")

                        iFrame = file[k+1:l]

                        if iFrame[0] == 'f':
                            iFrame = iFrame[1:]
                            self.indexFrames.append(int(iFrame))
                            self.prefixname = file[:k+2]
                        else:
                            self.indexFrames.append(int(iFrame))
                            self.prefixname = file[:k+1]

                        self.indexFrames = sorted(self.indexFrames)
                        self.videoStatusSTR.set( str(len(self.indexFrames)) + " Frames" )
                        self.videoLoadedFlag = True
                    elif file in ('Thumbs.db'):
                        continue
                    else:
                        showerror("Fail", "Only jpeg, jpg, JPG, bmp, BMP, png, PNG frames are supported")
                        self.videoLoadedFlag = False
                        return

                self.checkContinueEnable()

            except Exception as e:                     # <- naked except is a bad idea
                self.videoLoadedFlag = False
                self.checkContinueEnable()
                showerror("Error", ("Open Source File\n'%s'" % e)  + "\n" + ("Failed to open directory\n'%s'" % self.dname))
                return
        return


    # ===========  LOAD SVL CHOREOGRAPHY ===============================
    def loadChoreography(self):

        if self.debug_FLAG:
            if self.db == 'salsa':
                tempf =self.debug_fastaccess
                tempf = list(tempf)
                tempf[0] = tempf[0].upper()
                tempf = ''.join(tempf)

                fname = "Data\\Salsa\\SVL\\" + tempf + "_DanceAnnotationTool.svl"

            elif self.db == 'calus':
                fname = "Data\\Calus\\DanceAnnotationTool.txt"
        else:
            if self.db == 'salsa':
                fname  = askopenfilename(initialdir='Data\\Salsa\\SVL', filetypes=(("svl file", "*.svl"), ("txt file", "*.txt"), ("All files", "*.*") ))
            elif self.db == 'calus':
                fname  = askopenfilename(initialdir='Data\\Calus', filetypes=(("txt file", "*.txt"), ("svl file", "*.svl"), ("All files", "*.*") ))



        dummy, fextension = os.path.splitext(fname)

        if fname:
            try:
                if fextension == '.svl':
                    params, self.annotationSecs, self.labels = readsvl.extractSvlAnnotRegionFile(fname)
                    self.entry_name_choreo.insert(0,"..." + fname[-30:])
                    self.choreoStatusSTR.set(str(len(self.labels)) + " labels")
                    self.choreoLoadedFlag = True
                    self.checkContinueEnable()
                elif fextension == '.txt':
                    self.annotationSecs, self.labels, self.annotationSecsB, self.labelsB = readtxt.parse(fname)
                    self.entry_name_choreo.insert(0,"..." + fname[-30:])
                    self.choreoStatusSTR.set(str(len(self.labels)) + " labels")
                    self.choreoLoadedFlag = True
                    self.checkContinueEnable()
                else:
                    showerror("Waring", "Parser does not exists for such a file, only svl or txt are supported")

            except Exception as e:
                self.choreoLoadedFlag = False
                self.checkContinueEnable()
                msg = "There was a problem in loading!\n'%s'" % e
                if messagebox.askyesno("Error", msg + "\n" + "Do you want to choose another file?"):
                    self.loadChoreography()
                else:
                    return
        return

    #=================== Music beats ========================================
    def loadMusicBeats(self):

        if self.debug_FLAG:
            if self.db=='salsa':
                fname = 'Data\\Salsa\\MusicBeats\\' + self.debug_fastaccess + '_feetcam-beats.txt'
            else:
                fname = None
        else:
            fname = askopenfilename(initialdir='Data\\Salsa\\MusicBeats',
                                 filetypes=(("beats file", "*.txt"), ("All files", "*.*") )) #performance-trajectories

        if fname:
            try:
                self.entry_name_mbeats.insert(0, "..." + fname[-30:])
                dummy, fextension = os.path.splitext(fname)

                # ------- load skeleton trajectories -----------------------
                if fextension=='.txt':
                    self.beats = readtxt.parse_mbeats(fname)
                else:
                    showerror("Error","Only txt file extension is supported")
                    return

                self.nBeats = len(self.beats)
                self.mbeatsStatusSTR.set(str(self.nBeats) + " Beats")

            except Exception as e:                      # <- naked except is a bad idea
                showerror("Open Source File", "Failed to read file\n'%s'\n'%s'" % (fname, e))
                return
        return


    def close_window(self):
        #if messagebox.askokcancel("Exit", "Are you sure?"):
        self.root.destroy()

    def StartAnno(self):
        self.root.destroy()
        DanceAnno_Application.Application.StartAnnotating(self)

    def checkContinueEnable(self):
        if self.skeletonLoadedFlag and self.videoLoadedFlag: # and self.choreoLoadedFlag:
            self.bt_continue.config(state = NORMAL)