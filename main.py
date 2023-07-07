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
                    thelog.debug(f'Skipping {reading.ch_num}')
                else:
                    Hysql.installations_data_add_row(reading)
                    thelog.debug(f'Inserted {reading.hardware_name} into DB')
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
    hysql = Hysql()

    'For doing list of serials'
    # serial_list = FAPI.list_devices()
    # log_serial_list_length(serial_list['controller-list'])

    # for serial in serial_list['controller-list']:
    #     print(serial)

    'Reading single serial number'
    readings_list = FAPI.set_reading_obj(FAPI.get_device("1910291418"))
    write_readings_to_sql(hysql, readings_list)
    # for reading in readings_list:
    #     print(reading)



    # for reading in readings_list:
    #     print(reading)



if __name__=="__main__":
    # main()
    testing_shit()


# TODO add multithreading to make this faster? 

# TODO ERROR 2023-07-06 21:21:04,563 - LOG_ERROR This device 1703140574 failed with following error list index out of range 
# TODO Readings(dev_serial=1703140574, custom_name='AquaSoft', ch_num='S11', ch_type='C_COND', subch_type='VALUE', data_value='42', units='ppm', hardware_name='Sensor (S11)', installation_id=None, received_datetime='2023-07-06 21:21:04', posted=None)

# 1910291418 - no sub channels 
# 1602122079 - working 