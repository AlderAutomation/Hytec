import requests
import json


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


    def get_readings(self, data) -> list:
        readings = data['readings']
        for r in readings:
            if r['channel-number'] == "S11":
                print(r['channel-name'])


    def json_test_file(self) -> json:
        with open("./test_data/2012140870.json", "r") as json_file:
            file_data = json.load(json_file)
        
        return file_data



def main():
    FAPI = Fluent_Data()
    # FAPI.get_readings(FAPI.get_device('1703140568'))
    FAPI.get_readings(FAPI.json_test_file())


if __name__=="__main__":
    main()
