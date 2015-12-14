import os
import sys
sys.path.append(os.path.join('.','iT_Utils' ))
import matrix as m

def plotSignalJointDim(canvas, signalToPlot, color, tagsuffix):
    """
    Plot a signal per dimensionality per joint

    :param canvas: The canvas to plot the signal line
    :param signalToPlot: The signal to plot as a list of floats
    :param color:  The color of the line of the signal
    :param tagsuffix: The tag suffix to put in the signal line tag = 'Signal'+tagsuffix
    :return:
    """

    # Width and height of canvas
    W = canvas.winfo_width()
    H = canvas.winfo_height()

    lenSignal = len(signalToPlot)

    # Reverse because Tkinter y left upp corner is 0
    signalToPlot = m.multFlVec(-1, signalToPlot)

    # Shift Y to 0 until H pixels
    MinY = min(signalToPlot)
    MaxY = max(signalToPlot)

    YNormConst = - MinY  #max(MaxY,abs(MinY)) + 5

    signalToPlot = m.addFlVec(YNormConst, signalToPlot)
    signalToPlot = m.multFlVec(H / max(signalToPlot), signalToPlot)

    #-------------Subsample to W pixels ---------------
    SigXYList = 2*lenSignal*[0]

    xScale = W/lenSignal/2.0
    for i in range(0, 2*lenSignal, 2):
        SigXYList[i] = xScale * i
        SigXYList[i+1] = signalToPlot[int(i / 2)]

    # Plot the signal
    canvas.create_line(SigXYList, fill=color, tag=('Signal'+tagsuffix, 'all_resize'))

    return MinY, MaxY

def plotXLabels(canvas, lenSignal, Fs, iSeqSignal, LVframes):
    """
    Plot x labels

    :param canvas: canvas to plot the labels
    :param lenSignal: the length of the signal
    :param Fs: The sampling rate of Kinect
    :param iSeqSignal: The current index of the signals (max: nSignals*3)
    :param LVframes: length of video frames (might be < Ls)
    :return:
    """

    # Number of labels to plot
    nLabels = 10

    # Font size
    xLabelsFontSize = 6

    # Width and height of canvas
    W = canvas.winfo_width()
    H = canvas.winfo_height()

    Dx = lenSignal
    Stepx = Dx/nLabels
    ResW = float(W)/Dx

    for i in range(1, nLabels):
        xAct = i*Stepx
        xPix = xAct*ResW

        # Plot line
        canvas.create_line(xPix, H-12, xPix, H-17, width=1, dash=(4, 4), fill="#555555", tag=(str(i),'xLabelsLines', 'all_resize'))

        # Plot text
        canvas.create_text(xPix, H-6, text= "%4.2f" % float(xAct/Fs), font=("Arial", xLabelsFontSize, "normal"), tag=(str(i),'xLabelsValue','all_resize') )

    # Plot start line
    canvas.create_line(0, H, 0, 0, width=1, fill="#00ffff", tag=('STARTLINE','all_resize'))

    # Plot end line
    canvas.create_line(W-1, H, W-1, 0, width=1, fill="#00ffff", tag=('ENDLINE','all_resize'))

    # Plot end line of Video
    canvas.create_line(W * LVframes / lenSignal, H, W * LVframes / lenSignal, 0, width=2, fill="#ff5500", tag=('VIDEOENDLINE', 'all_resize'))

    # Every three canvases put a different separator line
    if (iSeqSignal+1) % 3 == 0:
        canvas.create_line(0, H, W, H, width=5, fill="#000", tag=('SEPARATOR','all_resize'))
    else:
        canvas.create_line(0, H, W, H, width=5, fill="#aaa", tag=('SEPARATOR','all_resize'))


def plotYLabels(canvas, MinY, MaxY):
   """
   Plot y labels

   :param canvas: current canvas to plot
   :param MinY: Minimum for y values
   :param MaxY: Maximum for y values
   :return:
   """

   # font size
   yLabelsFontSize = 6

   # Width and height of canvas
   W = canvas.winfo_width()
   H = canvas.winfo_height()

   # Step amplitutde in canvas y
   StepY = (MaxY - MinY)/5.0

   # define output format (integer or decimal) depending on the scale
   if abs(MaxY) > 5 or abs(MinY) > 5:
       units = '%d'
   else:
       units = '%3.2f'

   for i in range(1,5):
       yAct = i*StepY + MinY
       yPix = i/5.0 * float(H)

       # Plot line
       canvas.create_line(30, yPix, W, yPix, width=1, dash=(4,4), fill="#cccccc", tag=(str(i), 'yLabelsLines', 'all_resize'))

       # Plot text
       canvas.create_text(12, yPix, text= units % -yAct, font=("Arial", yLabelsFontSize, "normal"), tag=(str(i),'yLabelsTexts','all_resize'))