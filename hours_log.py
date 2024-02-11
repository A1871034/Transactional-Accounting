from os.path import exists as file_exists
from datetime import datetime
import json

# HOURS LOG
class hours_log:
    def __init__(self, log_filepath = "./data/log.json") -> None:
        self.log_filepath = log_filepath
        self.entry_format = "%d/%m/%y %H:%M"

        self.__ensure_log_file()
        self.entries = self.__parse_log_file()

    # Binary search both ends to find relevant entries
    # TODO: Implement properly, unimportant for performance right now
    def get_entries_between_period(self, start_date, end_date):
        return self.entries

    def get_entries(self):
        return self.entries
    
    # Add entry to log
    def add_entry(self):
        pass    

    # If the file doesn't exist create an empty one
    def __ensure_log_file(self) -> None:
        if file_exists(self.log_filepath):
            return
        
        self.__make_file()

    # Create an empty log file
    def __make_file(self, contents="[]") -> None:
        with open(self.log_filepath, "w") as f:
            f.write(contents)

    def __parse_datetime(self, val:str) -> datetime:
        return datetime.strptime(val, self.entry_format)

    def __parse_log_file(self) -> list:
        with open(self.log_filepath, "r") as f:
            entries = json.loads(f.read())

        parsed_entries = []

        for i in range(len(entries)):
            start_datetime = self.__parse_datetime(entries[i]["start_datetime"])
            end_datetime = self.__parse_datetime(entries[i]["end_datetime"])
            breaks = []
            for break_start, break_end in entries[i]["breaks"]:
                breaks.append([self.__parse_datetime(break_start), 
                               self.__parse_datetime(break_end)])
            cur_entry = entry(start_datetime, end_datetime, breaks, entries[i]["job_id"])

            parsed_entries.append(cur_entry)        

        return parsed_entries

    def __save_log_to_file(self):
        pass

# ----------------------------

# ENTRIES - Data Struct

class entry:
    def __init__(self, start_datetime, end_datetime, breaks, job_id) -> None:
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.breaks = breaks # [[start_datetime, ends_datetime], ...]
        self.job_id = job_id

        
if __name__ == "__main__":
    log = hours_log()