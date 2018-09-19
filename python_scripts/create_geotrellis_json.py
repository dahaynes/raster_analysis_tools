import json, os

theDirectory = "/home/david/shapefiles"
theJSONS = [r"%s/%s" % (root, f) for root, dirs, files in os.walk(theDirectory) for f in files if "geojson" in f]

#theFilePath = "/home/david/shapefiles/4326/states.geojson"
allSubdirectories = filter(os.path.isdir, [os.path.join(theDirectory,f) for f in os.listdir(theDirectory)])
crs = [s.split("/")[-1] for s in allSubdirectories]

vectorDatasets = [ (aJSON,coord) for coord in crs for aJSON in theJSONS if coord in aJSON]

for vector in vectorDatasets:
    #splitting the JSON filepath and coordinate systems

    theJSONPath, theCRS = vector
    print("Creating new geoJSON %s" % (theJSONPath))

    with open(theJSONPath, 'r') as theJSON:
        myGeoJSON = json.load(theJSON)
        #Setting the coordinate system for the geojson
        myGeoJSON['crs'] = theCRS
        for featureID in range(0,len(myGeoJSON['features'])):
            #Adding the ID field for geotrellis
            if 'id' not in myGeoJSON['features'][featureID].keys():

                myGeoJSON['features'][featureID]['id'] = int(myGeoJSON['features'][featureID]['properties']['ID'])

        jsonName = theJSONPath.split("/")[-1].split(".")[0]
        jsonDirectory = "/".join(theJSONPath.split("/")[:-1])
        outJSON = "%s/%s_2.geojson" % (jsonDirectory, jsonName)
        #print(outJSON)
        json.dump(myGeoJSON, open(outJSON, 'w'))