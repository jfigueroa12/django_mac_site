import requests
import base64
import os
import sys


URL = "https://jss.mskcc.org:8443"

jss_key = "ZmlndWVyb2o6SmYxMDM5Njc0NiU="

# serial = "C02C2B7LMD6M"

def dep_request(serial):

    final_results = {}

    #request a jss token in order to make calls to the api
    headers = { "Authorization" : "Basic " + jss_key }
    requestToken = requests.post(URL + "/uapi/auth/tokens", headers=headers)

    tokenDict = requestToken.json()
    token = tokenDict['token']

    #get the devices in the device enrollment program
    tokenHeader = { "Authorization" : "Bearer " + token }
    getDevices = requests.get(URL + "/uapi/v1/device-enrollment/1/devices", headers=tokenHeader)

    #results are returned in a json array
    dep_results = getDevices.json()

    #results is a list of dictionaries, each dictionary contains a device
    #serial number and its corresponding properties
    results = dep_results['results']

    #iterate over the array in order to get each devices info and status
    found = False
    sum = 0

    for device in results:
        #sum += sys.getsizeof(device)

        if device['serialNumber'] == serial:
            found = True

            final_results['serial'] = device['serialNumber']

            if device['profileStatus'] == 'PUSHED':
                final_results['profileStatus'] = 'COMPLETED'
            else:
                final_results['profileStatus'] = device['profileStatus']

            final_results['description'] = device['description']
            #final_results['prestageId'] = device['prestageId']

            break

    if (found):
        print("Serial Number was found in the DEP database")
    else:
        final_results['Not Found'] = 'Not Found'

    #invalidate the jss token for security
    invalidateHeader = { "Authorization" : "Bearer " + token }
    invalidateToken = requests.post(URL + "/uapi/auth/invalidateToken", headers=invalidateHeader)

    return final_results

#dep_request(serial)
