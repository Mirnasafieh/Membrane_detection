__version__ = "0.1.0"
__title__ = "membrabe_detection"
__description__ = "Parse Stuff With Ease"
__url__ = "https://github.com/Mirnasafieh/Membrane_detection.git"
__doc__ = __description__ + " <" + __url__ + ">"
__author__ = "Mirna Safieh and Hila Ben-Moshe"
__email__ = "mirna.safieh.91@gmail.com"
__license__ = "MIT"

from membrane_detection.class_membrane_new import *

if __name__ == "__main__":
    mem_det = MembraneDetect('images', "old data ApoER2.xlsx")

    mem_det.all_pipeline()

