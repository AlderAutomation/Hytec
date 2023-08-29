import subprocess
import requests
import json
import logging 
import datetime
from time import sleep


import reading 
import config 


LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename=f'./Logs/{str(datetime.datetime.now())}.log', format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)


BASE_URL = 'https://api.fluent.walchem.com/'
HEADERS = {
  'accept': '*/*',
  'authorization': config.FLUENT_API_KEY,
  'User-Agent':"HytecAPIAgent"
}


class Fluent_Data:
    def __init__(self) -> None:
        thelog.debug('Fluent_Data class init')
        self.sess = self.create_session()

    
    def create_session(self) -> object:
        s = requests.Session()
        s.headers.update(HEADERS)

        def api_calls(r, *args, **kwargs):
            calls_left = r.headers['X-Rate-Limit-Remaining']
            thelog.debug(f'API_X_RATE_LIMIT Calls left: {calls_left}')

            if int(calls_left) == 2: 
                thelog.debug('API_X_RATE_LIMIT X-Rate_Limit close, Sleeping App' )
                sleep(5)

        s.hooks['response'] = api_calls

        return s


    def request_retry_with_max_wait_time(self, url:str, max_retries:int = 1, max_wait_seconds:int = 6):
        for retry_count in range(max_retries):
            try: 
                response = self.sess.get(url, headers=HEADERS)
                response.raise_for_status()
                return response.json()
            except (requests.RequestException, ValueError) as e:
                thelog.error(f'REQUEST_ERROR: {e}')
                if retry_count == max_retries -1: 
                    break
                wait_time = min(2 ** retry_count, max_wait_seconds)
                sleep(wait_time)
        return None
    

    def list_devices(self) -> None: 
        '''Use this to get a list of serial number from the Fluent account'''

        type_of_req = 'controller/list/'
        self.url = BASE_URL + type_of_req
        json_response = self.request_retry_with_max_wait_time(self.url)
        thelog.debug(f'API_RESPONSE Listing device from {self.url} with a response of {json_response}')

        return json_response


    def get_device(self, serial: str) -> json:
        '''Get device readings based on serial number'''

        type_of_req = f'controller/current-readings/{serial}'
        self.url = BASE_URL + type_of_req
        json_response = self.request_retry_with_max_wait_time(self.url)
        thelog.debug(f'DEV_LOOKUP Doing device lookup of {serial} with response of {json_response}')

        return json_response


    def set_reading_obj(self, data) -> list:
        '''Setup readings dataclasses from Fluent device readings use with get_device function'''

        reading_obj_list = []

        if data == None:
            print("no data")

            return False

        elif 'error' in data:
            print(data)
            thelog.error(f'DEV_UNASSIGNED The device returned error data from api call. Likely due to being unassigned')
            thelog.error(data)
            
            return False
        else:
            readings = data['readings']
            for r in readings:
                serial = int(data['serial-number'])
                try:
                    if 'subchannel' in r:
                        for sub in r['subchannel']:
                            ch_name = r['channel-name']
                            # TODO handle and log ascii character better 
                            ch_name = ch_name.encode('ascii', 'ignore').decode('utf-8')
                            ch_num = r['channel-number']
                            ch_type = r['channel-type']
                            sub_type = sub['type']
                            sub_value = sub['value']
                            try:
                                sub_units = sub['units']
                            except Exception as e:
                                sub_units = ''

                            read_obj = reading.Readings(serial, ch_name, ch_num, ch_type, sub_type, sub_value, sub_units)
                            received = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                            read_obj.set_received_datetime_or_posted('received_datetime', received)

                            reading_obj_list.append(read_obj)
                    
                    else: 
                        ch_name = r['channel-name']
                        ch_name = ch_name.encode('ascii', 'ignore').decode('utf-8')
                        ch_num = r['channel-number']
                        ch_type = r['channel-type']
                        sub_type = r['channel-name']
                        sub_value = 'LOW'
                        sub_units = ''

                        read_obj = reading.Readings(serial, ch_name, ch_num, ch_type, sub_type, sub_value, sub_units)
                        received = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        read_obj.set_received_datetime_or_posted('received_datetime', received)

                        reading_obj_list.append(read_obj)

                except Exception as e:
                    thelog.error(f"ERROR occurred while trying to handle {serial}: \n {e}")
                    self.exception_notification(e)

            return reading_obj_list
        

    def exception_notification(self, exception) -> None: 
        '''On exit function to notify that the system is down'''
        script_path = './slack_notification.sh'
        arg_text = exception

        subprocess.call(f'/bin/bash {script_path} {arg_text}', shell=True)


    def get_active_alarms(self, serial: str) -> None:
        type_of_req = f'controller/active-alarms/{serial}'
        self.url = BASE_URL + type_of_req
        response = self.sess.get(self.url, headers=HEADERS)
        json_response = response.json()

        return json_response


    def alarm_lookup(self, alarms_list:list) -> list:
        '''lookup alarm code and return alarm string for SQL writes'''

        alarms_string_list = []

        if len(alarms_list) != 0:
            for reading in alarms_list['alarm-info']:
                if reading['alarm-type'] != 'fluent-alarm':
                    if reading['alarm-id'] == 48:
                        alr_text = 'No Flow'
                        alr_ch_name = reading['channel-name']
                        alr_ch_num = reading['channel-number']
                    else:
                        alr_text = reading['alarm-text']
                        alr_ch_name = reading['channel-name']
                        alr_ch_num = reading['channel-number']

                alarms_string_list.append(f'{alr_ch_name} ({alr_ch_num}) {alr_text}')
            return alarms_string_list


    def set_reading_alarm(self, serial) -> str:
        alarm_code = self.alarm_lookup(self.get_active_alarms(serial))

        return alarm_code



def main():
    FAPI = Fluent_Data()
    print(FAPI.get_active_alarms(1903291361))


if __name__=='__main__':
    main()