import csv

from django.db.utils import IntegrityError


def print_error(error, row, print_error):
    if print_error:
        print('Error:', error.args, '\nRow ID:', row.get('id'))


def create_models(file_path, model, print_errors):
    with open(file_path, encoding='utf-8', mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        total_count = 0
        successfull = 0
        for row in csv_reader:
            total_count += 1
            try:
                model.objects.get_or_create(**row)
                successfull += 1
            except IntegrityError as error:
                print_error(error, row, print_errors)
            except ValueError as error:
                print_error(error, row, print_errors)
        errors = total_count - successfull
        print('Model: {}\nSuccessfull: {}; errors: {}'.format(
            model.__name__, successfull, errors
        ))
