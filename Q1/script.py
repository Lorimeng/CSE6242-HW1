import http.client
import json
import time
import sys
import collections


api_key = sys.argv[1]
conn = http.client.HTTPSConnection("api.themoviedb.org")

# Q1.1 b
f = open("movie_ID_name.csv", "w")
i = 0
for page in range(1, 19):
        time.sleep(0.3)
        conn.request("GET", "https://api.themoviedb.org/3/discover/movie?api_key=" + api_key + "&sort_by=popularity.desc&page=" + str(page) + "&release_date.gte=2004-01-01&with_genres=18")
        page_status = conn.getresponse()
        page_data = page_status.read().decode('utf-8')
        page_json = json.loads(page_data) 
        results = page_json["results"]
        for x in results:
                i = i + 1
                if (i == 351): break
                f.write(str(x["id"]) + "," + x["title"] + "\n")         
f.close()

# Q1.1 c
file = open("movie_ID_name.csv", "r")
movie_list = []
for line in file:
        
        time.sleep(0.3)
        i = 0
        l = line.split(",")
        movie_id = l[0]
        
        conn.request("GET", "https://api.themoviedb.org/3/movie/" + movie_id +"/similar?api_key=" + api_key + "&page=1" )
        similar_status = conn.getresponse()
        similar_data = similar_status.read().decode('utf-8')
        similar_json = json.loads(similar_data)
        sim_movie_results = similar_json["results"]
        
        for x in sim_movie_results:
                i = i + 1
                movie_list.append(movie_id + "," + str(x["id"]))
                if (i == 5): break       
file.close()

# deduplicates
remove_list =[]
for movie in movie_list:
        pair = movie.split(",")
        if int(pair[0]) > int(pair[1]):
                newPair = str(pair[1]) + "," + str(pair[0])
                
                if newPair in movie_list: 
                        # delete pair
                        remove_list.append(movie)

for movie in remove_list:
        movie_list.remove(movie)



deduplicate_file = open("movie_ID_sim_movie_ID.csv", "w")
for ele in movie_list:
        deduplicate_file.write(ele + "\n")
deduplicate_file.close()

