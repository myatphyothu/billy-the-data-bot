import sys, datetime
from faker import Faker

ff = Faker()
Faker.seed(0)

def str_to_date(str_date):
    xx_list = str_date.split('-')
    d_year, d_month, d_day = int(xx_list[0]), int(xx_list[1]), int(xx_list[2])
    return datetime.date(d_year, d_month, d_day)


def generate_date(item):
    if 'from' in item and 'to' in item:
        start_date_str, end_date_str = item['from'], item['to']

        # ToDo: validate start_date, end_date
        # validate(start_date_str, end_date_str)

        start_date, end_date = str_to_date(start_date_str), str_to_date(end_date_str)
        data = f'{ff.date_between_dates(start_date, end_date)}'
    else:
        data = f'{ff.date()}'

    return data


def generate_number(item):
    if 'from' in item and 'to' in item:
        try:
            start_num, end_num = int(item['from']), int(item['to'])
            return f'{ff.pyint(min_value=start_num, max_value=end_num, step=1)}'
        except ValueError:
            print(f'Unable to parse integer for {item["name"]} ==> "from" or "to" values')
            sys.exit(1)
    else:
        return f'{ff.pyint()}'


