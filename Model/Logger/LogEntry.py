import datetime


class LogEntry:

    def __init__(self, action_title: str, action_description: str):
        self.__entry_time = str(datetime.datetime.now())
        self.__action_title = action_title
        self.__action_description = action_description

    def __str__(self):
        return self.__entry_time+"\t\t"+self.__action_title+"\t\t\t"+self.__action_description

