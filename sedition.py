#!/bin/env/python

### PUT THAT IN SOME IMPORTS
from query import *
import astropy.units as u
from astropy.coordinates import Angle
import matplotlib.pyplot as plt
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['Helvetica']})
rc('text', usetex=True)


#### PUT IT IN A SRC CLASS?
test_src_name="Virgo A"
q=query_sed(test_src_name,radius=0.005)

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


####  PUT IT IN A PLOT CLASS ?
plt.loglog(src_freq,src_flux,'.')
plt.xlabel(freq_unit)
plt.ylabel(flux_unit)
plt.suptitle(r"SED of %s"%(test_src_name),fontsize=16)
plt.title(r"($\alpha$=%s,$\delta$=%s)"%(txtRA,txtDEC))
plt.show()
