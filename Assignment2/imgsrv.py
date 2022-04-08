from time import sleep


def get_img_path():
    """
    """
    total_img = 100
    while True:
        sleep(1)
        with open('image-service.txt', 'r+') as file:
            is_num = file.read()
            if is_num.isdigit():
                num = int(is_num)
                sleep(2.5)
                img_num = num % total_img
                file.truncate(0)
                file.seek(0)
                file.write(
                    f'./ass2-images/{img_num}.jpg')


if __name__ == "__main__":
    get_img_path()
