import config 
import mysql.connector
import datetime
import logging

import reading
import config

LOG_FORMAT = '%(levelname)s %(asctime)s - %(message)s'
logging.basicConfig(filename=f'./Logs/{str(datetime.datetime.now())}.log', format = LOG_FORMAT)
thelog = logging.getLogger()
thelog.setLevel(config.LOGLEVEL)



class Hysql:
    def __init__(self) -> None:
        thelog.debug('Hysql has been init')
        self.my_db = mysql.connector.connect(
            host=config.SQLIP,
            port=config.PORT,
            user=config.SQLUSER, 
            password=config.SQLPWD
        )

        thelog.debug(self.my_db)
        self.my_cursor = self.my_db.cursor()
        self.posted = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        
    def device_lookup(self, serial:str) -> None: 
        '''Function to lookup device data based on serial number'''

        query = f'SELECT * from myhytec_dotcomdb.oi4h8_installations where device_serial_num = "{serial}";'
        self.my_cursor.execute(query)
        thelog.debug(f'SQL_FUNC Looking up device {serial}')

        return self.my_cursor.fetchall()


    def installations_data_add_row(self, dataclass: object) -> None:
        '''Adds new row the the oi4h8_installation_data table'''

        dataclass.set_received_datetime_or_posted('posted', self.posted)

        table_name = 'myhytec_dotcomdb.oi4h8_installation_data'
        cols = ['installations_installation_id', 'received_datetime', 'hardware_name', 'custom_name', 'units', 'data_value', 'posted']
        values = [dataclass.installation_id, dataclass.received_datetime, dataclass.hardware_name, dataclass.custom_name, dataclass.units, dataclass.data_value, dataclass.posted]
        
        columns_str = ', '.join(cols)
        placeholders = ', '.join(['%s'] * len(values)) 

        query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});'
        thelog.debug(f'SQL_FUNC Inserting data into DB using: {query}')
        self.my_cursor.execute(query, values)
        self.my_db.commit()
        thelog.debug(f'SQL_WRITE {self.my_cursor.rowcount} records inserted.')


    def alarm_data_add_row(self, alarm_num: int, dataclass: object) -> None:
        '''Adds row to oi4h8_installation_problem_data'''

        dataclass.set_received_datetime_or_posted('posted', self.posted)

        table_name = 'myhytec_dotcomdb.oi4h8_installation_problem_data'
        cols = ['installations_installation_id', 'received_datetime', 'alarm_code']
        if alarm_num == 1:
            values = [dataclass.installation_id, dataclass.received_datetime, dataclass.alarm1]
        else:
            values = [dataclass.installation_id, dataclass.received_datetime, dataclass.alarm2]

        columns_str = ', '.join(cols)
        placeholders = ', '.join(['%s'] * len(values))

        query = f'INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});'
        thelog.debug(f'SQL_FUNC Inserting data into DB using: {query}')
        self.my_cursor.execute(query, values)
        self.my_db.commit()
        thelog.debug(f'SQL_WRITE {self.my_cursor.rowcount} records inserted.')
        

    def alarm_data_inInstallations_update(self, dataclass: object) -> None:
        '''Updates the alarm code on the oi4h8_installations table'''

        dataclass.set_received_datetime_or_posted('posted', self.posted)

        table_name = 'myhytec_dotcomdb.oi4h8_installations'

        query = f"UPDATE {table_name} SET alarm_code = '{dataclass.alarm1}' WHERE installation_id = {dataclass.installation_id};"
        thelog.debug(f'SQL_FUNC Inserting data into DB using: {query}')
        self.my_cursor.execute(query)
        self.my_db.commit()
        thelog.debug(f'SQL_WRITE {self.my_cursor.rowcount} records inserted.')


def main():
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    hysql = Hysql()
    read_obj = reading.Readings('1705301238', 'AquaSoft', 'S11', 'C_Cond', 'Value', '449', 'ppm')

    install_id = hysql.device_lookup(read_obj.dev_serial)
    read_obj.set_install_id(install_id[0][0])
    read_obj.set_received_datetime_or_posted('received_datetime', now)
    
    hysql.installations_data_add_row(read_obj)


if __name__=='__main__':
    main()

