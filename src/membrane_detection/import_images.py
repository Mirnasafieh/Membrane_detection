import pathlib


def import_images(foldername):
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
    import_images('images')