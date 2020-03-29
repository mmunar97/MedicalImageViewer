import datetime
import threading
import io

from Model.Logger.LogEntry import LogEntry


class LogManager(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)

        self.__logs = []
        self.__file_name = self.get_log_file_name()
        self.create_new_log_file(self.__file_name)

        self.set_initial_log()

    def set_initial_log(self):
        log = LogEntry("PROGRAM DID START", "EXECUTION HAS STARTED")
        self.append_new_log(log)

    def append_new_log(self, log: LogEntry):
        file = open(self.__file_name, "a")
        self.__logs.append(log)
        file.write(str(log)+"\n")
        file.close()

    @staticmethod
    def create_new_log_file(file_name: str):
        file = open(file_name, "x")
        file.close()

    @staticmethod
    def get_log_file_name():
        name = str(datetime.datetime.now())
        name = name.replace(" ", "_")
        name = name.replace(":", "-")
        name = name.replace(".", "-")
        return "logs/"+name+".txt"
