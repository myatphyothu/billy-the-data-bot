import os, sys, random, datetime
import argparse, json
from faker import Faker
from utils import generate_date, generate_number


def get_cli_args():
    parser = argparse.ArgumentParser(description='Generates random data')
    parser.add_argument('input_file', type=str, help='input data file')
    return parser.parse_args()


def check_missing_keys(*expected_keys, provided_keys):
    for key in expected_keys:
        if key not in provided_keys:
            return True, key
    return False, None


def validate_input_data(input):

    # check for missing keys
    R, missing_key = check_missing_keys('output file', 'delimiter', 'cols', 'sample size', provided_keys=data.keys())
    if R:
        print(f'Missing {missing_key} in file')
        sys.exit(1)

    filename = input['output file']
    delimiter = input['delimiter']

    try:
        rows = int(input['sample size'])
    except ValueError:
        print(f"unable to parse value to integer {input['sample size']}")
        sys.exit(1)

    column_data_list = input['cols']
    for column_data in column_data_list:

        # check for missing keys
        cR, c_missing_key = check_missing_keys('name', 'type', provided_keys=column_data.keys())
        if cR:
            print(f'Missing {c_missing_key} in cols section of the file')
            sys.exit(1)

    return filename, delimiter, rows, column_data_list


def generate_output(filename, delimiter, rows, column_data_list):
    # print(filename, delimiter, rows)

    ff = Faker()
    Faker.seed(0)

    # print header
    header = []
    for item in column_data_list:
        header.append(item['name'])

    data_list = []
    for i in range(rows):

        row_data = []
        for item in column_data_list:

            if 'consider only' in item:
                consider_only = item['consider only']
                data = random.choice(consider_only)
            else:
                consider = item['consider'] if 'consider' in item else []
                # generate name
                if item['type'] == 'f_name':
                    data = (ff.name() if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else ff.name()

                elif item['type'] == 'f_date':
                    data = (generate_date(item) if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else generate_date(item)

                elif item['type'] == 'f_address':
                    data = (ff.address() if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else ff.address()

                elif item['type'] == 'f_phonenumber':
                    data = (ff.phone_number() if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else ff.phone_number()

                elif item['type'] == 'f_job':
                    data = (ff.job() if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else ff.job()

                elif item['type'] == 'f_number':
                    data = (generate_number(item) if random.choice([0, 1]) == 0 else random.choice(consider)) if len(consider) > 0 else generate_number(item)


            if data:
                data = data.replace('\n', ' ').replace('\r', ' ').replace(',', ' ')
                row_data.append(data)


        data_list.append(row_data)

    lines = ''
    with open(filename, 'w') as f:
        # write header
        f.write(delimiter.join(header) + '\n')

        # write rows
        for row in data_list:
            f.write(delimiter.join(row) + '\n')

    print(f'{filename} was generated...')


if __name__ == '__main__':
    args = get_cli_args()

    try:
        with open(args.input_file) as f:
            data = json.load(f)
            generate_output(*validate_input_data(input=data))
    except FileNotFoundError:
        print(f'File {args.input_file} is missing...')

