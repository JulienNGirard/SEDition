from query import *

class Target():
    def __init__(self, obj_id, r):
        viz = query_sed(obj_id,radius=r)
        self.obj_id = obj_id
        self.r = r
        self.src_flux=viz['sed_flux']
        self.src_freq=viz['sed_freq']
        self.ra=viz['_RAJ2000'][0]
        self.dec=viz['_DEJ2000'][0]