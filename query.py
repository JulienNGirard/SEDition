from io import BytesIO
from http.client import HTTPConnection

from astropy.table import Table
import matplotlib.pyplot as plt


def query_sed(pos, radius=2):
    """ Query VizieR Photometry 
      
    Parameters
    ----------
    pos: tuple or str
        position tuple or object name
    radius: float
        position matching in arseconds.
    
    Returns
    -------
    table: astropy.Table
        VO table returned by the Vizier service.
    """
    try:
        ra, dec = pos
        target = "{0:f},{1:f}".format(ra, dec)
    except:
        target = pos
    
    if isinstance(target,str):
        target=target.replace(" ", "%20")

    host = "vizier.u-strasbg.fr"
    port = 80
    path = "/viz-bin/sed?-c={target:s}&-c.rs={radius:f}".format(target=target, radius=radius)
    print("Query: GET ",path)
    connection = HTTPConnection(host, port)
    connection.request("GET", path)
    response = connection.getresponse()
   
    table = Table.read(BytesIO(response.read()), format="votable")
    return table



