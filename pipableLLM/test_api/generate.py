import requests
import json

question = "List the official names of cities that have not held any competition." 
context= "CREATE TABLE farm_competition (Official_Name VARCHAR, City_ID VARCHAR, Host_city_ID VARCHAR); CREATE TABLE city (Official_Name VARCHAR, City_ID VARCHAR, Host_city_ID VARCHAR)" 

r = requests.post("http://127.0.0.1:5000/generate", headers={"Content-Type":"application/json"},
                 data = json.dumps({
                      "context": context,
                      "question": question
                 }))
print(r.text)