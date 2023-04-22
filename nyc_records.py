import csv
import geopy
from geopy.geocoders import Nominatim


# ----- Finding lat. and long. for a specific address (will be user-generated) -----


address = "30 St James Pl, Brooklyn"

locator = Nominatim(user_agent="myGeocoder")

print("Finding the exact location of the address, this might take a minute or so...")

location = locator.geocode(address, timeout=None)

print("Exact location...well, located!")


#Creating a dictionary to store each lat. and long. with its corresponding info
place_matches = {}

# ----- Opening the directories and vital records data files and converting them to DictReader objects


with open("city-directories.csv","r") as dir_file, open("vital-records.csv","r") as vital_file:
	
	vital_reader = csv.DictReader(vital_file)
	
	dir_reader = csv.DictReader(dir_file)

	for entry in dir_reader:
		entry["name"] = entry["name"].split(" ")
		
