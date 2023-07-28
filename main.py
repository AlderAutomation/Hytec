import datetime
import logging
import atexit
import sys, os, subprocess

import config
from fluent import Fluent_Data
from sql import Hysql


LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename=f'./Logs/{str(datetime.datetime.now())}.log', format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)


def write_readings_to_sql(Hysql, FAPI, readings_list: list) -> None:
    if readings_list != False:
        device = Hysql.device_lookup(readings_list[0].dev_serial)
        try:
            installation_id = device[0][0]

            for reading in readings_list:
                reading.set_install_id(installation_id)
                if reading.ch_num in ['R1', 'R2', 'R3', 'R4', 'R5']:
                    thelog.debug(f'Skipping {reading.ch_num}')
                elif reading.ch_num == 'R6':
                    reading.set_alarm(FAPI.alarm_lookup(FAPI.get_active_alarms(reading.dev_serial)))
                    if reading.alarm != None:
                        Hysql.alarm_data_add_row(reading)
                        Hysql.alarm_data_inInstallations_update(reading)
                        thelog.debug(f'Inserted {reading.alarm} into DB problem data')
                else:
                    Hysql.installations_data_add_row(reading)
                    Hysql.alarm_data_inInstallations_update(reading)
                    thelog.debug(f'Inserted {reading.hardware_name} into DB')
        except Exception as e:
            thelog.error(f'LOG_ERROR This device {readings_list[0].dev_serial} failed with following error {e} \n {readings_list[0]}')


def log_serial_list_length(serials: list) -> None:
    thelog.info(f'DEV_SERIAL_COUNT There are {len(serials)} serials in this run')


def exit_notification() -> None: 
    '''On exit function to notify that the system is down'''
    script_path = './slack_notification.sh'
    arg_text = 'HYTEC_API_HAS_STOPPED_RUNNING_oh_noes'

    # subprocess.call(f'/bin/bash {script_path} {arg_text} {config.SLACKURL}', shell=True)
    subprocess.call(f'/bin/bash {script_path} {arg_text} {config.SLACKURL}', shell=True)

def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def main():
    FAPI = Fluent_Data()
    hysql = Hysql()

    start = datetime.datetime.now()
    thelog.info(f'APP_TIMERS process starts at {start}')
    
    serial_list = FAPI.list_devices()
    log_serial_list_length(serial_list['controller-list'])

    for serial in serial_list['controller-list']:
        readings_list = FAPI.set_reading_obj(FAPI.get_device(serial))
        write_readings_to_sql(hysql, FAPI, readings_list)

    end = datetime.datetime.now()
    time_took = end - start
    thelog.info(f'APP_TIMERS The process ended at: {end}. And took {time_took}.')
    print(f'APP_TIMERS process took {time_took}')


def testing_shit():
    FAPI = Fluent_Data()
    # hysql = Hysql()

    'For doing list of serials'
    serial_list = FAPI.list_devices()
    log_serial_list_length(serial_list['controller-list'])

    for serial in serial_list['controller-list']:
        print(serial)

    'Reading single serial number'
    # readings_list = FAPI.set_reading_obj(FAPI.get_device('1608315810'))

    # for reading in readings_list:
    #     print(reading)

    # write_readings_to_sql(hysql, FAPI, readings_list)
    # exit_notification()



if __name__=='__main__':
    atexit.register(exit_notification)

    main()
    restart_program()


    # testing_shit()
