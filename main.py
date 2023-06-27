import requests
import json
import datetime
import logging

import reading
from sql import Hysql


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.log", level=logging.DEBUG, format = LOG_FORMAT)
thelog = logging.getLogger()



BASE_URL = "https://api.fluent.walchem.com/"
HEADERS = {
  'accept': '*/*',
  'authorization': 'Basic bWhlbHRtYW5AYWxkZXJhdXRvbWF0aW9uLmNhOmE1ODhjMDAwLWZjNWYtNGNmNy1iNDYxLTM5OWQ3ZjAyMGQ3Mw=='
}


class Fluent_Data:
    def __init__(self) -> None:
        thelog.debug('Fluent_Data class init')


    def list_devices(self) -> None: 
        """Use this to get a list of serial number from the Fluent account"""

        type_of_req = "controller/list/"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        thelog.debug(f'Listing device from {self.url} with a response of {response}')
        json_response = response.json()
        pretty_response = json.dumps(json_response, indent=4)

        print(pretty_response)


    def get_device(self, serial: str) -> json:
        """Get device readings based on serial number"""

        type_of_req = f"controller/current-readings/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        thelog.debug(f'Doing device lookup of {serial} with response of {response}')
        json_response = response.json()

        return json_response


    def set_reading_obj(self, data) -> list:
        """Setup readings dataclasses from Fluent device readings use with get_device function"""

        reading_obj_list = []

        if 'error' in data:
            print(data)
            thelog.error(f'The device returned error data from api call. Likely due to being unassigned')
            thelog.error(data)
            
            return False
        else:
            readings = data['readings']
            for r in readings:
                serial = int(data["serial-number"])
                if 'subchannel' in r:
                    # TODO need a countering else to handle readings with out subchannels 
                    for sub in r['subchannel']:
                        ch_name = r['channel-name']
                        ch_num = r['channel-number']
                        ch_type = r['channel-type']
                        sub_type = sub['type']
                        sub_value = sub['value']
                        try:
                            sub_units = sub['units']
                        except Exception as e:
                            sub_units = ""

                        read_obj = reading.Readings(serial, ch_name, ch_num, ch_type, sub_type, sub_value, sub_units)
                        received = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        read_obj.set_received_datetime(received)

                        reading_obj_list.append(read_obj)
        
            return reading_obj_list
        
    
    def list_active_alarms(self, serial: str) -> None:
        type_of_req = f"controller/active-alarms/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()

        return json_response



    def json_test_file(self) -> json:
        """Testing stuff with json file due to being faster then API"""

        with open("./test_data/2012140870.json", "r") as json_file:
            file_data = json.load(json_file)
        
        return file_data



def main():
    FAPI = Fluent_Data()
    hysql = Hysql()
    # FAPI.list_devices()

    # readings_list = FAPI.set_reading_obj(FAPI.json_test_file())
    readings_list = FAPI.set_reading_obj(FAPI.get_device("1705301238"))

    # error_dev = FAPI.get_device("1606071152")
    # print (error_dev['error'])

    if readings_list != False:
        device = hysql.device_lookup(readings_list[0].dev_serial)
        installation_id = device[0][0]

        for reading in readings_list:
            reading.set_install_id(installation_id)
            if reading.ch_num in ["R1", "R2", "R3", "R4", "R5", "R6"]:
                print(f'Skipping {reading.ch_num}')
            else:
                hysql.installations_data_add_row(reading)
                print(f'Inserted {reading.hardware_name} into DB')


def testing_shit():
    FAPI = Fluent_Data()
    print(FAPI.list_active_alarms('1608315810'))


if __name__=="__main__":
    main()
    # testing_shit()


""" Random serial number issues:

1609132084 - no sub channel 
1606071152 - no reading error - dealt with 
1703140568 - no sub channel on the R's
2012140870 - Good but not in my test sql 
1602254151 - no subchannel
1705301238 - Good and in test SQL
"""