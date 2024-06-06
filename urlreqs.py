import requests


def delete_vin (vin, server_url): # call api to delete the vin
    res = requests.request('DELETE', server_url + vin)
    return res

def get_vin_by_status (status, server_url): # get the status by calling the api
    if (status.lower() == "available"):
        par = {"stati":"Available"}
    elif (status.lower() == "sold"):
        par = {"stati":"Sold"}
    url_find_by_status = server_url + "/findByStatus" #url to get vins by status
    res = requests.get(url_find_by_status, params=par)   
    return res

def get_vin_status(vin, server_url):
    url_get_vin = server_url+'/'+vin
    res = requests.get(url_get_vin)
    return res   

def update_vin_status (item, server_url):
    res = requests.put(server_url, json=item)
    return res

def create_vin_status (item, server_url):
    res = requests.post(server_url, json=item)
    return res