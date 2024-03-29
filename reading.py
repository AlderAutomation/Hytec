from dataclasses import dataclass 
import logging 
import datetime 

import config

LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename=f'./Logs/{str(datetime.datetime.now())}.log', format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)



@dataclass(slots=True)
class Readings:
    thelog.debug('The dataclass has been init')
    dev_serial: str
    custom_name: str
    ch_num: str
    ch_type: str
    subch_type: str
    data_value: str
    units: str
    alarm1:str = None
    alarm2:str = None
    hardware_name: str = None
    installation_id: str = None
    received_datetime: str = None
    posted: str = None


    def __post_init__(self) -> None: 
        '''create the hardware_name fields by mapping all the numbers to 
        their equivalent current value in the SQL'''
        
        if self.ch_num == 'S11':
            self.hardware_name = 'Sensor (S11)'
        elif self.ch_num == 'S12':
            self.hardware_name = 'Sensor Temperature (S12)'
        elif self.ch_num == 'S21':
            self.hardware_name = 'Sensor (S21)'
        elif self.ch_num == 'S22':
            self.hardware_name = 'Sensor Temperature (S22)'
        elif self.ch_num == 'D1':
            if self.subch_type == 'TOTAL':
                self.hardware_name = 'FlowMeter Total (D1)'
            else:
                self.hardware_name = 'FlowMeter Rate (D1)'
        elif self.ch_num == 'D2':
            if self.subch_type == 'Aqua Level':
                self.hardware_name = 'Generic (D2)'
            else:
                self.hardware_name = 'Generic (D3)'
        elif self.ch_num == 'D3':
            if self.subch_type == 'TOTAL':
                self.hardware_name = 'FlowMaster Total (D2)'
            elif self.subch_type == 'pH Level':
                self.hardware_name = 'Generic (D3)'
            else:
                self.hardware_name = 'FlowMaster Rate (D2)'
        elif self.ch_num == 'D4':
            self.hardware_name = 'Generic (D4)'
        elif self.ch_num == 'D6':
            self.hardware_name = 'Generic (D6)'
        
        thelog.debug(f'READING_FUNC Dataclass hardware name has been assigned {self.hardware_name} based on {self.ch_num}')

    
    def set_install_id(self, installation_id) -> None:
        '''Set the installation ID for the dataclass'''

        thelog.debug(f'READING_FUNC Setting the installation ID to {installation_id}')
        self.installation_id = installation_id


    def set_alarm(self, alarm:str) -> None:
        '''Set the installation ID for the dataclass'''

        if type(alarm) == list:
            if len(alarm) == 1:
                thelog.debug(f'READING_FUNC Setting the alarm to {alarm}')
                self.alarm1 = alarm[0]
            elif len(alarm) == 2:
                thelog.debug(f'READING_FUNC Setting the alarm to {alarm[0]} and {alarm[1]}')
                self.alarm1 = alarm[0]
                self.alarm2 = alarm[1]


    def set_received_datetime_or_posted(self, column: str, time: str) -> None:
        '''set the received_datetime or posted value for sql col'''

        if column == 'received_datetime':
            thelog.debug(f'READING_FUNC Setting the received_datetime to {time}')
            self.received_datetime = time
        elif column == 'posted':
            thelog.debug(f'READING_FUNC Setting the posted time to {time}')
            self.posted = time 
