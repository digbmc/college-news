"""
Processing Place Names
- reads a list of place names from csv
- uses geocoder to get geographic coordinates from place name
- creates geojson FeatureCollection for coordinates of all places found
- saves FeatureCollection to geojson file

"""
# Import Statements
import csv # use to read the input file (place names)
from geopy.geocoders import MapBox # use the MapBox API to get geographic data
from geopy.extra.rate_limiter import RateLimiter # use RateLimiter to add delay between requests
import os # use to make a folder for the output
from geojson import Point, Feature, FeatureCollection, dump # use to store the information retrieved with the geocoder

# read csv to get place names
input_file = "gpe-processed.csv" # filepath for input file
places = {} # create empty dictionary for place names
with open(input_file, newline="") as csvfile: # open the input file
    georeader = csv.reader(csvfile) # read the csv
    header = next(georeader)
    for row in georeader: # for every row in the csv:
        place_name = row[0]
        num_total = row[1]
        num_issues = row[2]
        variations = row[3]
        places[place_name] = [num_total, num_issues, variations]

# use geocoding to get the coordinates

geocoder = MapBox("pk.eyJ1IjoiYW5hc2gxOCIsImEiOiJja3FzajhremIxemYyMm9xcWkxd3QzbnVvIn0.dohQuDA2XclaVtcpD8m9SA") # create a MapBox object, using a specific account token
geocode = RateLimiter(geocoder.geocode, min_delay_seconds = 1, return_value_on_exception = None) # initialize the RateLimiter with a one second minimum delay
features = [] # create an empty list for features to output
bmc = (40.028071, -75.315265) # set a coordinate for bryn mawr
not_found = []
for name in places.keys(): # for every place name from the input list:
    location = geocode(name, proximity=bmc) # get the location data from the geocoder
    if location is not None: # if a location is found:
        lat = float(location.latitude) # save the latitude as "lat"
        long = float(location.longitude) # save the longitude as "long"
        point = Point((long, lat)) # create a geojson point using the lat/long data
        feature = Feature(geometry=point, properties={"name": name, "count": places[name][0], "issues": places[name][1], "variations": places[name][2]}) # create a geojson feature
        features.append(feature) # add the feature to the features list
    else:
        not_found.append(name)
# print the unmapped locations:
# print("These locations could not be mapped: " + ", ".join(not_found))
feature_collection = FeatureCollection(features) # make the features list into a FeatureCollection
subfolder = "geomapping" # name the directory that will contain the output csv
if os.path.exists(subfolder) == False: # if the folder doesn't already exist:
    os.mkdir(subfolder) # make the folder
output_file = subfolder + "/GPE_output.geojson" # make csv file path
with open(output_file, "w", encoding = "utf-8") as f: # create the output file
    f.write("var locations = ")
    dump(feature_collection, f) # add the feature collection to the output file