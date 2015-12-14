from tkinter import *
from tkinter import ttk
from PIL import ImageTk

def layout(mGUI):

    mGUI.root = Tk()
    mGUI.root.configure(background='#000')
    mGUI.root.title("Dance Annotator")
    mGUI.root.protocol("WM_DELETE_WINDOW", mGUI.close_window)

    # Window initial width and height
    w = 1000
    h = 750

    # Screen width and height
    ws = mGUI.root.winfo_screenwidth()
    hs = mGUI.root.winfo_screenheight()

    # Use the themed tk to make more nice widgets
    style = ttk.Style()
    style.configure("BW.TFrame", foreground="black", background="white")
    style.configure("BW.TLabel", foreground="black", background="white", font=('Helvetica', 12, 'bold'))
    style.configure("BW.TCheckbutton", foreground="black", background="white")
    style.configure('BW.TButton', highlightthickness='10', font=('Helvetica', 8, 'bold'))
    # More styling of the buttons
    style.map("BW.TButton",
              foreground=[('disabled', 'gray'), ('pressed', 'green'), ('active', 'blue')],
        background=[('disabled', 'black'), ('pressed', '!focus', 'cyan'), ('active', 'white')],
        highlightcolor=[('focus', 'green'), ('!focus', 'red')],
        relief=[('pressed', 'groove'), ('!pressed', 'ridge')])

    # top left position of the window
    x = (ws/2) - (w/2) # top
    y = (hs/2) - (h/2) # left

    mGUI.root.geometry('%dx%d+%d+%d' % (w, h, x, y))

    # The frame
    mGUI.myframe = ttk.Frame(mGUI.root, style="BW.TFrame")

    # The timeline buttons
    mGUI.fr_buttons = ttk.Frame(mGUI.myframe, style="BW.TFrame")

    # The widget to show time info
    mGUI.str_time_info = StringVar()
    mGUI.str_time_info.set(" ")
    mGUI.lbl_infoTime = ttk.Label(mGUI.fr_buttons, textvariable = mGUI.str_time_info, width=15, style="BW.TLabel")

    # The widget to mirror video frames
    mGUI.mirrorizeFrame = IntVar()
    mGUI.mirrorizeFrame.set(1)
    mGUI.chb_framemirrorize = ttk.Checkbutton(mGUI.myframe, text = "Mirrorize", variable = mGUI.mirrorizeFrame,
                                              command = mGUI.refreshVideoFrame, style ='BW.TCheckbutton')

    # HELP - SAVE - NEW - EXIT BUTTONs
    mGUI.save_img = ImageTk.PhotoImage(file="Graphics/save.png")
    mGUI.newsession_img = ImageTk.PhotoImage(file="Graphics/newsession.png")
    mGUI.exit_img = ImageTk.PhotoImage(file="Graphics/exit.png")

    mGUI.bt_save = ttk.Button(mGUI.myframe, compound=LEFT, image = mGUI.save_img, text="Save as",
                              command= mGUI.saveAnnotation, width=20, style="BW.TButton")
    mGUI.bt_help = ttk.Button(mGUI.myframe, compound=LEFT, text="Help", command= mGUI.showHelp, width=18, style="BW.TButton")
    mGUI.bt_newsession = ttk.Button(mGUI.myframe, compound=LEFT, image = mGUI.newsession_img, text="New session",
                                    command = mGUI.newSession, width=18, style="BW.TButton")
    mGUI.bt_exit = ttk.Button(mGUI.myframe, compound=LEFT, image = mGUI.exit_img, text="Exit",
                              command = mGUI.close_window, width=20, style="BW.TButton")

    # TIME ZOOM-PAN BUTTONs
    mGUI.bt_panLeft  = ttk.Button(mGUI.fr_buttons, text="<",    command=mGUI.panLeft,  width=4, style="BW.TButton")
    mGUI.bt_zoomIn  = ttk.Button(mGUI.fr_buttons,  text="zIn",  command=mGUI.zoomIn,   width=6, style="BW.TButton")
    mGUI.bt_zoomOut = ttk.Button(mGUI.fr_buttons,  text="zOut", command=mGUI.zoomOut,  width=6, style="BW.TButton")
    mGUI.bt_panRight = ttk.Button(mGUI.fr_buttons, text=">",    command=mGUI.panRight, width=4, style="BW.TButton")

    mGUI.separatorBtsA = ttk.Separator(mGUI.fr_buttons, orient=VERTICAL)

    mGUI.bt_play_forward = ttk.Button(mGUI.fr_buttons, text ="Play F", command = mGUI.playForwardFunctionality, style="BW.TButton")
    mGUI.bt_play_backward = ttk.Button(mGUI.fr_buttons, text = "Play B", command = mGUI.playBackwardFunctionality, style="BW.TButton")
    mGUI.bt_stop = ttk.Button(mGUI.fr_buttons, text = "Stop", command = mGUI.stopFunctionality, style="BW.TButton", width=7)
    mGUI.bt_pause = ttk.Button(mGUI.fr_buttons, text = "Pause", command = mGUI.pauseFunctionality, style="BW.TButton", width=7)

    mGUI.bt_frameleft = ttk.Button(mGUI.fr_buttons, text= u"\u21E6" + " Frame Left", command=mGUI.frameleftFunctionality, width=14, style="BW.TButton")
    mGUI.bt_frameright = ttk.Button(mGUI.fr_buttons, text="Frame Right"+u"\u21E8", command=mGUI.framerightFunctionality, width=14, style="BW.TButton")

#  PLACEMENT OF WIDGETs IN THE ROOT WINDOW ----
def placement(mGUI):

    mGUI.myframe.grid(row=0, column=0,  sticky=(N, S, E, W))

    # Help button
    mGUI.bt_help.grid(column=1, row=0, sticky=(N,W), pady=5, padx = 5)

    # Timeline buttons container
    mGUI.fr_buttons.grid(row=1, column=0, columnspan=2, sticky=(S,W),  padx=0, pady=3)

    # Timeline buttons
    mGUI.bt_panLeft.pack(side="left", padx=2)
    mGUI.bt_zoomIn.pack(side="left")
    mGUI.bt_zoomOut.pack(side="left")
    mGUI.bt_panRight.pack(side="left", padx=2)
    mGUI.separatorBtsA.pack(side="left", fill=Y, padx = 2)
    mGUI.bt_play_forward.pack(side="left")
    mGUI.bt_play_backward.pack(side="left")
    mGUI.bt_stop.pack(side="left")
    mGUI.bt_pause.pack(side="left")
    mGUI.bt_frameleft.pack(side="left")
    mGUI.bt_frameright.pack(side="left")

    # Video frame
    mGUI.frame_video.columnconfigure(0, weight=5)
    mGUI.frame_video.rowconfigure(0, weight=5)

    # Mirrorize checkbutton
    mGUI.chb_framemirrorize.grid(column=3, row=0, columnspan=1,  sticky=(N, S, E, W), pady=5, padx=5)

    # Labels text for each joint
    mGUI.lbl_joint = mGUI.nSignals*[0]

    # Canvases of signals
    for i in range( mGUI.nSignals ):

        if (i+1) % 3 == 1:
            # show the entire joint name and the x or y or z
            labeltext = mGUI.labels_axes[i]
        else:
            # only show x or y or z
            labeltext = mGUI.labels_axes[i][-1]

        # label widget
        mGUI.lbl_joint[i] = ttk.Label(mGUI.myframe, text = labeltext, style="BW.TLabel")
        mGUI.lbl_joint[i].grid(row=2+i, column=0, rowspan=1, sticky=(N,S,E))

        # signal canvas
        mGUI.canvas_SG[i].grid(row=2+i, column=1, columnspan=3, rowspan=1, sticky=(N,S,W,E))

    # time info
    mGUI.lbl_infoTime.pack(side="top")

    # Buttons
    mGUI.bt_save.grid(column=1, row=4+mGUI.nSignals, sticky=(W,S), pady=5, padx = 5)
    mGUI.bt_newsession.grid(column=2, row=4+mGUI.nSignals, sticky=(W,S), pady=5, padx = 5, ipadx=10)
    mGUI.bt_exit.grid(column=2, row=4+mGUI.nSignals, sticky=(E,S), pady=5, padx = 0)

    ttk.Sizegrip().grid(column=0, row=5+mGUI.nSignals, sticky=(E))

    # window resizing configuration instructions
    mGUI.root.columnconfigure(0, weight=1)
    mGUI.root.rowconfigure(0, weight=1)

    mGUI.myframe.columnconfigure(0, weight=1)
    mGUI.myframe.columnconfigure(1, weight=20)
    mGUI.myframe.columnconfigure(2, weight=20)

    for i in range(2 + mGUI.nSignals):
        mGUI.myframe.rowconfigure(i, weight=1)