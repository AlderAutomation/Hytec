import requests
import config

BASE_URL = "https://api.fluent.walchem.com/"
API_KEY = config.API_KEY
HEADERS = {
  f'Authorization': API_KEY,
  'Accept': '*/*'
}

class Fluent_Data:
    def __init__(self) -> None:
        self.device_serial = 1510050448


    def list_devices(self) -> None: 
        type_of_req = "controller/list/"
        self.url = BASE_URL + type_of_req


def main():
    FAPI = Fluent_Data()
    FAPI.list_devices()
    response = requests.request("GET", "https://api.fluent.walchem.com/controller/list/", headers=HEADERS)

    print(response)
    print(response.text)
    print(FAPI.url)




if __name__=="__main__":
    main()
    # type_of_req = "controller/current-readings/"
    # serial = "1510050448"
    # url = BASE_URL + type_of_req + serial





