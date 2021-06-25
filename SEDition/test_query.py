import pytest
from . import query

def test_query_sed():
   import astropy
   srcname="Virgo A"
   q=query.query_sed(srcname,radius=0.002)
   assert isinstance(q,astropy.table.table.Table)
