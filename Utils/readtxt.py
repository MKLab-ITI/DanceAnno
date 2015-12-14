# readSVLfiles.py

import numpy as np
import collections

def parse(filename):

    Fs = 30 # standard for Kinect

    audioSplitGTsecs = []
    labels = {}
    audioSplitGTsecsB = []
    labelsB = {}
    jA = -1
    jB = -1

    with open(filename) as f:
        for line in f:
            toks = line[:-2].split(" \'")
            toks[1] = toks[1][:-1]

            if toks[2] == 'anntoken_A':
                jA+=1
                audioSplitGTsecs.append(int(toks[0])/Fs)
                labels[jA] = toks[1]
            elif toks[2] == 'anntoken_B':
                jB+=1
                audioSplitGTsecsB.append(int(toks[0])/Fs)
                labelsB[jB] = toks[1]


    return audioSplitGTsecs, labels, audioSplitGTsecsB, labelsB


def parse_mbeats(filename):

    mbeats = collections.OrderedDict()

    with open(filename) as f:
        for line in f:
            toks = line[:-1].split(" \t")
            mbeats[float(toks[0])] = toks[1]

    return mbeats