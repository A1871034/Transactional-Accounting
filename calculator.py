from jobs import jobs
from hours_log import hours_log

from datetime import timedelta, datetime

class calculator:
    def __init__(self) -> None:
        self.hours_log = hours_log()
        self.jobs = jobs()

    # Calculate pay between a period from a job
    # Start date (inclusive) to end date (exclusive)
    # TODO: Use function calls instead of directly referencing class attributes
    def period_pay(self, start_date, end_date, job_id):
        # Initialise job and get only relevant entries
        job = self.jobs.jobs[job_id]
        entries = self.hours_log.get_entries_between_period(start_date, end_date)

        # Adjust for casual Loading
        if job.casual:
            rate = job.base_rate*(1+job.casual_loading_rate)
        else:
            rate = job.base_rate
        print()
        # Calculate pay at ORD Rate
        pay = 0
        for entry in entries:
            hours_worked = self.__hours_worked(entry)
            pay += rate*hours_worked
        print(f"rate {rate}")
        print(f"hrs {pay/rate}")
        print(pay)
        # Add extra pay from penalties
        for penalty in job.penalties:
            if penalty.eval_type == "additional":
                adjust = 1
            elif penalty.eval_type == "multiplicative":
                adjust = job.base_rate
            print(penalty.name)
            print(f"value {penalty.value}")
            for entry in entries:
                hrs = self.__hours_worked_under_penalty(entry, penalty)
                pay += adjust*penalty.value*hrs
                print(f"hr {hrs}: earned {round(adjust*penalty.value*hrs,2)} at {adjust*penalty.value}")
            
            print(rate)
            print(pay)
        return pay

    @staticmethod
    def __hours_worked(entry):
        hours_total = calculator.__hours_between(entry.start_datetime, entry.end_datetime)
        hours_break = 0
        for break_start, break_end in entry.breaks:
            cur_break_hrs = calculator.__hours_of_period_intersection(entry.start_datetime, 
                                                                      entry.end_datetime, 
                                                                      break_start, break_end)
            if cur_break_hrs == 0:
                raise Exception("Break lies outside of hours worked")
 
            hours_break += cur_break_hrs

        return hours_total - hours_break

    @staticmethod
    def time_to_datetime(year, month, day, time):
        return datetime(year, month, day, time.hour, time.minute, 0)

    @staticmethod
    def __hours_worked_under_penalty(entry, penalty):
        if entry.start_datetime.weekday() == entry.end_datetime.weekday() and entry.start_datetime.weekday() not in penalty.days:
            return 0
        
        if entry.start_datetime.weekday() in penalty.days:
            s1 = entry.start_datetime
            e1 = entry.end_datetime
        elif entry.end_datetime.weekday() in penalty.days:
            s1 = entry.end_datetime
            e1 = entry.end_datetime
        else:
            return 0
        
        penalty_start = calculator.time_to_datetime(s1.year, s1.month, s1.day, penalty.start_time)
        if penalty.end_time is None:
            penalty_end = s1.date()+timedelta(days=1)
            penalty_end = datetime(penalty_end.year, penalty_end.month, penalty_end.day, 0, 0, 0)
        else:
            penalty_end = calculator.time_to_datetime(s1.year, s1.month, s1.day, penalty.end_time)

        total_under_penalty = calculator.__hours_of_period_intersection(s1, e1, penalty_start, penalty_end)
        break_hours = 0
        for break_start, break_end in entry.breaks:
            break_hours += calculator.__hours_of_period_intersection(break_start, break_end,
                                                    penalty_start, penalty_end)
        return total_under_penalty - break_hours
        

    @staticmethod
    def __hours_between(datetime_1, datetime_2):
        return (abs(datetime_1-datetime_2).seconds)/3600

    @staticmethod
    def __hours_of_period_intersection(s1: datetime, e1: datetime,
                                       s2: datetime, e2: datetime) -> float:
        if s1 > s2:
            s_last = s1
            e_last = e1
            s_first = s2
            e_first = e2
        else:
            s_last = s2
            e_last = e2
            s_first = s1
            e_first = e1

        if e_first <= s_last:
            return 0
        
        overlap = e_first - s_last

        if e_last < e_first:
             overlap -= e_first - e_last

        return overlap.seconds/3600

    def shift_pay(self) -> float:
        pass
    
    # Calculates weekly from starting_day after first occurance of an
    # entry under the given job
    def weekly_pay(self, job_id):
        pass

    # Calculates pay from latest complete week
    def latest_complete_week_pay(self, job_id):
        pass

    # Returns total pay given by function for all jobs 
    def sum_pay(self, funct):
        pass
        

if __name__ == "__main__":
    calc = calculator()
    paid = calc.period_pay("13/12/23", "17/12/23", 0)
    print(paid)