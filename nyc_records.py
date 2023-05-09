import csv
import geopy
from geopy.geocoders import Nominatim
import ast
import re


# ----- Finding lat. and long. for a specific address (will be user-generated) -----

 

# address = "241 W 29th St, Manhattan"
address = input('What is your address? Please include the borough! (ex: "241 W 29th St, Manhattan")\n')

locator = Nominatim(user_agent="myGeocoder")

print("Finding the exact location of the address...")

location = locator.geocode(address, timeout=None)

print()

coordinates = [round(location.longitude, 4), round(location.latitude, 4)]


print("Exact location...well, located! Your coordinates are {}.\n".format(coordinates))


# ----- Opening the directory data and converting to a DictReader object




# Creating lists to store info about matched addresses
my_city_directory = []
my_vital_records = []

print()
print("Searching the city directory data for entries that match your address...")
print()


# My laptop was taking way too long to load the NDJSON file, so I went with the CSV instead

with open("city-directories.csv","r") as dir_file:


	
	dir_reader = csv.DictReader(dir_file)


	# ----- POPULATING MY_CITY_DIRECTORY -----

	# Going through each dictionary in the DictReader object of the city directory entries
	# I only want to pull out the entries that have a matching(ish) latitude and longitude
	# I'll round the latitude and longitude to 4 decmimal places, which represents about 11.1 meters
	
	# Adding the keys I need to a new list of dictionaries

	my_keys = ["id", "name", "type", "validSince", "validUntil", "$.data.occupation", "$.data.locations", "$.data.geocoded", "geometry"]




	for entry in dir_reader:

		# Some entries from the OCR'd images are ads, titles, etc. and don't have any address info.
		# I want to filter those out so my code doesn't break

		if entry["geometry"] != "":

			# Converting the geometry value to a dictionary (it got flattened to a list in the CSV)
			
			geometry = ast.literal_eval(entry["geometry"])

			
			possible_longs = []
			possible_lats = []

			# "Point" entries have one address per name, while "MultiPoint" have more than one

			if geometry["type"] == "Point":
				
				# Adding the longitudes and latitudes to their own lists, as well as deviations in order to broaden the search radius
				
				possible_longs.extend([round(geometry["coordinates"][0], 4), round(geometry["coordinates"][0]+0.0001, 4), round(geometry["coordinates"][0]-0.0001, 4)])
				possible_lats.extend([round(geometry["coordinates"][1], 4), round(geometry["coordinates"][1]+0.0001, 4), round(geometry["coordinates"][1]-0.0001, 4)])

			elif geometry["type"] == "MultiPoint":
				
				# Adding the longitudes and latitudes to their own lists, but accounts for all items in the nested list
				possible_longs.extend([round(geometry["coordinates"][0][0], 4), round(geometry["coordinates"][0][0]+0.0001, 4), round(geometry["coordinates"][0][0]-0.0001, 4), round(geometry["coordinates"][1][0], 4), round(geometry["coordinates"][1][0]+0.0001, 4), round(geometry["coordinates"][1][0]-0.0001, 4)])
				possible_lats.extend([round(geometry["coordinates"][0][1], 4), round(geometry["coordinates"][0][1]+0.0001, 4), round(geometry["coordinates"][0][1]-0.0001, 4),round(geometry["coordinates"][1][1], 4), round(geometry["coordinates"][1][1]+0.0001, 4), round(geometry["coordinates"][1][1]-0.0001, 4)])

			# If the coordinates are a match for the address inputted by the user, create a dictionary including the keys I'm interested in
			# Then add the dictionary to my my_city_directory list

			if ((coordinates[0] in possible_longs) and (coordinates[1] in possible_lats)):
				temp_dict = {}
				for key in entry:
					
					# Splits name into a list of separate parts (last, first, middle)
					
					if key == "name":
						cleaned_name = entry["name"].strip(" .«")
						newval = cleaned_name.split(" ")	
						temp_dict[key] = newval
			


						
					
					elif key in my_keys:
						temp_dict[key] = entry[key]
				
				# Filterning out entries for businesses - I only want real people so I can compare to vital records

				if "Co" not in temp_dict["name"] and "&" not in temp_dict["name"] and "Brothers" not in temp_dict["name"]:
					my_city_directory.append(temp_dict)




for match in my_city_directory:

	# Getting rid of random non-alpha characters and empty strings in the name list
	
	new_name = [] 

	for name_piece in match["name"]:

		if name_piece != " " and name_piece != ".":
			name_piece = re.sub("«", "", name_piece)
			new_name.append(name_piece)

	match["name"] = new_name

	match["certinfo"] = []


	"""

	print()
	print("Name:", end=" ")
	for name in match["name"]:
		print(name + ", ", end=" ")
	print()
	print("Occupation: ",match["$.data.occupation"])
	print("Valid since: " + match["validSince"]) 
	print("Valid until: " + match["validUntil"])
	print(match["$.data.locations"])
	print(match["$.data.geocoded"])
	print(match["geometry"])
	
	"""

# ----- POPULATING MY_VITAL_RECORDS -----
# Not adding any entries where the first and last name are blank, as the name is all I have for linking




with open("vital-records.csv","r") as vital_file:

	vital_reader = csv.DictReader(vital_file)

	for cert in vital_reader:
		if (cert["First Name"] != "" and cert["Last Name"] != "") and int(cert["Certificate Year"])<1880:
			for match in my_city_directory:
				if (match["name"][0] == cert["Last Name"] and match["name"][1] == cert["First Name"]) and (int(cert["Certificate Year"]) >= int(match["validSince"]) and int(cert["Certificate Year"]) <= int(match["validUntil"])):
					match["certinfo"].append(cert)


print ("Done matching certificates!")

address_file = str(re.sub("[^0-9a-zA-Z_]", "", address))

with open("address_results"+address_file+".txt", "w") as outfile:
	outfile.write("Thank you for searching " + address + ". Here are your results!")
	outfile.write("\n")
	outfile.write("\n")

	counter = 1

	for match in my_city_directory:
		outfile.write("-------------------- Match #" + str(counter) + "-------------------------\n")
		counter += 1
		
		outfile.write("Name: ")
		
		for name in match["name"]:
			outfile.write(name + ", ")
		outfile.write("\n")
		outfile.write("Occupation: " + match["$.data.occupation"] + "\n")
		outfile.write("Valid since: " + match["validSince"] + "\n") 
		outfile.write("Valid until: " + match["validUntil"] + "\n")
		outfile.write("Historical address data: " + match["$.data.locations"] + "\n")
		outfile.write("Geocoded address data as of ~2018: " + match["$.data.geocoded"] + "\n")
		outfile.write("\n")
		outfile.write("Vital Record Matches: " + "\n")
		outfile.write("\n")
		
		for certmatch in match["certinfo"]:
			outfile.write("\n")
			outfile.write("Name: " + certmatch["Last Name"] + " " + certmatch["First Name"] + "\n")
			outfile.write("Certificate type: " + certmatch["Type"] + "\n")
			outfile.write("County: " + certmatch["County"] + "\n")
			outfile.write("Certificate number: " + certmatch["Certificate Number"] + "\n")
			outfile.write("Age at death (if applicable): " + certmatch["Age at Death"] + "\n")
			outfile.write("Certificate year: " + certmatch["Certificate Year"] + "\n")

		outfile.write("\n")
















