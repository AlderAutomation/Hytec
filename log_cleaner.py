import os 
import datetime
import config

class Log_Cleaner ():
    def __init__(self) -> None:
        self.LOG_DIR = "./Logs/"
        self.log_files = self.populate_log_files()
        self.NOW = datetime.datetime.now()
        self.SEVEN_DAYS = self.NOW - datetime.timedelta(days=config.LOG_DAYS)


    def compare_remove_older_logs(self):
        for log_file in self.log_files:
            dt_obj = datetime.datetime.strptime(log_file[:-4], "%Y-%m-%d %H:%M:%S.%f")

            if dt_obj < self.SEVEN_DAYS:
                os.remove(f"{self.LOG_DIR}{log_file}")



    def populate_log_files(self) -> list:
        '''Init function to preload list of log files into class variable'''

        log_list = []
        for dirpath, dirnames, filenames in os.walk(self.LOG_DIR):
            for filename in filenames:
                if filename.endswith(".log"):
                    log_list.append(filename)
        
        return log_list


def main():
    LC = Log_Cleaner()
    LC.populate_log_files()
    LC.compare_remove_older_logs()

if __name__=="__main__":
    main()