import config 
import mysql.connector
import datetime

import reading


class Hysql:
    def __init__(self) -> None:
        self.my_db = mysql.connector.connect(
            host=config.SQLIP,
            port=config.PORT,
            user=config.SQLUSER,
            password=config.SQLPWD
        )

        self.my_cursor = self.my_db.cursor()
        self.posted = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        
    def device_lookup(self, serial:str) -> None: 
        '''Function to lookup device data based on serial number'''

        query = f"SELECT * from myhytec_dotcomdb.oi4h8_installations where device_serial_num = '{serial}';"
        self.my_cursor.execute(query)

        return self.my_cursor.fetchall()


    def installations_data_add_row(self, dataclass: object) -> None:
        dataclass.set_posted(self.posted)

        table_name = "myhytec_dotcomdb.oi4h8_installation_data"
        cols = ['installations_installation_id', 'received_datetime', 'hardware_name', 'custom_name', 'units', 'data_value', 'posted']
        values = [dataclass.installation_id, dataclass.received_datetime, dataclass.hardware_name, dataclass.custom_name, dataclass.units, dataclass.data_value, dataclass.posted]
        
        columns_str = ', '.join(cols)
        placeholders = ', '.join(['%s'] * len(values)) 

        query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders});"

        self.my_cursor.execute(query, values)
        self.my_db.commit()
        print(self.my_cursor.rowcount, 'records inserted.')


def main():
    hysql = Hysql()
    read_obj = reading.Readings('1705301238', 'AquaSoft', 'S11', 'C_Cond', 'Value', '449', 'ppm')

    install_id = hysql.device_lookup(read_obj.dev_serial)
    read_obj.set_install_id(install_id[0][0])

    hysql.installations_data_add_row(read_obj)


if __name__=="__main__":
    main()

