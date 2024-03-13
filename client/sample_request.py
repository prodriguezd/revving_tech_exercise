import requests
import json

# Define the URL
url = 'http://127.0.0.1:8000/api/customer/?customer=testCustomer'

data = {
  "file_path": "/Users/paula/Documents/revving/revving/data2.csv"
}

headers = {'Content-Type': 'application/json'}

json_data =json.dumps(data)

response = requests.post(url, data=json_data, headers=headers)

print(response)