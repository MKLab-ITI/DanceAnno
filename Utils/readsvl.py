# readSVLfiles.py

from xml.dom import minidom
import numpy as np

def extractSvlAnnotRegionFile(filename):
    """
    extractSvlAnnotRegionFile(filename)

    Extracts the SVL files (sonic visualiser)
    in this function, we assume annotation files
    for regions (generated by Sonic Visualiser 1.7.2,
    Regions Layer)

    Returns the following objects:
        parameters: copy-paste of the "header" of the SVL file,
        frames    : a numpy array containing the time
                    stamps of each frame, at the beginning
                    of the frame,
        durations : a numpy array containing the duration
                    of each frame,
        labels    : a dictionary with keys equal to the frame
                    number, containing the labels,
        values    : a dictionary with keys equal to the frame
                    number, containing the values.

    Note that this code does not parse the end of the xml file.
    The 'display' field is therefore discarded here.

    Numpy and xml.dom should be imported in order to use this
    function.

    Jean-Louis Durrieu, 2010
    firstname DOT lastname AT epfl DOT ch
    """
    ## Load the XML structure:
    dom = minidom.parse(filename)

    ## Keep only the data-tagged field:
    ##    note that you could also keep any other
    ##    field here.
    dataXML = dom.getElementsByTagName('data')[0]

    ## XML structure for the parameters:
    parametersXML = dataXML.getElementsByTagName('model')[0]

    ## XML structure for the dataset field, containing the points:
    datasetXML = dataXML.getElementsByTagName('dataset')[0]

    ## XML structure with all the points from datasetXML:
    pointsXML = datasetXML.getElementsByTagName('point')

    ## converting to a somewhat easier to manipulate format:
    ## Dictionary for the parameters:
    parameters = {}
    for key in parametersXML.attributes.keys():
        parameters[key] = parametersXML.getAttribute(key)

    ## number of points (or regions):
    nbPoints = len(pointsXML)

    ## number of attributes per point, not used here,
    ## but could be useful to check what type of SVL file it is?
    # nbAttributes = len(pointsXML[0].attributes.keys())

    ## Initialize the numpy arrays (frame time stamps and durations):
    frames = nbPoints*[0] # np.zeros([nbPoints], dtype=np.float)
    durations = np.zeros([nbPoints], dtype=np.float)
    ## Initialize the dictionaries (values and labels)
    values = {}
    labels = {}

    ## Iteration over the points:
    for node in range(nbPoints):
        ## converting sample to seconds for the time stamps and the durations:

        frames[node] = np.int(pointsXML[node].getAttribute('frame')) / np.double(parameters['sampleRate'])
        #durations[node] = np.int(pointsXML[node].getAttribute('duration')) / np.double(parameters['sampleRate'])
        ## copy-paste for the values and the labels:
        #values[node] = pointsXML[node].getAttribute('value')
        labels[node] = pointsXML[node].getAttribute('label')


    ## return the result:
    return parameters, frames, labels


