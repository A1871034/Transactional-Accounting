from datetime import datetime

def __hours_of_period_intersection(s1: datetime, e1: datetime,
                                       s2: datetime, e2: datetime):
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

def pd(val:str) -> datetime:
    return datetime.strptime(val, "%d/%m/%y %H:%M")

s1 = "15/12/23 19:00"
e1 = "16/12/23 01:00"
s2 = "15/12/23 23:00"
e2 = "15/12/23 23:30"

s1 = pd(s1)
e1 = pd(e1)
s2 = pd(s2)
e2 = pd(e2)

a = __hours_of_period_intersection(s1,s2,e2,e1)
print(a)
