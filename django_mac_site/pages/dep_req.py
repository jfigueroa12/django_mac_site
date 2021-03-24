import requests
import base64
import os
import sys


URL = "https://jss.mskcc.org:8443"

jss_key = "cmVzX0ZTX2xvb2t1cDo4Y31MZ059cXM="

#serial = "C02Z1373LVDL"

def dep_request(serial):

    final_results = {}

    #request a jss token in order to make calls to the api
    headers = { "Authorization" : "Basic " + jss_key }
    requestToken = requests.post(URL + "/uapi/auth/tokens", headers=headers)

    tokenDict = requestToken.json()
    #print(tokenDict)
    token = tokenDict['token']

    #get the devices in the device enrollment program
    tokenHeader = { "Authorization" : "Bearer " + token }
    #getDevices = requests.get(URL + "/uapi/v1/device-enrollment/1/devices", headers=tokenHeader)
    getDevices = requests.get(URL + "/api/v2/computer-prestages/1/scope", headers=tokenHeader)

    #results are returned in a json array
    dep_results = getDevices.json()
    #print(dep_results)

    #results is a list of dictionaries, each dictionary contains a device
    #serial number and its corresponding properties
    results = dep_results['assignments']

    #iterate over the array in order to get each devices info and status
    found = False
    sum = 0

    for device in results:
        sum += sys.getsizeof(device)

        if device['serialNumber'] == serial:
            found = True

            final_results['serial'] = device['serialNumber']
            final_results['enrolled'] = True

            break

    if (found):
        print("Serial Number was found in the DEP database")
    else:
        final_results['Not Found'] = 'Not Found'
        final_results['enrolled'] = False

     #invalidate the jss token for security
    invalidateHeader = { "Authorization" : "Bearer " + token }
    invalidateToken = requests.post(URL + "/uapi/auth/invalidateToken", headers=invalidateHeader)

    print(sum)
    return final_results
#
#dep_request(serial)
