from time import sleep
from random import randint


def get_randint():
    """
    Receives no argument. Opens 'prng-service.txt'. If the file reads "run", erases "run", generates a random positive integer and writes that integer (as a string) into the text file. Otherwise, does nothing.
    """
    while True:
        sleep(1)
        with open('prng-service.txt', 'r+') as file:
            is_run = file.read()
            if is_run == 'run':
                random_num = randint(0, 100000)
                sleep(2.5)
                file.truncate(0)
                file.seek(0)
                file.write(str(random_num))


if __name__ == "__main__":
    get_randint()
