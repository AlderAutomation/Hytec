import datetime
import logging

import config
from fluent import Fluent_Data
from sql import Hysql


LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename="log.log", format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)


def write_readings_to_sql(Hysql, readings_list: list) -> None:
    if readings_list != False:
        device = Hysql.device_lookup(readings_list[0].dev_serial)
        try:
            installation_id = device[0][0]

            for reading in readings_list:
                reading.set_install_id(installation_id)
                if reading.ch_num in ["R1", "R2", "R3", "R4", "R5", "R6"]:
                    print(f'Skipping {reading.ch_num}')
                else:
                    Hysql.installations_data_add_row(reading)
                    print(f'Inserted {reading.hardware_name} into DB')
        except Exception as e:
            thelog.error(f'LOG_ERROR This device {readings_list[0].dev_serial} failed with following error {e} \n {readings_list[0]}')


def log_serial_list_length(serials: list) -> None:
    thelog.info(f'DEV_SERIAL_COUNT There are {len(serials)} serials in this run')


def main():
    start = datetime.datetime.now()
    thelog.info(f'APP_TIMERS process starts at {start}')
    FAPI = Fluent_Data()
    hysql = Hysql()

    serial_list = FAPI.list_devices()
    log_serial_list_length(serial_list['controller-list'])

    for serial in serial_list['controller-list']:
        readings_list = FAPI.set_reading_obj(FAPI.get_device(serial))
        write_readings_to_sql(hysql, readings_list)

    end = datetime.datetime.now()
    time_took = end - start
    thelog.info(f'APP_TIMERS The process ended at: {end}. And took {time_took}.')
    print(f'APP_TIMERS process took {time_took}')


def testing_shit():
    FAPI = Fluent_Data()
    # hysql = Hysql()

    'For doing list of serials'
    # serial_list = FAPI.list_devices()
    # log_serial_list_length(serial_list['controller-list'])

    # for serial in serial_list['controller-list']:
    #     print(serial)

    'Reading single serial number'
    # readings_list = FAPI.set_reading_obj(FAPI.get_device("1803050206"))
    # write_readings_to_sql(hysql, readings_list)

    # for reading in readings_list:
    #     print(reading)

    'Examing X-Rate headers'
    serial_list = FAPI.list_devices()
    for serial in serial_list['controller-list']:
        print(serial)

    # headers = serial_list.headers

    # for header, value in headers:
    #     print(f'{header}:{value}')



if __name__=="__main__":
    # main()
    testing_shit()


# TODO add multithreading to make this faster? 
 