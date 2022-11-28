import subprocess
import shlex
import datetime

import threading
import time
import sys

'''
    type your command here:
    example: ('command_name': 'command')
'''
COMMANDS = [
    ('BUILD', 'docker-compose build'),
    ('RUN', 'docker-compose up'),
    ('DOWN', 'docker-compose down'),
    ('TEST', 'docker-compose run --rm src sh -c "python manage.py test"'),
    ('COVERAGE', 'docker-compose run --rm src sh -c "coverage run manage.py test && coverage report"'),
    ('FLAKE8', 'docker-compose run --rm src sh -c "flake8 --exclude=core/migrations/,server/settings.py,*/__init__.py,*/*/__init__.py"'),
    ('MAKE_MIGRATION', 'docker-compose run --rm src sh -c "python manage.py makemigrations"'),
    ('MIGRATE', 'docker-compose run --rm src sh -c "python manage.py migrate"'),
    ('SHOW_URLS', 'docker-compose run --rm src sh -c "python manage.py show_urls"'),

    ('PRODUCTION/BUILD', 'docker-compose -f docker-compose-deploy.yml build'),
    ('PRODUCTION/RUN', 'docker-compose -f docker-compose-deploy.yml up'),
    ('PRODUCTION/DOWN', 'docker-compose -f docker-compose-deploy.yml down'),
]


WHITE = '\033[0m'  # white (normal)
RED = '\033[31m'  # red
GREEN = '\033[32m'  # green
ORANGE = '\033[33m'  # orange
BLUE = '\033[34m'  # blue
PURPLE = '\033[35m'  # purple


KEY_COLORS = {
    "ERROR": RED,
    "WARN": ORANGE,
    "!!!": ORANGE,
    "[INFO]": GREEN,
    "[DEBUG]": GREEN,
    "LOG:": GREEN,
    "***": GREEN,
}


lock = threading.Lock()

def get_user_input() -> int:
    print("\n\t\t\t*" + RED + " ♥ " + WHITE + "* * * * * * * * * * * * * * * * * * *")
    print("\t\t\t*   " + GREEN + "Developer" + WHITE + " Command Line Interface:\t*")
    print("\t\t\t* * * * * * * * * * * * * * * * * * *" + RED + " ♥ " + WHITE + "*")
    for i in range(0, len(COMMANDS)):
        print(f'\t\t\t {i+1}\t{COMMANDS[i][0]} >_ {BLUE}{COMMANDS[i][1]}{WHITE}')
    print(f'\t\t\t -{0}-\texit')

    number = input(f'\t\t\t {PURPLE}enter a number: {WHITE}')
    if not number.isdigit() or not -1 < int(number) < len(COMMANDS) + 1:
        print(f'Inputs must be a numbers (0-{len(COMMANDS)})')
        return -1
    else:
        return int(number)


def find_and_replace_with_color(output: str):
    for key in KEY_COLORS:
        if key in output.upper():
            return f'{KEY_COLORS[key]}{output}{WHITE}'
    return output


def execute_command(command):
    print(GREEN + f"{datetime.datetime.now()}> Executing: " + RED + command + WHITE)
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    time.sleep(4)
    try:
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                exit_status = process.poll()
                print(GREEN + f"{datetime.datetime.now()}> Done with exit status: " + RED + str(exit_status) + WHITE)
                break
            if output:
                line_output = find_and_replace_with_color(
                    output.strip().decode()
                )
                print(line_output)
                time.sleep(.04)

    except Exception as e:
        print("Interrupt exception!!: " + e.__str__())


def re_call_cli():
    number = -1
    while number == -1:
        number = get_user_input()
        if 0 < number < len(COMMANDS):
            execute_command(COMMANDS[number-1][1])
        elif number == -1:
            continue
        elif number == 0:
            print(PURPLE + "Exiting...\nfollow the white rabbit :)" + WHITE)
            break
        number = -1


if __name__ == "__main__":
    try:
        re_call_cli()
    except KeyboardInterrupt:
        print('\nInterrupted caught!\n' \
              + PURPLE + "follow the white rabbit :)" + WHITE)
        sys._exit(0)
