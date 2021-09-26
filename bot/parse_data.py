from datetime import date
from bot import error


def get_data(date_entry, id_dir=99, id_group=30687):
    if not error.date_valid(date_entry):
        return []
    print(id_group)
    year, month, day = map(int, date_entry.split('-'))
    p = date(year, month, day).weekday()
    url ='https://ruz.spbstu.ru/faculty/'+str(id_dir)+'/groups/'+str(id_group)+'/?date='+date_entry
    print(url)

    return url
