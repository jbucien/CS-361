from time import sleep
from PIL import Image


def run_program():
    print("Welcome to Pokemon Image Generator!")
    sleep(0.5)
    answer = None
    while answer != '2':
        print("Press 1 to generate a new Pokemon image. Press 2 to exit")
        answer = input()
        if answer == '1':
            with open('prng-service.txt', 'w') as file:
                file.write('run')
            sleep(5)
            with open('prng-service.txt', 'r') as file1:
                num = file1.read()
            with open('image-service.txt', 'w') as file2:
                file2.write(num)
            sleep(5)
            with open('image-service.txt', 'r') as file3:
                img_path = file3.read()
            img_path_str = img_path[2:]
            print(
                f"The file path is: /users/jenna/CS-361/Assignment2/{img_path_str}")
            pokemon = Image.open(img_path)
            pokemon.show()
        if answer == '2':
            print("Thanks for using my program!")


if __name__ == "__main__":
    run_program()
