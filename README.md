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


As a result
![3](https://github.com/arsha-cova/top_50_songs/assets/59336004/fa45312f-48ba-48b8-bf18-1a8057dc0794)




