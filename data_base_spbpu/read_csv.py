import csv


def get_group_id(group_name, name_institute):
    file_name = 'data_base_spbpu/' + name_institute + '.csv'
    with open(file_name, newline='\n') as csv_file:
        reader = csv.DictReader(csv_file)
        data = {row["name"]: row["id"] for row in reader}
        if group_name in data.keys():
            return data[group_name]
        else:
            return 0
