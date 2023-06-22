import requests
import json

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
        type_of_req = "controller/list/"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()
        pretty_response = json.dumps(json_response, indent=4)

        print(pretty_response)


    def get_device(self, serial: str) -> json:
        type_of_req = f"controller/current-readings/{serial}"
        self.url = BASE_URL + type_of_req
        response = requests.get(self.url, headers=HEADERS)
        json_response = response.json()

        return json_response


    def set_reading_obj(self, data) -> list:
        reading_obj_list = []

        readings = data['readings']
        for r in readings:
            serial = int(data["serial-number"])
            for sub in r['subchannel']:
                ch_name = r['channel-name']
                ch_num = r['channel-number']
                ch_type = r['channel-type']
                sub_type = f"SUB TYPE : {sub['type']}"
                sub_value = f"SUB TYPE : {sub['value']}"
                try:
                    sub_units = f"SUB TYPE : {sub['units']}"
                except Exception as e:
                    sub_units = ""

                read_obj = reading.Readings(serial, ch_name, ch_num, ch_type, sub_type, sub_value, sub_units)
                reading_obj_list.append(read_obj)
        
        return reading_obj_list


    def json_test_file(self) -> json:
        with open("./test_data/2012140870.json", "r") as json_file:
            file_data = json.load(json_file)
        
        return file_data



def main():
    FAPI = Fluent_Data()
    # FAPI.get_readings(FAPI.get_device('1703140568'))
    readings_list = FAPI.set_reading_obj(FAPI.json_test_file())
    
    for reading in readings_list:
        print(reading)


if __name__=="__main__":
    main()
