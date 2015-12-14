# This is the script that you should execute to start DanceAnno
# Use Pycharm from Intellij for speeding up your programming

import DanceAnno_Loader
import DanceAnno_MainGUI

__author__ = 'DIMITRIOS'
__version__ = '0.3.0'

# This class makes an instance of the data Loader GUI and afterwards the Main annotating GUI
class Application:

    # on start run the loader
    def __init__(self, parent):

        self.parent = parent
        # The Data Loader class
        myLoader = DanceAnno_Loader.Loader()

        return

    # when loader exits then start the main GUI
    def StartAnnotating(myLoader): # self here is the myLoader class

        #print(myLoader.length_signal_samples)
        myAnno_MainGUI = DanceAnno_MainGUI.DanceAnno(myLoader)

        return


# # make an application instance
if __name__ == "__main__":
    app = Application(None)
