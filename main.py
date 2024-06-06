import json
import random
import time

import requests
from datetime import datetime

url = "https://playgroundvwtestapp.azurewebsites.net/vehicle"
url_find_by_status = url + "/findByStatus"
url_delete = url + ""
# Define the character pool
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


params_available = {"stati":"Available"}
params_sold = {'stati':"Sold"}

# Clean up
response_available = requests.get(url_find_by_status, params=params_available)
response_available = json.loads(response_available.text)

response_sold = requests.get(url_find_by_status, params=params_sold)
response_sold = json.loads(response_sold.text)

print("Cleaning up VINs...")

for available in response_available:
    res = requests.request('DELETE', "https://playgroundvwtestapp.azurewebsites.net/vehicle/" + available["vin"])
for sold in response_sold:
    res = requests.request('DELETE', 'https://playgroundvwtestapp.azurewebsites.net/vehicle/' + sold["vin"])

'''
def generate_random_string(length):
    """Generates a random string of the specified length."""
    return ''.join(random.sample(chars, length))


print("Generating VINs...")
# Generate 100 random strings with "AKKODIS" prefix
data = []

print("-----Timestamp------||-RES-||--------VIN--------||--Status--")

for i in range(10):
    # Generate random suffix
    suffix = generate_random_string(17 - len("AKKODIS"))
    car = {"vin": f"AKKODIS{suffix}", "name": f"AKKODIS{suffix}", "status": f"Available"}
    data.append(car)
    res = requests.post(url, json=car)
    date_format = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    print(f"{date_format} || {res.status_code} || {car['vin']} || {car['status']}")


print("Updating every second VIN to 'Sold'...")
for i, obj in enumerate(data):
    if i % 2:
        res_get = requests.request('GET', "https://playgroundvwtestapp.azurewebsites.net/vehicle/" + obj["vin"])
        obj["status"] = "Sold"
        res_put = requests.put(url, json=obj)
        print("Changing status to sold: ")
        print(res_get.text)
        print(res_put.text)
        date_format = datetime.utcfromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
        print(f"{date_format} || {res.status_code} || {obj['vin']} || {obj['status']}")
'''