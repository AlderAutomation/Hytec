import requests
import config

BASE_URL = "https://api.fluent.walchem.com/"
API_KEY = config.API_KEY
HEADERS = {
  'Authorization': 'a588c000-fc5f-4cf7-b461-399d7f020d73',
  'Accept': '*/*'
}

class fluent_data:
    def __init__(self) -> None:
        self.device_serial = 1510050448
        

def main():
    print(API_KEY)


if __name__=="__main__":
    # main()
    type_of_req = "controller/current-readings/"
    serial = "1510050448"
    url = BASE_URL + type_of_req + serial
    response = requests.request("GET", url, headers=HEADERS)

    print(response)
    print(response.text)



