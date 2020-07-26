import pandas as pd
import pytest
import traceback
import pathlib
from cv2 import cv2
from membrane_detection.class_membrane_new import *

class TestPandasMunch:

    def test_missing_folder(self):
        fname = pathlib.Path('teststs')
        with pytest.raises(ValueError):
            MembraneDetect(fname)

    def test_wrong_input_type(self):
        fname = 2
        with pytest.raises(TypeError):
            q = MembraneDetect(pathlib.Path(fname))

    def test_missing_images(self):
        fname = pathlib.Path('empty folder')
        with pytest.raises(ValueError):
            MembraneDetect(fname)

    def test_old_data_missing(self):
        fname = pathlib.Path('empty folder')
        old_data=pathlib.Path('teststs.xlsx')
        with pytest.raises(ValueError):
            MembraneDetect(fname, old_data=old_data)
    
    #failed
    def test_wrong_data_type(self):
        fname = pathlib.Path('images for testing')
        old = 'word for test.docx'
        with pytest.raises(TypeError):
            MembraneDetect(fname, old_data=old)
    
    def test_N_positive(self):
        fname = 'images for testing'
        with pytest.raises(ValueError):
            MembraneDetect(fname, N=-1)

    #failed
    def test_old_data_structure(self):
        fname = pathlib.Path('images for testing')
        old = 'test excel.xlsx'
        with pytest.raises(TypeError):
            MembraneDetect(fname, old_data=old)                            
 
    def test_import_images_output_islist(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        
        assert type(mem_det.images_list) is list
    
    def test_import_images_output_len(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        
        assert len(mem_det.images_list)==4
    
    def test_import_images_output_list_tuples(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        assert isinstance(mem_det.images_list[0], tuple)

    def test_import_images_output_len_tuples(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        assert len (mem_det.images_list[0])==2

    #not working
    def test_import_images_output_pairs(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        file1=pathlib.WindowsPath('images for testing/e3 hol 1250 1500_z0_ch01.tif')
        file2= pathlib.WindowsPath('images for testing/e3 hol 1250 1500_z0_ch02.tif')
        tup= tuple(file1,file2)
        assert mem_det.images_list[0]==tup

    def test_grayscale_output_shape(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)

        assert img_gray.shape == (1024, 1024)
    
    def test_grayscale_output(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)

        assert len(img_gray.shape)< 3

    def test_membrane_detect_shape(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert membrane.shape == (1024, 1024)
    
    def test_membrane_detect_binary(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert len(np.unique(membrane)) == 2
    
    def test_membrane_detect_output(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im_path='D:\DannyM19\Desktop\Membrane detection\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert np.count_nonzero(membrane) <(1024*1024)

    # def test_compate_imgs(self):
    #     fname = pathlib.Path('images for testing')
    #     mem_det = MembraneDetect(fname)
    #     im1=
    #     im2=
    #     im_compare=mem_det.compare_images(im1, im2)

    #     assert im_compare


if __name__ == '__main__':
    ttests = TestPandasMunch()
    methods = ["missing_folder", "wrong_input_type", "missing_images", "old_data_missing", "old_data_missing", "wrong_data_type", "N_positive", "old_data_structure",
    "import_images_output_islist", "test_import_images_output_len", "import_images_output_list_tuples", "import_images_output_len_tuples", "import_images_output_pairs", 
    "grayscale_output_shape", "grayscale_output", "membrane_detect_shape", "membrane_detect_binary", "membrane_detect_output"]
    errors = []

    for method in methods:
        try:
            getattr(ttests, "test_" + method)()
        except AssertionError as e:
            errors.append(f"Failed when testing method 'test_{method}': {e}")

    if len(errors) > 0:
        print(errors)
    else:
        print("Tests pass successfully.")
