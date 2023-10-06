import requests
import json

dataset_path = ""

r = requests.post("http://127.0.0.1:5000/train", headers={"Content-Type":"application/json"},
                  data = json.dumps({
                      "dataset_path": dataset_path 
                  }))

print(r.text)