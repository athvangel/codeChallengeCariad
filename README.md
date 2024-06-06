# CARIAD Coding Backend Challenge

## Table of Contents

- [Installation](#install)
- [Answers](#answers)

## Installation
In order to run the code is necessary to have *python*, *fastapi*, *json2html* and *requests* installed.

1. [Python](https://www.python.org/downloads/)
2. ``` $ pip install fastapi ```
3. ``` $ pip install json2html ```
4. ``` $ pip install requests ```

## Answers

### **TESTSUITE AND TESTCASES**
   The exercise solution lies on running in the console the following command
   ```console
   $ python testsuite.py
   ```
   Once the command is executed: 

1. Creates 100 VINs starting with suffix AKKODIS and length 17 chars and the status is available. 
   - The artifact can be found on: *Artifacts/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/01_Creating_VINs.json* 
   - The report on: *Reports/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/01_Creating_VINs.html*

2. An api request ( */vehicle/findByStatus* ) to Cariad web server is executed and crosschecked with the VIN list created by us. 
   - The artifact can be found on: *Artifacts/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/02_Validating_VINs.json* 
   - The report on: *Reports/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/02_Validating_VINs.html* 

3. For every second VIN the status changes from available to sold. 
   - The artifact can be found on: *Artifacts/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/03_Altering_Status.json* 
   - The report on: *Reports/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/03_Altering_Status.html*
   
4. All artifacts and reports from the first section, TESTSUIT AND TESTCASES, can be found in  
   - *Artifacts/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/*
   - *Reports/&lt;yymmdd&gt;_&lt;hhmmss&gt;_cariad/* 

### **VIRTUALIZATION**

1. To run local webserver execute the command
   ```console
   $ fastapi dev local_server.py
   ```

2. The testsuite against the local virtualization, in a new terminal execute the command
   ```console
   $ python testsuite.py local
   ```

3. The artifacts and reports of the local virtualization testsuite can be found 
   - *Artifacts/&lt;yymmdd&gt;_&lt;hhmmss&gt;_local/*
   - *Reports/&lt;yymmdd&gt;_&lt;hhmmss&gt;_local/* 

   Regarding the reports, the 01_Creating_VINs.html report retrieves a response 500 internal server error for 100 VIN list and the VINS are not created. 
   The second report 02_Validating_VINs.html the response is 200 since the server is able to retrieve, however each VIN from list of 100 created by us will not be present. The server reply, will not contain the VIN list created moments before, due to an internal server error on the api endpoint create vehicle. 
   The third and last report, 03_Altering_Status.html, changing the status of every second VIN to sold will not be possible 
   

4. The code would be monitored in two situations, if the error happens in runtime, an error handling is in place and would report a string with "500 internal server error". 
In case the server starts to run, unit testing was checked across all the api enpoints and the developer would know something was wrong with the server.   


### **PROTOCOLS** 

#### Assumptions & Prerequisites

- Brokers and/or servers for the different protocols are up and running. 
- Endpoints to communicate wich are known. 
- Implemented message schemas are documented.

#### Concept

All testcases in the testsuite will have a generic structure and follow the same Arrange-Act-Assert pattern.
1. *Arrange* - Objects for this test are prepared. This includes the request that will be sent later as well as the expected response.
2. *Act* - The request is sent as defined and the corresponding response is captured then.
3. *Assert* - Actual response and expected response are compared. If they match, this testcase will pass, otherwise it will fail.

Instead of building requests and parsing responses directly in these testcases, this functionality is encapsulated in a dedicated module. That module is only responsible for message processing and a testcase is only responsible for validation correct behavior. While doing so appropriate methods from that other module can be used. Due to the prescribed approach modules with a single responsibility are achieved. 

In order to enable different protocols, that messaging module and their methods will be abstracted from a specific protocol. More precisely, for each supported protocol an adapter will be provided. Such an adapter can convert from the common interface used in testcases to a specific protocol interface, and back. Any further actions to do these conversions are wrapped in the respective adapters and hided from testcases.

Hence a testsuite setup as follows is feasible.
- Any testcase of an HTTP call makes use of an HTTP-specific adapter. That adapter converts query parameters and a request schema into an HTTP message as well as HTTP messages and a response schema into returns.
- Any testcase of a MQTT call makes use of a MQTT-specific adapter. That adapter converts query parameters and a request schema into a MQTT message as well as MQTT messages and a response schema into returns.
- Any testcase of a Protobuf call makes use of a Protobuf-specific adapter. That adapter converts query parameters and a request schema into a Protobuf message as well as Protobuf messages and a response schema into returns.
- And so on...