import subprocess
import shlex
import datetime

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
    ('FLAKE8', 'docker-compose run --rm src sh -c flake8 --exclude=core/migrations/'),
]


W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


def get_user_input() -> int:
    print("\n\t\t\t*" + R + " ♥ " + W + "* * * * * * * * * * * * * * * * * * *")
    print("\t\t\t*   " + G + "Developer" + W + " Command Line Interface:\t*")
    print("\t\t\t* * * * * * * * * * * * * * * * * * *" + R + " ♥ " + W + "*")
    for i in range(0, len(COMMANDS)):
        print(f'\t\t\t {i} - {COMMANDS[i][0]} {B}{COMMANDS[i][1]}{W}')
    print(f'\t\t\t {len(COMMANDS)} - exit')

    number = input(f'\t\t\t {P}enter a number: {W}')
    if not number.isdigit() or int(number) < 0 or int(number) > 6:
        print('Inputs must be a numbers (0-6)')
        return -1
    else:
        return int(number)


def execute_command(command):
    print()
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    try:
        print(G + f"{datetime.datetime.now()}> Executing: " + R + command)
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                exit_status = process.poll()
                print(G + f"{datetime.datetime.now()}> Done with exit status: " + R + str(exit_status) + W)
                break
            if output:
                print(O + output.strip().decode())
    except Exception as e:
        print("Interrupt exception!!: " + e.__str__())


def re_call_cli():
    number = -1
    while number == -1:
        number = get_user_input()
        if 0 < number < len(COMMANDS):
            execute_command(COMMANDS[number][1])
        elif number == -1:
            continue
        elif number == len(COMMANDS):
            print("\n" + P + "Exiting - Good luck! :))" + W)
            break
        number = -1


if __name__ == "__main__":
    re_call_cli()
