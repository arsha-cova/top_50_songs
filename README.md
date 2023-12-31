# Top 50 songs by country and user 

In this project we have developed scripts in python that will send each user the top 50 songs for their country as well as their own personal top 50 songs of the last 7 days.

## Project description
We are receiving each day in a folder, a text file named listen-YYYYMMDD.log that contains the logs of all listening streams made on that date. These logs are formatted as follows: 
-	There is a row per stream (1 listening). 
-	Each row is in the following format: sng_id|user_id|country

    With:  
    -	sng_id: Unique song identifier, an integer.
    -	user_id: Unique user identifier, an integer. 
    -	country: 2 characters string upper case that matches the country ISO code (Ex: FR, GB, ...). 

To extract the top 50 songs for a given day d, we need to use the 7 log files for the previous days d-1, d-2, ...,d-7. In this case, each log file of a single day will be processed 7 times to calculate the top 50 songs for the following 7 days. 

In order to optimize the time and improve the performance of our solution, we propose that each day as soon as a new log file arrives, we process it and save the results in an intermediate file which we then use to find the top 50 songs for the following 7 days.


![1](https://github.com/arsha-cova/top_50_songs/assets/59336004/124ce12b-c7cb-43a8-99ba-6803f29d7a68)


As a result, combining the intermediate files gives us the final result text file: country_top50_YYYYMMDD.txt


![3](https://github.com/arsha-cova/top_50_songs/assets/59336004/fa45312f-48ba-48b8-bf18-1a8057dc0794)


- The process_data.py process the new arrived log file to calculate for each country all the streamed songs and their number of occurrences, then save the result as a json file. This result is used in addition to others intermediate files to generate the final result file: country_top50_YYYYMMDD.txt

- The process_user_data.py  process the new arrived log file to calculate for each user all the streamed songs and their number of occurrences, then save the result as a json file. This result is used in addition to others intermediate files to generate the final result file: user_top50_YYYYMMDD.txt

Based on this result, we can give a user the most popular 50 songs in his country in the last week  and also the top 50 songs he heard last week.

### Libraries
Before running the scripts, you need to be sure you have already installed the following python libraries:
- datetime 
- time
- pycountry
- ujson
- psutil

### Automation Process
To schedule the processes to run every day in a Linux environment, we need to run the two following commands: 

- echo "0 0 * * * path /Process_Automation.sh" > mycron
- crontab mycron

You need to replace "path/" with the actual path of the shell script.
We can modify  "0 0 * * *" to update the programed time to execute the bash file.







