import json
import random
import urlreqs
import os
from datetime import datetime

# Define the character pool
chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"


def generate_random_string(length):
    """Generates a random string of the specified length."""
    return ''.join(random.sample(chars, length))


def generate_vins(count, folder_path):
    json_log     = create_jsonlog(folder_path)
    data=[]
    
    for i in range(count):
        # Generate random suffix
        suffix = generate_random_string(17 - len("AKKODIS"))
        car = {"vin": f"AKKODIS{suffix}", "name": f"AKKODIS{suffix}", "status": f"Available"}
        data.append(car)

    with open(json_log.name, "w") as outfile:
        json.dump(data, outfile)
        outfile.close()
    return json_log.name


def create_vins_on_server (number, server_url, folder_path):
    file_path=generate_vins(number, folder_path)
    with open(file_path, 'r') as openfile:
	    # Reading from json file
        vin_list = json.load(openfile)
        openfile.close()
        os.remove(openfile.name)
    
    result_log_path= create_jsonlog(folder_path, "01_Creating_VINs")
    all_results=[]
    for items in vin_list:
        timestamp   =   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        res         =   urlreqs.create_vin_status(items, server_url)
        result      =   dict(time=f"{timestamp}")
        
        result.update(json.loads(res.text))
        result.update(dict(response=f"{res.status_code}"))
        all_results.append(result)

	# Writing to json file
    json.dump(all_results, result_log_path)
    result_log_path.close()
    return result_log_path.name


def validate_vin(file, server_url, folder_path):
    res = urlreqs.get_vin_by_status("Available", server_url)
    # open the file to read the list of VINs
    with open(file, "r") as readfile:
        vin_validate_list = json.load(readfile)
        readfile.close()
    vins_from_request = []
    vins_not_found = len(vin_validate_list)
    vins_found = 0
    for vehicle in vin_validate_list:
        vehicle["present"] = "-"
        vehicle["response"] = res.status_code
    if res.json():
        for vehicle in res.json():
            vins_from_request.append(vehicle["vin"])
        for vehicle in vin_validate_list:
            if vehicle["vin"] in vins_from_request:
                vins_found += 1
                vins_not_found -= 1
                vehicle["present"] = "Yes"
            else:
                vehicle["present"] = "No"
    else:
        for vehicle in vin_validate_list:
            vehicle["present"] = "No"
    validation_file = create_jsonlog(folder_path, '02_Validating_VINs')
    json.dump(vin_validate_list, validation_file)
    return validation_file.name, vins_found, vins_not_found  # return file name, counter_found and counter_notfound


def alter_vin_status(vin, server_url, status="Sold"):
    #change the status of a vin to sold
    res         = urlreqs.get_vin_status(vin, server_url)
    json_data   = json.loads(res.text)
    result      = dict () # create empty
    if "detail" in json_data and json_data["detail"] == "Vehicle with this VIN not found":
        json_data["vin"] = vin
        result.update(dict(info=json.loads(json.dumps(json_data))))
    else:
        if res.status_code == 200 and not(json_data['status']== status): #true when positive response and status different than desired

            result.update (dict(before=json.loads(json.dumps(json_data))))

            del json_data['id']                 #delete the id
            json_data['status']     = status        #update the status
            res_sold                = urlreqs.update_vin_status (json_data, server_url) # update the vin

            if (res_sold.status_code==200):
                json_data_sold = json.loads(res_sold.text)
                result.update(dict(after=json.loads(json.dumps(json_data_sold))))

            else:
                result.update(dict(after=dict(message="Could not change the status. Response: "+f"{res.status_code}")) )

        elif(json_data['status']== status): # status is already set to desired value
            result.update (dict(before=json_data))
            result.update (dict(after=dict(message="No change is needed Status is already set to: "+f"{status}")))
        else:
            result.update(dict(before = dict(message="NotFound. Response: "+f"{res.status_code}")))
            result.update(dict(after  = dict(message="NOT APPLICABLE")))
    result = json.dumps(result)
    result = json.loads(result)
    return result 

 
def alter_vin(file, server_url, folder_path):
    with open(file, "r") as readfile:
        validated_list = json.load(readfile)
        readfile.close()
    toggle=0
    all_results=[]
    for items in validated_list:
        if (items['response']==200 and toggle%2==1): # if positively validated and toggle is one
            result = alter_vin_status(items['vin'], server_url)
            all_results.append(result)
        toggle+=1
        

    altered_list=create_jsonlog(folder_path, "03_Altering_Status")
    json.dump(all_results,altered_list)
    altered_list.close
    return altered_list.name
         
         
def create_jsonlog(folder_path, name="vins"):
    json_file = folder_path + name + ".json"
    json_obj = open(json_file,'a')
    return json_obj