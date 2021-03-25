import requests
import xml.etree.ElementTree as ET
import base64
import os
import math

new = []


username = os.getenv('JSS_USER_KEY')
password = os.getenv('JSS_PASS_KEY')
url = os.getenv('JSS_URL')
http_status = 0

def query_api(serial):

    results = {}
    storage_results = {}
    request = request_data(serial)
    http_status = request.status_code

    if http_status != 200:
        results['Not Found'] = 'Not Found'
        storage_results['Not Found'] = 'Not Found'
        return results, storage_results

    root = ET.fromstring(request.text)
    general = root.find('general')
    search_list = ['name', 'serial_number', 'ip_address', 'last_reported_ip',
                   'mac_address', 'alt_mac_address']

    for search_Item in search_list:
        get_Item(results, search_Item, general)

    # get_Nested_Items(results, 'mdm_capable_users', general)

    dep = general.find('management_status')
    if dep != None:
        get_Item(results, 'enrolled_via_dep', dep)
    else:
        results['enrolled via dep'] = 'false'

    results['Separator'] = ""

    hardware = root.find('hardware')
    search_list = ['make', 'model', 'model_identifier', 'os_version',
                   'processor_type', 'processor_speed_mhz',
                   'number_processors', 'number_cores', 'total_ram_mb',
                   'cache_size_kb', 'available_ram_slots', 'sip_status',
                   ]

    for search_Item in search_list:
        get_Item(results, search_Item, hardware)

    get_Nested_Items(results, 'filevault2_users', hardware)

    storage = hardware.find('storage')
    device = storage.find('device')
    results['model hard drive'] = device.find('model').text
    results['serial hard drive'] = device.find('serial_number').text
    results['drive capacity mb'] = device.find('drive_capacity_mb').text


    count = 1
    for item in storage.findall('device'):
        storage_results['model hard drive ' + str(count)] = item.find('model').text
        storage_results['serial hard drive ' + str(count)] = item.find('serial_number').text
        storage_results['drive capacity mb ' + str(count)] = item.find('drive_capacity_mb').text
        count += 1

    return results, storage_results


    """
    Function get_Item() No return value

    The "data" argument is a dictionary, "search" argument
    is a string argument for the Element.find() function,
    "root" argument is a root Element object for this search
    """
def get_Item(data, search, root):
    item = root.find(search)
    item.tag = item.tag.replace("_", " ")
    data[item.tag] = item.text


    """
    Function get_Nested_Items() No return value

    Same as get_Item() but can get nested lists of Element objects
    """
def get_Nested_Items(data, search, root):
    count = 1
    items = root.find(search)
    for item in items:
        item.tag = item.tag.replace("_", " ")
        data[item.tag + ' ' + str(count)] = item.text
        count += 1


    """
    Function request_data(serial)

    Query the jss api and get the XML file it returns.  The XML file has all
    the data.

    Returns the jss data as a request object
    """
def request_data(serial):
    if len(serial) < 10:
        request = requests.get(
        url + '/computers/name/' + serial,
        auth=(base64.b64decode(username.encode('ascii')).decode('ascii'),
        base64.b64decode(password.encode('ascii')).decode('ascii')))
    else:
        request = requests.get(
        url + '/computers/serialnumber/' + serial,
        auth=(base64.b64decode(username.encode('ascii')).decode('ascii'),
        base64.b64decode(password.encode('ascii')).decode('ascii')))

    return request


def convert_units(results, storage_results):
    speed_in_ghz = float(results['processor speed mhz']) / 1000
    results['processor speed mhz'] = str(truncate(speed_in_ghz, 1)) + ' ' + 'GHz'

    ram_in_gb = int(results['total ram mb']) / 1024
    results['total ram mb'] = str(int(ram_in_gb)) + ' ' + 'GB'
    results['total ram gb'] = results.pop('total ram mb')

    cache_in_kb = int(results['cache size kb']) / 1024
    results['cache size kb'] = str(int(cache_in_kb)) + ' ' + 'MB'
    results['cache size mb'] = results.pop('cache size kb')

    count = 1
    looper = len(storage_results)
    while looper / 3 > 0:
        drive_capacity = int(storage_results['drive capacity mb ' + str(count)]) / 1024
        storage_results['drive capacity mb ' + str(count)] = str(int(drive_capacity)) + ' ' + 'GB'
        count += 1
        looper -= 3

    return None


def format_results(results, storage_results):
    final_results = {}

    final_results['name'] = results['name']
    final_results['serial number'] = results['serial number']
    final_results['make'] = results['make']
    final_results['model'] = results['model']
    final_results['model identifier'] = results['model identifier']
    final_results['mac os version'] = results['os version']
    final_results['imaged via dep'] = results['enrolled via dep']
    final_results['system integrity protection'] = results['sip status']
    final_results['ip address'] = results['ip address']
    final_results['last reported ip'] = results['last reported ip']
    final_results['mac address'] = results['mac address']
    final_results['alternate mac address'] = results['alt mac address']
    final_results['processor type'] = results['processor type']
    final_results['processor speed'] = results['processor speed mhz']
    final_results['processor cache'] = results['cache size mb']
    final_results['number processors'] = results['number processors']
    final_results['number of cores'] = results['number cores']
    final_results['total ram'] = results['total ram gb']
    final_results['available ram slots'] = results['available ram slots']

    count = 1
    looper = len(storage_results)
    while looper / 3 > 0:
        final_results['model hard drive ' + str(count)] = storage_results['model hard drive ' + str(count)]
        final_results['serial hard drive ' + str(count)] = storage_results['serial hard drive ' + str(count)]
        final_results['hard drive capacity ' + str(count)] = storage_results['drive capacity mb ' + str(count)]
        count += 1
        looper -= 3

    return final_results


def truncate(number, digits):
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper



#(new, other) = query_api('mski2102')
#print(len(other))
#convert_units(new)
#print(format_results(new, other))

#print(new)
