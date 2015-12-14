import scipy.io                         # for loading matlab files
import os
import time
global SLS
if os.name == 'posix':
   SLS = '//'
elif os.name == 'nt':
   SLS = '\\'

import numpy

def readmatlab(fname):
    mat = scipy.io.loadmat(fname)

    data = mat['skdata']

    Ns = len(data)      # 25 samples / sec
    D  = len(data[0])   # 3 dimensions x,y,z
    Np = len(data[0][0]) # 15 joints
    Fs = 25

    #print (str(Ns) + " samples" + " | secs:" + str(Ns/Fs) + " " + str(Np) + ":Skeleton Points | " + str(D) + ":Dimensions" )
    if 0:
        print("0 HEAD, 1 NECK")
        print("2 LEFT SHOULDER, 3 LEFT ELBOW, 4 LEFT HAND")
        print("5 RIGHT SHOULDER, 6 RIGHT ELBOW, 7 RIGHT HAND")
        print("8 TORSO")
        print("9 LEFT HIP, 10 LEFT KNEE, 11 LEFT FOOT")
        print("12 RIGHT HIP, 13 RIGHT KNEE, 14 RIGHT FOOT")

    signalHE = [Ns*[0], Ns*[0], Ns*[0]]
    signalNE = [Ns*[0], Ns*[0], Ns*[0]]
    signalLS = [Ns*[0], Ns*[0], Ns*[0]]
    signalLE = [Ns*[0], Ns*[0], Ns*[0]]
    signalLD = [Ns*[0], Ns*[0], Ns*[0]]
    signalRS = [Ns*[0], Ns*[0], Ns*[0]]
    signalRE = [Ns*[0], Ns*[0], Ns*[0]]
    signalRD = [Ns*[0], Ns*[0], Ns*[0]]
    signalTO = [Ns*[0], Ns*[0], Ns*[0]]
    signalLF = [Ns*[0], Ns*[0], Ns*[0]]
    signalLH = [Ns*[0], Ns*[0], Ns*[0]]
    signalLK = [Ns*[0], Ns*[0], Ns*[0]]
    signalRF = [Ns*[0], Ns*[0], Ns*[0]]
    signalRH = [Ns*[0], Ns*[0], Ns*[0]]
    signalRK = [Ns*[0], Ns*[0], Ns*[0]]


    for i in range(Ns):
        for d in range(D):
            for p in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]:
                if p == 0:
                    signalHE[d][i] = data[i][d][p]
                elif p == 1:
                    signalNE[d][i] = data[i][d][p]
                elif p == 2:
                    signalLS[d][i] = data[i][d][p]
                elif p == 3:
                    signalLE[d][i] = data[i][d][p]
                elif p == 4:
                    signalLD[d][i] = data[i][d][p]
                elif p == 5:
                    signalRS[d][i] = data[i][d][p]
                elif p == 6:
                    signalRE[d][i] = data[i][d][p]
                elif p == 7:
                    signalRD[d][i] = data[i][d][p]
                elif p == 8:
                    signalTO[d][i] = data[i][d][p]
                elif p == 9:
                    signalLH[d][i] = data[i][d][p]
                elif p == 10:
                    signalLK[d][i] = data[i][d][p]
                elif p == 11:
                    signalLF[d][i] = data[i][d][p]
                elif p == 12:
                    signalRH[d][i] = data[i][d][p]
                elif p == 13:
                    signalRK[d][i] = data[i][d][p]
                elif p == 14:
                    signalRF[d][i] = data[i][d][p]



    return signalHE, signalNE, signalLS, signalLE, signalLD, signalRS, signalRE, signalRD, signalTO, signalLH, signalLK, signalLF, signalRH, signalRK, signalRF, Fs

def readmatlab_wrapper(fname):

    signalHE, signalNE, signalLS, signalLE, signalLD, signalRS, signalRE, signalRD, signalTO, signalLH, signalLK, \
        signalLF, signalRH, signalRK, signalRF, Fs = readmatlab(fname)

    wrapper = {'Head': signalHE, 'Neck': signalNE, 'Left shoulder': signalLS, 'Left elbow': signalLE,
               'Left hand': signalLD, 'Right shoulder': signalRS, 'Right elbow': signalRE, 'Right hand': signalRD,
               'Torso': signalTO, 'Left hip': signalLH, 'Left knee': signalLK, 'Left foot': signalLF,
               'Right hip': signalRH, 'Right knee': signalRK, 'Right foot': signalRF}

    return wrapper,Fs


def skelparser(fname):

    #print(os.getcwd())
    #fname = 'iT_Data/Calus/rec_sm.skel'
    Fs = 30

    with open(fname, 'r') as f:
        nTotalLines = sum(1 for _ in f)

    nframes = int(nTotalLines/74)
    frames_indices = nframes*[0]
    frames_ids = nframes*[0]
    frames_timestamp_kinect = nframes*[0]
    frames_timestamp_system = nframes*[0]

    sig = numpy.ndarray( shape=(24,3,nframes), dtype=float, order='C')

    iFrame = -1
    iline = 1
    with open(fname, 'r') as f:
        for line in f:

            residual = iline % 74

            if residual == 1:
               iFrame = iFrame + 1
               lsplit = line.split()
               frames_indices[iFrame]  = int(lsplit[0])
               frames_ids[iFrame] = int(lsplit[1])
               frames_timestamp_kinect[iFrame] = int(lsplit[2])
               frames_timestamp_system[iFrame] = int(lsplit[3])

            if residual >= 2 and residual <= 25:
               lsplit = line.split()
               sig[residual-2][0][iFrame] = float(lsplit[0])
               sig[residual-2][1][iFrame] = float(lsplit[1])
               sig[residual-2][2][iFrame] = float(lsplit[2])

            iline = iline + 1

    f.close()

    # print("LF x", max(sig[19][0]) ,  min(sig[19][0]) )
    # print("LF y", max(sig[19][1]) , min(sig[19][1]) )
    # print("LF z", max(sig[19][2]) , min(sig[19][2]) )

    wrapper = {'Head': sig[0], 'Neck': sig[1], 'Torso': sig[2], 'Waist': sig[3],
               'Left collar': sig[4], 'Left shoulder': sig[5], 'Left elbow': sig[6], 'Left wrist': sig[7],
               'Left hand': sig[8], 'Left fingertip': sig[9],
               'Right collar': sig[10], 'Right shoulder': sig[11], 'Right elbow': sig[12], 'Right wrist': sig[13], 'Right hand': sig[14],
               'Right fingertip': sig[15], 'Left hip': sig[16], 'Left knee': sig[17], 'Left ankle': sig[18], 'Left foot': sig[19],
               'Right hip': sig[20], 'Right knee': sig[21], 'Right ankle': sig[22], 'Right foot': sig[23]}

    return wrapper, Fs




