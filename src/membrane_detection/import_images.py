from PIL import Image
import pathlib
import matplotlib.pyplot as plt 

def import_images(foldername):
  X_data = []
  pathname = pathlib.Path(foldername)
  for x in pathname.iterdir():
    xname = pathlib.Path(x).name
    if xname.endswith('01.tif'):
      im = Image.open(x)
      plt.imshow(im)
      plt.show()
      X_data.append(im)
  print (X_data)

if __name__ == "__main__":
  import_images('images')
