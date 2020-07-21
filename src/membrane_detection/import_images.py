import pathlib


def import_images(foldername):
    images_data = []
    pathname = pathlib.Path(foldername)
    for file in pathname.iterdir():
        filename = pathlib.Path(file).name
        tup = ()
        if filename.endswith('01.tif'):
            temp = filename[:-6]
            for file2 in pathname.iterdir():
                if pathlib.Path(file2).name == (temp + "02.tif"):
                    tup = (file, file2)
                    images_data.append(tup)
    return images_data

if __name__ == "__main__":
    import_images('images')