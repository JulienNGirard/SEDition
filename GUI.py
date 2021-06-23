
import sys, os, random
from query import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog,QVBoxLayout,QMainWindow, QFileDialog,QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import astropy.units as u
from astropy.coordinates import Angle

from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)
# main window
# which inherits QDialog


class Window(QDialog):
       
    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
   
        # a figure instance to plot on
        self.figure = plt.figure()
   
        # this is the Canvas Widget that 
        # displays the 'figure'it takes the
        # 'figure' instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)
        self.canvas.resize
        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
   
        # Just some button connected to 'plot' method
        self.buttonplot = QPushButton('Search and Plot SED of the source')

        self.buttonexport = QPushButton('Export as EPS file')

        self.buttonexit = QPushButton('Exit')

        self.textbox= QLineEdit(self)
        self.textbox.resize(280,40)
        # adding action to the button
        self.buttonplot.clicked.connect(self.plot)
   
        self.buttonexport.clicked.connect(self.file_save)

        self.buttonexit.clicked.connect(QCoreApplication.instance().quit)

        # creating a Vertical Box layout
        layout = QVBoxLayout()
           
        # adding tool bar to the layout
        layout.addWidget(self.toolbar)
           
        # adding canvas to the layout
        layout.addWidget(self.canvas)
        
        layout.addWidget(self.textbox)

        # adding push button to the layout
        layout.addWidget(self.buttonplot)

        layout.addWidget(self.buttonexport)       

        layout.addWidget(self.buttonexit)  
        # setting layout to the main window
        self.setLayout(layout)
   
    # action called by thte push button
    def plot(self):
        
        text_src_name=self.textbox.text()
        if text_src_name =='':
            raise ValueError('No source specified')

        q=query_sed(text_src_name,radius=0.005)

        src_name=q
        src_flux=q['sed_flux'] # in Jansky
        src_freq=q['sed_freq'] # in GHz

        src_RA=q['_RAJ2000'][0]
        src_DEC=q['_DEJ2000'][0]
        src_pos=Angle([str(src_RA)+'d', str(src_DEC)+'d'])
        txtRA=Angle(src_RA,u.degree).to_string(unit=u.hour)
        txtDEC=Angle(src_DEC,u.degree).to_string(unit=u.degree)

        flux_unit=src_flux.unit
        freq_unit=src_freq.unit

        # clearing old figure
        self.figure.clear()
   
        # create an axis
        self.ax = self.figure.add_subplot(111)

        self.ax.loglog(src_freq,src_flux,'.')
        plt.xlabel(freq_unit,fontsize=12)
        plt.ylabel(flux_unit,fontsize=12)
        plt.suptitle(r"SED of %s"%(text_src_name),fontsize=12)
        plt.title(r"($\alpha$=%s,$\delta$=%s)"%(txtRA,txtDEC),fontsize=12)
        plt.tight_layout(pad=0.3)
        # refresh canvas
        self.canvas.draw()
        del q

    def file_save(self):
        pathname = QFileDialog.getSaveFileName(self, 'Save File')
        print(pathname)
        if pathname != "":
            plt.savefig(pathname[0],format="eps")
        #file = open(name,'w')
        #text = self.textEdit.toPlainText()
        #file.write(text)
        #file.close()
   
# driver code
if __name__ == '__main__':
       
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()
       
    # showing the window
    main.show()
   
    # loop
    sys.exit(app.exec_())
