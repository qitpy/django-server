import subprocess
import shlex

commands = [

]


W = '\033[0m'  # white (normal)
R = '\033[31m'  # red
G = '\033[32m'  # green
O = '\033[33m'  # orange
B = '\033[34m'  # blue
P = '\033[35m'  # purple


def get_user_input() -> int:
    print("\n\t\t\t* " + R + "♥" + W + " * * * * * * * * * * * * * * * * * * *")
    print("\t\t\t*   " + G + "Developer" + W + " Command Line Interface:\t*")
    print('\t\t\t*\t\t\t\t\t*')
    print('\t\t\t*\t1 - BUILD\t\t\t*')
    print('\t\t\t*\t2 - RUN\t\t\t\t*')
    print('\t\t\t*\t3 - DOWN\t\t\t*')
    print('\t\t\t*\t4 - TEST\t\t\t*')
    print('\t\t\t*\t5 - COVERAGE\t\t\t*')
    print('\t\t\t*\t6 - FLAKE8\t\t\t*')
    print('\t\t\t*\t0 - exit\t\t\t*')
    print("\t\t\t* * * * * * * * * * * * * * * * * * * " + R + "♥" + W + " *")
    number = input('\t\t\t your choice: ')

    if not number.isdigit() or int(number) < 0 or int(number) > 6:
        print('Inputs must be a numbers (0-6)')
        return -1
    else:
        return int(number)


def execute_command(command):
    print()
    process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE)
    try:
        print(G + "===> Executing: " + R + command)
        while True:
            output = process.stdout.readline()
            if not output and process.poll() is not None:
                rc = process.poll()
                print(G + "===> Done with exit status: " + R + str(rc) + W)
                break
            if output:
                print(O + output.strip().decode())
    except Exception as e:
        print("Interrupt exception!!: " + e.__str__())
    return rc


def re_call_cli():
    number = -1
    while number == -1:
        number = get_user_input()
        if number == -1:
            continue
        elif number == 1:
            execute_command('docker-compose build')
        elif number == 2:
            execute_command('docker-compose up')
        elif number == 3:
            execute_command('docker-compose down')
        elif number == 4:
            execute_command('docker-compose run --rm src sh -c "python manage.py test"')
        elif number == 5:
            execute_command('docker-compose run --rm src sh -c "coverage run manage.py test"')
            execute_command('docker-compose run --rm src sh -c "coverage report"')
        elif number == 6:
            execute_command('docker-compose run --rm src sh -c flake8 --exclude=core/migrations/')
        elif number == 0:
            print("\n" + P + "Exiting - Good luck! :))" + W)
            break
        number = -1


if __name__ == "__main__":
    re_call_cli()
