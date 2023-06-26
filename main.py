import requests
import json
import datetime

import reading


BASE_URL = "https://api.fluent.walchem.com/"
HEADERS = {
  'accept': '*/*',
  'authorization': 'Basic bWhlbHRtYW5AYWxkZXJhdXRvbWF0aW9uLmNhOmE1ODhjMDAwLWZjNWYtNGNmNy1iNDYxLTM5OWQ3ZjAyMGQ3Mw=='
}


class Fluent_Data:
    def __init__(self) -> None:
        self.device_serial = 1510050448


    def list_devices(self) -> None: 
        """Use this to get a list of serial number from the Fluent account"""

        type_of_req = "controller/list/"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()
        pretty_response = json.dumps(json_response, indent=4)

        print(pretty_response)


    def get_device(self, serial: str) -> json:
        """Get device readings based on serial number"""

        type_of_req = f"controller/current-readings/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()

        return json_response


    def set_reading_obj(self, data) -> list:
        """Setup readings dataclasses from Fluent device readings use with get_device function"""

        reading_obj_list = []

        if 'error' in data:
            print(data)
            
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


    def json_test_file(self) -> json:
        """Testing stuff with json file due to being faster then API"""

        with open("./test_data/2012140870.json", "r") as json_file:
            file_data = json.load(json_file)
        
        return file_data



def main():
    FAPI = Fluent_Data()
    # FAPI.list_devices()

    # readings_list = FAPI.set_reading_obj(FAPI.json_test_file())
    readings_list = FAPI.set_reading_obj(FAPI.get_device("1705301238"))

    # error_dev = FAPI.get_device("1606071152")
    # print (error_dev['error'])

    if readings_list != False:
        for reading in readings_list:
            print (reading)


if __name__=="__main__":
    main()


""" Random serial number issues:

1609132084 - no sub channel 
1606071152 - no reading error - dealt with 
1703140568 - no sub channel on the R's
2012140870 - Good but not in my test sql 
1602254151 - no subchannel
1705301238 - Good and in test SQL
"""