import vingenerator as vg
import reporting as rp
import sys
import os
from datetime import datetime
import time

if len(sys.argv) == 2 and sys.argv[1] == "local":
    # VIRTUALIZATION - Ex 2. Run the testsuite against you local virtualization.
    server_url = "http://127.0.0.1:8000/vehicle"
    server_name = "local"
else:
    # TESTSUITE AND TESTCASES - Ex 1 Ex 2 Ex 3 Ex 4
    server_url = "https://playgroundvwtestapp.azurewebsites.net/vehicle"
    server_name = "cariad"

curr_folder = os.path.dirname(__file__)
if not os.path.isdir(curr_folder + "/Reports"):
    os.mkdir(curr_folder + "/Reports")

if not os.path.isdir(curr_folder + "/Artifacts"):
    os.mkdir(curr_folder + "/Artifacts")

time.sleep(1)
testsuite_start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
artifact_folder_path = curr_folder + f"/Artifacts/{testsuite_start_time}_{server_name}/"
report_folder_path = curr_folder + f"/Reports/{testsuite_start_time}_{server_name}/"
os.mkdir(artifact_folder_path)
os.mkdir(report_folder_path)


# step 1
# Create vins
print("")
print("")
print("")
print("")
print("-----------START-------------")
print("")
print("Step 1: Create 100 VINS")
print("-----------------------------")
created_vins_list   =   vg.create_vins_on_server(100, server_url, artifact_folder_path)
print("-> Created VIN list is generated")
rep_created_vin=rp.convert2html(created_vins_list, report_folder_path)
print("FILE: "+rep_created_vin)
print("-----------------------------")

#Step 2 Validate Data
print("")
print("")
print("Step 2: Validate 100 VINS")
print("-----------------------------")

validated_list, found, not_found=vg.validate_vin(created_vins_list, server_url, artifact_folder_path)
print("-> Validated VIN list is generated")
print(f"-> No of NOT FOUND:{not_found}")
print(f"-> No of FOUND:{found}")
rep_validated_vin=rp.convert2html(validated_list, report_folder_path)
print("FILE: "+rep_validated_vin)
print("-----------------------------")
#Step 3 Alter status
print("")
print("")
print("Step 3: Alter Status")
print("-----------------------------")
print("-> Altered VIN Status list is generated")

altered_vin_list = vg.alter_vin(validated_list, server_url, artifact_folder_path)
rep_altered_vin = rp.convert2html(altered_vin_list, report_folder_path)
print("FILE: "+rep_altered_vin)
print("-----------------------------")
print("")
print("-------------END-------------")
print("")
print("")
print("")
print("")