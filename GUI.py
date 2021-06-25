
import sys, os, random
from query import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import QDialog,QVBoxLayout,QMainWindow, QFileDialog,QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox

import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure



import numpy as np


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

        self.buttonfit = QPushButton('Fit linear trend')

        self.buttonexport = QPushButton('Export as EPS file')

        self.buttonexit = QPushButton('Exit')

        self.textbox= QLineEdit(self)
        self.textbox.resize(280,40)
        # adding action to the button
        self.buttonplot.clicked.connect(self.plot)
        self.buttonfit.clicked.connect(self.fit_linear_trend)

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

        layout.addWidget(self.buttonfit)       

        layout.addWidget(self.buttonexport)       

        layout.addWidget(self.buttonexit)  
        # setting layout to the main window
        self.setLayout(layout)
   
    # action called by thte push button
    def plot(self):
        
        text_src_name=self.textbox.text()
        if text_src_name =='':
            raise ValueError('No source specified')

        try:
            q=query_sed(text_src_name,radius=0.005)
        except ValueError:
            print('No table found, please check the source ID')
            
        src_name=q
        self.src_flux=q['sed_flux'] # in Jansky
        self.src_freq=q['sed_freq'] # in GHz

        src_RA=q['_RAJ2000'][0]
        src_DEC=q['_DEJ2000'][0]
        src_pos=Angle([str(src_RA)+'d', str(src_DEC)+'d'])
        txtRA=Angle(src_RA,u.degree).to_string(unit=u.hour)
        txtDEC=Angle(src_DEC,u.degree).to_string(unit=u.degree)

        flux_unit=self.src_flux.unit
        freq_unit=self.src_freq.unit

        # clearing old figure
        self.figure.clear()
   
        # create an axis
        self.ax = self.figure.add_subplot(111)

        self.ax.loglog(self.src_freq,self.src_flux,'.')
        plt.xlabel(freq_unit,fontsize=12)
        plt.ylabel(flux_unit,fontsize=12)
        plt.suptitle(r"SED of %s"%(text_src_name),fontsize=12)
        plt.title(r"($\alpha$=%s,$\delta$=%s)"%(txtRA,txtDEC),fontsize=12)
        plt.tight_layout(pad=0.3)
        # refresh canvas
        self.canvas.draw()
        del q

    def fit_linear_trend(self):
        logfreq=np.log10(self.src_freq)
        logflux=np.log10(self.src_flux)       
        coeffs = np.polyfit(logfreq,logflux,deg=1)
        poly = np.poly1d(coeffs)
        model=lambda x: 10**(poly(x))
        modeldata=model(logfreq)
        #print(modeldata)
        plt.loglog(self.src_freq,modeldata,'r:')
        plt.annotate(r"Model: $\log F$=%.3f*$\log\nu$+%.3f"%(coeffs[0],coeffs[1]),xy=(0.025,0.85),xycoords='axes fraction',fontsize=6,color="red")
        self.canvas.draw()

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
