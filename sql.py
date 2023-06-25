import config 
import mysql.connector


class Hysql:
    def __init__(self) -> None:
        self.my_db = mysql.connector.connect(
            host=config.SQLIP,
            port=config.PORT,
            user=config.SQLUSER,
            password=config.SQLPWD
        )

        self.my_cursor = self.my_db.cursor()

        
    def device_lookup(self, serial:str) -> None: 
        '''Function to lookup device data based on serial number'''

        query = f"SELECT * from myhytec_dotcomdb.oi4h8_installations where device_serial_num = '{serial}';"
        self.my_cursor.execute(query)

        return self.my_cursor.fetchall()


    def installations_data_add_row(self, dataclass:object) -> None:
        pass


def main():
    hysql = Hysql()
    print(hysql.device_lookup(1609132084))


if __name__=="__main__":
    main()
