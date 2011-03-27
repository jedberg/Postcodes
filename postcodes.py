import sqlalchemy as sa
from math import *

echo=False
engine = sa.create_engine('sqlite:///postcodes.db', echo=False)

def make_metadata():
    metadata = sa.MetaData(engine)
    metadata.bind.echo = echo
    metadata.bind.text_factory = str

    return metadata

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a)) 
    km = 6367 * c
    return km 

def query_post(postcode):
    fields = (
        'postcode',
        'st',
        'lat',
        'lon',
        )
    metadata = make_metadata()
    postcodes = sa.Table('postcodes', metadata, autoload=True)
    s = postcodes.select(postcodes.c.postcode == postcode)
    try:
        return dict(zip(fields,s.execute().fetchone()))
    except (TypeError, sa.exc.OperationalError):
        return False

def distance(postcode1, postcode2):
    c1 = query_post(postcode1)
    c2 = query_post(postcode2)
    if c1 and c2:
        return haversine(c1['lon'], c1['lat'],c2['lon'], c2['lat'])
    else:
        return -1
    
if __name__ == "__main__":
    import sys
    try:
        print distance(sys.argv[1], sys.argv[2])
    except IndexError:
        print "Usage: %s postcode1 postcode2" % sys.argv[0]
