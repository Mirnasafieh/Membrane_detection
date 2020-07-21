import pathlib


def import_images(foldername):
    images_data = []
    pathname = pathlib.Path(foldername)
    for file in pathname.iterdir():
        filename = pathlib.Path(file).name
        tup = ()
        if filename.endswith('01.tif'):
            temp = filename[:-6]
            secondfile = temp + "02.tif"
            for file2 in pathname.iterdir():
                filename2 = pathlib.Path(file2).name
                if filename2 == secondfile:
                    tup = (file, file2)
                    images_data.append(tup)
    return images_data