import pathlib
import matplotlib.pyplot as plt


def create_folder(path):
    new_folder_path = path+"\Membrane_images"
    pathlib.Path(new_folder_path).mkdir()


if __name__ == "__main__":
    path='D:\DannyM19\Desktop\Membrane detection\images'

    create_folder(path)
