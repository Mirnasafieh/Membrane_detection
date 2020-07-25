import pathlib

def create_folder(path):
    new_folder_name = path+"\Membrane_images"
    pathlib.Path(new_folder_name).mkdir()

def export_membrane_image(img):
    


if __name__ == "__main__":

    create_folder('D:\DannyM19\Desktop\Membrane detection\images')
