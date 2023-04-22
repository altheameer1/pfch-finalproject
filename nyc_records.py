import csv
import geopy
from geopy.geocoders import Nominatim


# ----- Finding lat. and long. for a specific address (will be user-generated) -----

"""

address = "30 St James Pl, Brooklyn"

locator = Nominatim(user_agent="myGeocoder")

print("Finding the exact location of the address, this might take a minute or so...")

location = locator.geocode(address, timeout=None)

print("Exact location...well, located!")

# NOTE: Coordinates in the city directories data are stored as lon., lat. while Nominatim stores them the opposite order


#Creating a dictionary to store each lat. and long. with its corresponding info
place_matches = {}

# ----- Opening the directories and vital records data files and converting them to DictReader objects

"""

my_city_directory = []
my_vital_records = []

with open("city-directories.csv","r") as dir_file, open("vital-records.csv","r") as vital_file:
	

	vital_reader = csv.DictReader(vital_file)
	
	dir_reader = csv.DictReader(dir_file)


	# ----- POPULATING MY_CITY_DIRECTORY -----

	# Going through each dictionary in the DictReader object of the city directory entries
	# Adding the keys I need to a new list of dictionaries

	my_keys = ["id", "name", "type", "validSince", "validUntil", "$.data.occupation", "$.data.locations", "$.data.geocoded", "geometry"]

	for entry in dir_reader:
		temp_dict = {}
		for key in entry:
			if key in my_keys:

				# Splits name into a list of separate parts (last, first, middle)
				
				if key == "name":
					newval = entry["name"].split(" ")
					temp_dict[key] = newval
				else: 
					temp_dict[key] = entry[key]

		my_city_directory.append(temp_dict)

	# ----- POPULATING MY_VITAL_RECORDS -----
	# Not adding any entries where the first and last name are blank, as the name is all I have for linking
	
	for cert in vital_reader:
		if cert["First Name"] != "" or cert["Last Name"] != "":
			my_vital_records.append(cert)

# ----- Now I'm done dealing with the original source files -----

# ----- Create a dictionary of matches in the city directories based on the inputted address

test_coord = [40.68887475,-73.96522064999999]

# Re-ordering the coordinates so they match the ones in the city directories data

temp_coord1 = test_coord[0]
temp_coord2 = test_coord[1]

test_coord = [temp_coord2, temp_coord1]

print(my_city_directory[3]["geometry"]["type"])



"""

for entry2 in my_city_directory:
	if entry2["geometry"]["type"] == "Point":
		if entry2["geometry"]["coordinates"] == test_coord:
			print("found a match!")
			print(entry2)

loc_matches = {}

"""






