from datetime import time, timedelta
from os.path import exists as file_exists

import json

class jobs:
    def __init__(self, job_filepath = "./data/jobs.json") -> None:
        self.job_filepath = job_filepath

        self.__ensure_job_file()
        self.jobs = self.__parse_job_file()

    def __ensure_job_file(self):
        if file_exists(self.job_filepath):
            return

        self.__make_job_file()

    def __make_job_file(self, content = "[]"):
        with open(self.job_filepath, "w") as f:
            pass

    def __parse_job_file(self):
        with open(self.job_filepath, "r") as f:
            jobs = json.loads(f.read())

        parsed_jobs = []
        for i in range(len(jobs)):
            cur_penalties = self.__parse_penalties(jobs[i]["penalties"])
            cur_job = job(
                name = jobs[i]["name"],
                id = jobs[i]["id"],
                casual = jobs[i]["casual"],
                pay_week_start_day = jobs[i]["pay_week_start_day"],
                weeks_per_payslip = jobs[i]["weeks_per_payslip"],
                min_hours_requiring_break = jobs[i]["min_hours_requiring_break"],
                min_break_time_mins = jobs[i]["min_break_time_mins"],
                base_rate = jobs[i]["base_rate"],
                age_modifiers = jobs[i]["age_modifiers"],
                penalties = cur_penalties
            )
            parsed_jobs.append(cur_job)

        return parsed_jobs
    
    @staticmethod
    def __parse_time(val:str) -> time:
        return time.fromisoformat(val)
        
    
    @staticmethod
    def __parse_penalties(penalties):
        cur_penalties = []
        for iter_penalty in penalties:
            cur_penalty = penalty(
                name = iter_penalty["name"],
                eval_type = iter_penalty["eval_type"],
                value = iter_penalty["value"],
                days = iter_penalty["days"],
                start_time = jobs.__parse_time(iter_penalty["start_time"]),
                end_time = None if iter_penalty["end_time"] is None else jobs.__parse_time(iter_penalty["end_time"])
            )
            cur_penalties.append(cur_penalty)

        return cur_penalties


class job:
    def __init__(self, name, id, casual, pay_week_start_day, weeks_per_payslip, min_hours_requiring_break,
                 min_break_time_mins, base_rate, age_modifiers, penalties) -> None:
        self.name = name
        self.id = id
        self.casual = casual #Bool
        self.casual_loading_rate = 0.25
        self.pay_week_start_day = pay_week_start_day
        self.weeks_per_payslip = weeks_per_payslip
        self.min_hours_requiring_break = min_hours_requiring_break
        self.min_break_time_mins = min_break_time_mins
        self.base_rate = base_rate
        self.age_modifiers = age_modifiers
        self.penalties = penalties       


class penalty:
    def __init__(self, name, eval_type, value, days, start_time, end_time) -> None:
        self.name = name
        self.eval_type = eval_type
        self.value = value
        self.days = days
        self.start_time = start_time
        self.end_time = end_time
        
if __name__ == "__main__":
    j = jobs()
    print("a")