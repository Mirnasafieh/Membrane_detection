import pathlib
from os import path, listdir


def import_images(foldername):
    """Return list of pairs of images (fluorecent anf BF)"""
    images_data = []
    pathname = pathlib.Path(foldername)
    for file1 in pathname.iterdir():
        filename1 = pathlib.Path(file1).name
        tup = ()
        if filename1.endswith('01.tif'):
            temp = filename1[:-6]
            for file2 in pathname.iterdir():
                if pathlib.Path(file2).name == (temp + "02.tif"):
                    tup = (file1, file2)
                    images_data.append(tup)
    return images_data


if __name__ == "__main__":
    # a=import_images('images for testing')
    # print (a[0])
    directory = 'D:\DannyM19\Desktop\Membrane detection\images for testing\membrane_images'
    imges= list(f for f in listdir(directory) if f.endswith('.tif'))
    print( len(imges))
