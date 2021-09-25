import requests
from bs4 import BeautifulSoup
import datetime
from datetime import date
import error

# in: date(YYYY-MM-DD), dir id, group id
# out: list with shedule

def get_data(date_entry, id_dir=99, id_group=30687):
    if not error.date_valid(date_entry):
        return []
    print(id_group)
    year, month, day = map(int, date_entry.split('-'))
    p = date(year, month, day).weekday()

    # tttt=str(year)+'-'+str(month)+'-'+str(day-p)

    url ='https://ruz.spbstu.ru/faculty/'+str(id_dir)+'/groups/'+str(id_group)+'/?date='+date_entry
    print(url)

    return url


#print(get_data(input(' YYYY-MM-DD ')))
