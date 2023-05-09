# pfch-finalproject

Using the program:

- Enter an address that includes building number, street name, and borough. Keep in mind that many addresses are not going to be represented in the city directory dataset. Your best best is trying something in lower Manhattan or the Chelsea area.

- You might have to wait a minute or two for the program to work. It takes a while to iterate through each entry in both datasets. 


Project description:

I used this program to begin building a new tool for genealogy and building research using two open-access datasets available from NYPL's Space/Time Directory and NYC Open Data. Currently, it is still very hard to simply search an NYC address and find a list of people who used to live there. Though many of NYPL'S New York City Directories are digitized and machine-readable data is available from the Space/Time Directory, there isn't currently a way for the public to search an address accross all directories at once. I wanted to start creating a tool that would eventually allow for this type of searching, while also connecting the directories dataset to historical NYC vital records available from the Municipal Archives, through NYC Open Data. This would allow users to see not only a list of the people at a certain address from the directory, but potential matches of important life events (birth, marriage, death) from the historical vital records.

Output is displayed in a .txt file and shows each match, their name, occupation, year listed in the directory, and address information, as well as any vital records created in the years listed that match the first and last name of the entry.


The general process of my work was:

1. Getting to know the nyc-directories dataset, downloading it as CSV (the other file types were too large for my computer to process), and determinging that I wanted to match searched addresses to directory entires through coordinates. NYPL Labs staff had used their nyc-addresses tool to assign coordinates to the historical addresses in the directory entries based on their historical locations, meaning changed in house number/street name over time wouldn't affect the matches I found.

2. Figuring out how to convert a user-inputted address into coordinates. I ended up using the geopy module to connect to the Nominatim geocoder API.

3. Determing how to get user-generated coordinates to match the right ones in the directories dataset. I ended up rounding my coordinates to the fourth decimal point, which represesnts about 11.1m of distance, and letting matches occur if the rounded coordinates were within + or - 0.0001 of each other.

4. Testing to see if random addresses I entered would return matches. I realized that the directories don't cover most of Brooklyn, and anywhere below 14th street in Manhattan or in Chelsea is the most likely to return matches, but there were still gaps in the data. This is probably due to the way that people were distributed across the city in the mid-to-late 1800s, and the fact that most of NYPL's digitized directories only cover Manhattan.

5. Looping through the historical vital records dataset and finding matches by comparing first and last name and the year the vital record was created. I wanted to only find certificates from the year that that person was living (or working) at the address in the directory.

Future ways to increase accuracy:

Unfortunately, the historical vital records dataset currently does not contain information like home address or occupation that might help make my results a lot more accurate. However, in the future I'd like to increase the accuracy of the results by comparing the year the vital record was created, the type of record, and the year the person is listed in the city directory to weed out obvious false matches (i.e. if someone was born that year, they probably aren't listed in the city directory as being a blacksmith). This would also let me expand my search by looking at vital records that were created outside the exact years someone is listed in the directory, but could still correspond to the same individual.

I also would like to eventually create a web-based search tool with a clean, accessible user interface for people to use.

Data sources: 

NYPL Space/Time Directory city-directories dataset: http://spacetime.nypl.org/#data
NYC Open Data Historical Vital Records dataset: https://data.cityofnewyork.us/City-Government/New-York-City-Historical-Vital-Records-Digitized-C/xdc2-zgy3 

