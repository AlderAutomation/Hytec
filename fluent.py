import requests
import json
import logging 
import datetime

import reading 
import config 


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.log", format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)


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
        thelog.debug(f'API_RESPONSE Listing device from {self.url} with a response of {response}')
        json_response = response.json()

        return json_response


    def get_device(self, serial: str) -> json:
        """Get device readings based on serial number"""

        type_of_req = f"controller/current-readings/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        thelog.debug(f'DEV_LOOKUP Doing device lookup of {serial} with response of {response}')
        json_response = response.json()

        return json_response


    def set_reading_obj(self, data) -> list:
        """Setup readings dataclasses from Fluent device readings use with get_device function"""

        reading_obj_list = []

        if 'error' in data:
            print(data)
            thelog.error(f'DEV_UNASSIGNED The device returned error data from api call. Likely due to being unassigned')
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
                        ch_name = ch_name.encode('ascii', 'ignore').decode('utf-8')
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
                        read_obj.set_received_datetime_or_posted('received_datetime', received)

                        reading_obj_list.append(read_obj)
        
            return reading_obj_list
        
    
    def list_active_alarms(self, serial: str) -> None:
        type_of_req = f"controller/active-alarms/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()

        return json_response




def main():
    print('hello')


if __name__=="__main__":
    main()