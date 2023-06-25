import config 
import mysql.connector


class Hysql:
    def __init__(self) -> None:
        self.mydb = mysql.connector.connect(
            host=config.SQLIP,
            port=config.PORT,
            user=config.SQLUSER,
            password=config.SQLPWD
        )

        
    def device_lookup(self, serial:str) -> None: 
        pass 


    def installations_data_add_row(self, dataclass:object) -> None:
        pass


def main():
    hysql = Hysql()
    print(hysql.mydb)


if __name__=="__main__":
    main()
