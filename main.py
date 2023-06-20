import requests
import config
import base64


BASE_URL = "https://api.fluent.walchem.com/"
api_key = config.API_KEY
API_KEY = base64.b64encode(api_key.encode("utf-8")).decode("utf-8")
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


def main():
    # FAPI = Fluent_Data()
    # FAPI.list_devices()
    try:
        response = requests.get(BASE_URL + "controller/list", headers=HEADERS)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        print(response.status_code)
        print(response.json())

    except requests.exceptions.RequestException as e:
        print("Error occurred during the request:", e)

    except ValueError as e:
        print("Error occurred while parsing the response:", e)

if __name__=="__main__":
    main()
