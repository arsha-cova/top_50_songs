# import libraries
from datetime import datetime,timedelta
import time
import pycountry
import ujson
import psutil

# we use the psutil library to know the memory used by our script
p = psutil.Process ()
# we use the time library in order to calculate the time of execution
start_time = time.time()

# we define all the necessary paths
path="h:\\Desktop\\Deezer_Top_50_Songs\\"
log_folder=path+"input\\log_files\\"
intermediary_files=path+"input\\intermediary_files\\"
output_path=path+"output\\"

# Get the current date
current_date = datetime.now()
# Create an empty tuple to store the filenames
log_filenames = ()
json_filenames = ()
# Iterate through the past 7 days
for i in range(7, 0, -1):
    # Calculate the date of the current iteration
    past_date = current_date - timedelta(days=i)

    # Format the date as YYYYMMDD
    formatted_date = past_date.strftime("%Y%m%d")

    # Create the desired filename
    log_filename = f"listen-{formatted_date}.log"
    json_filename = f"listen-{formatted_date}.json"

    # Concatenate the filename to the tuple
    log_filenames += (log_filename,)
    json_filenames += (json_filename,)

# get the name of the last added log file
streams_file = log_filenames[-1]

# define a function row_validated() that verifies if a row in our file is right to process it
def row_validated(row,countries_ISO_Code):
    if len(row)==3:
        if row[0].isdigit() and row[1].isdigit() and row[2] in countries_ISO_Code:
            return(True)
    return(False)

# Define a function process_logFile_for_country that process a log file and return a dictionary contain countries as keys and
#   a  dictionary of id_song and their number occurrence as a value. example: {"NL":{"12345678":681,"789456128":562,...}...}
def process_logFile_for_country(log_folder,streams_file):
    data = {}
    countries_ISO_Code={country.alpha_2 for country in pycountry.countries}
    with open(log_folder + streams_file, 'r') as file:
        for line in file:
            try:
                row = line.strip().split("|")
                if row_validated(row,countries_ISO_Code):
                    sng_id, user_id, country = row
                    if country not in data:
                        data[country] = {}
                    if sng_id in data[country]:
                        data[country][sng_id] += 1
                    else:
                        data[country][sng_id] = 1
                else: pass # we can store the corrupted rows and try to find a solution for this problem
            except ValueError:
                #
                continue
    return(data)


# define a function save_data_countries that save a given data as a json file in intermediary_files
def save_data_countries(intermediary_files,file_name,data):
    with open(intermediary_files+file_name, "w") as json_file:
        ujson.dump(data, json_file)


# define a function combined_data_country that process the saved results of the past 7 days in intermediary_files
#   and return a dictionary of top 50 songs for each country in the past 7 days
def combined_data_country(intermediary_files,json_filenames):
    # groupe the result of the last 7 days to return top 50 songs per country
    combined_data = {}
    for i in range(7):
        try:
            with open(intermediary_files + json_filenames[i], 'r') as f:
                json_data = ujson.load(f)
        except:
            data = process_logFile_for_country(log_folder, log_filenames[i])
            save_data_countries(intermediary_files, json_filenames[i],data)
            with open(intermediary_files + json_filenames[i], 'r') as f:
                json_data = ujson.load(f)

        for country, songs in json_data.items():
            if country not in combined_data:
                combined_data[country] = {}

            for song_id, number in songs.items():
                # Add the number to the corresponding song_id in the combined_data dictionary
                combined_data[country][song_id] = combined_data[country].get(song_id, 0) + number

    top_songs = {}
    for country, sng_ids in combined_data.items():
        sorted_songs = sorted(sng_ids.items(), key=lambda x: x[1], reverse=True)
        top_songs[country] = sorted_songs[:50]
    return(top_songs)


# Process the last added log file and get the result as a dictionary
data=process_logFile_for_country(log_folder,streams_file)
# save the result as a json file
save_data_countries(intermediary_files,streams_file[:-4]+'.json',data)
# delete the dictionary to free memory
del data

# Calculate Top 50 Songs per Country and store the result in top_songs_country
top_songs_country=combined_data_country(intermediary_files,json_filenames)

# Get the current date to use it for naming the new
outputfile=current_date.strftime("%Y%m%d")

# Save the result as a text file : country_top50_YYYYMMDD.txt
with open(output_path+'country_top50_'+outputfile+'.txt', 'w') as file:
    # Iterate over the keys and values of the dictionary
    for country, songs in top_songs_country.items():
        # Convert the values to a string representation
        values_str = ','.join([f"{key}:{value}" for key, value in songs])
        # Write the data to the file
        file.write(f"{country}|{values_str}\n")

# delete the variable to free memory
del top_songs_country

# Get the time of runing the script
end_time = time.time()
execution_time = end_time - start_time
#print the execution time
print(f"Execution time: {execution_time} seconds")

# calculate the memory used
memory_used=p.memory_info().rss/(1024*1024)
# print the value
print(f"Memory used by the script: {memory_used:.2f} MB")
