# Import libraries
from datetime import datetime, timedelta
import time
import pycountry
import ujson
import psutil

# We use the psutil library to know the memory used by our script
p = psutil.Process()
# We use the time library in order to calculate the time of execution
start_time = time.time()

# Define all the necessary paths
path = "C:\\Users\\medam\\OneDrive\\Bureau\\Deezer_Top_50_Songs\\"
log_folder = path + "input\\log_files\\"
intermediary_files = path + "input\\intermediary_files\\"
output_path = path + "output\\"

# Get the current date
current_date = datetime.now()
# Create empty tuples to store the filenames
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

# Get the name of the last added log file
streams_file = log_filenames[-1]


# Define a function row_validated() that verifies if a row in our file is right to process it
def row_validated(row, countries_ISO_Code):
    if len(row) == 3:
        if row[0].isdigit() and row[1].isdigit() and row[2] in countries_ISO_Code:
            return True
    return False


# General function to process a log file by country or user
def process_logFile(log_folder, streams_file, process_type="country"):
    data = {}
    countries_ISO_Code = {country.alpha_2 for country in pycountry.countries}
    with open(log_folder + streams_file, 'r') as file:
        for line in file:
            try:
                row = line.strip().split("|")
                if row_validated(row, countries_ISO_Code):
                    sng_id, user_id, country = row
                    if process_type == "country":
                        key = country
                    elif process_type == "user":
                        key = user_id
                    else:
                        raise ValueError("Invalid process_type, must be 'country' or 'user'")

                    if key not in data:
                        data[key] = {}
                    if sng_id in data[key]:
                        data[key][sng_id] += 1
                    else:
                        data[key][sng_id] = 1
                else:
                    pass  # Store corrupted rows for future analysis
            except ValueError:
                continue
    return data


# Define a function to save the data as a JSON file
def save_data(intermediary_files, file_name, data):
    with open(intermediary_files + file_name, "w") as json_file:
        ujson.dump(data, json_file)


# Define a function to combine data for countries or users over the past 7 days
def combined_data(intermediary_files, json_filenames, process_type="country"):
    combined_data = {}
    for i in range(7):
        try:
            with open(intermediary_files + json_filenames[i], 'r') as f:
                json_data = ujson.load(f)
        except:
            data = process_logFile(log_folder, log_filenames[i], process_type)
            save_data(intermediary_files, json_filenames[i], data)
            with open(intermediary_files + json_filenames[i], 'r') as f:
                json_data = ujson.load(f)

        for key, songs in json_data.items():
            if key not in combined_data:
                combined_data[key] = {}

            for song_id, number in songs.items():
                # Add the number to the corresponding song_id in the combined_data dictionary
                combined_data[key][song_id] = combined_data[key].get(song_id, 0) + number

    top_songs = {}
    for key, sng_ids in combined_data.items():
        sorted_songs = sorted(sng_ids.items(), key=lambda x: x[1], reverse=True)
        top_songs[key] = sorted_songs[:50]
    return top_songs


# Process the last added log file by country and save the result as a JSON file
data_country = process_logFile(log_folder, streams_file, "country")
save_data(intermediary_files, streams_file[:-4] + '.json', data_country)
del data_country  # Free memory

# Process the last added log file by user and save the result as a JSON file
data_user = process_logFile(log_folder, streams_file, "user")
save_data(intermediary_files, streams_file[:-4] + '_user.json', data_user)
del data_user  # Free memory

# Calculate the top 50 songs per country for the past 7 days
top_songs_country = combined_data(intermediary_files, json_filenames, "country")

# Calculate the top 50 songs per user for the past 7 days
top_songs_user = combined_data(intermediary_files, json_filenames, "user")

# Get the current date to use it for naming the new output files
outputfile = current_date.strftime("%Y%m%d")

# Save the top 50 songs by country as a text file
with open(output_path + 'country_top50_' + outputfile + '.txt', 'w') as file:
    for country, songs in top_songs_country.items():
        values_str = ','.join([f"{key}:{value}" for key, value in songs])
        file.write(f"{country}|{values_str}\n")

# Save the top 50 songs by user as a text file
with open(output_path + 'user_top50_' + outputfile + '.txt', 'w') as file:
    for user_id, songs in top_songs_user.items():
        values_str = ','.join([f"{key}:{value}" for key, value in songs])
        file.write(f"{user_id}|{values_str}\n")

# Free memory
del top_songs_country
del top_songs_user

# Get the time of running the script
end_time = time.time()
execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")

# Calculate the memory used
memory_used = p.memory_info().rss / (1024 * 1024)
print(f"Memory used by the script: {memory_used:.2f} MB")
