import pandas as pd
import pytest
import traceback
import pathlib
from cv2 import cv2
import os.path
from os import path, listdir
import glob
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
        fname = pathlib.Path('files for testing\empty folder')
        with pytest.raises(ValueError):
            MembraneDetect(fname)

    def test_old_data_missing(self):
        fname = pathlib.Path('files for testing\empty folder')
        old_data=pathlib.Path('files for testing\teststs.xlsx')
        with pytest.raises(ValueError):
            MembraneDetect(fname, old_data=old_data)
    
    def test_wrong_data_type(self):
        fname = pathlib.Path('files for testing\images for testing')
        old = 'word for test.docx'
        with pytest.raises(ValueError):
            MembraneDetect(fname, old_data=old)
    
    def test_N_positive(self):
        fname = 'files for testing\images for testing'
        with pytest.raises(ValueError):
            MembraneDetect(fname, N=-1)

    def test_old_data_structure(self):
        fname = pathlib.Path('files for testing\images for testing')
        old = 'test excel.xlsx'
        with pytest.raises(ValueError):
            MembraneDetect(fname, old_data=old)                            
 
    def test_import_images_output_islist(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        
        assert type(mem_det.images_list) is list
    
    def test_import_images_output_len(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        
        assert len(mem_det.images_list)==4
    
    def test_import_images_output_list_tuples(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        assert isinstance(mem_det.images_list[0], tuple)

    def test_import_images_output_len_tuples(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        assert len (mem_det.images_list[0])==2

    def test_import_images_output_pairs(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        file1=pathlib.WindowsPath('files for testing\images for testing/e3 hol 1250 1500_z0_ch01.tif')
        file2= pathlib.WindowsPath('files for testing\images for testing/e3 hol 1250 1500_z0_ch02.tif')
        tup= (file1,file2)
        assert mem_det.images_list[0]==tup

    def test_grayscale_output_shape(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)

        assert img_gray.shape == (1024, 1024)
    
    def test_grayscale_output(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)

        assert len(img_gray.shape)< 3

    def test_membrane_detect_shape(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert membrane.shape == (1024, 1024)
    
    def test_membrane_detect_binary(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert len(np.unique(membrane)) == 2
    
    def test_membrane_detect_output(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        membrane=mem_det.membrane_detect(img_gray)

        assert np.count_nonzero(membrane) <(1024*1024)

    #failed
    def test_compare_imgs(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im1 = skimage.io.imread("files for testing\images for testing\e3 hol 1250 1500_z0_membrane.tif")
        im_path="files for testing\images for testing\e3 hol 1250 1500_z0_ch02.tif"     
        im2=mem_det.grayscale(im_path)

        im_compare=mem_det.compare_images(im1, im2)
        assert np.count_nonzero(im_compare)==np.count_nonzero(im1)

    def test_compare_imgs_output_shape(self):
        fname = pathlib.Path('images for testing')
        mem_det = MembraneDetect(fname)
        im1 = skimage.io.imread("images for testing\e3 hol 1250 1500_z0_membrane.tif")
        im_path="images for testing\e3 hol 1250 1500_z0_ch02.tif"     
        im2=mem_det.grayscale(im_path)

        im_compare=mem_det.compare_images(im1, im2)
        assert im_compare.shape == (1024, 1024)

    def test_image_measurements(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        genotype="E3"
        cell_number=1
        l=list(mem_det.image_measurements(img_gray, genotype=genotype, cell_number=cell_number))      
        
        assert len(l)== 6

    def test_image_measurements_area(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        im_path='files for testing\images for testing\e3 hol 1250 1500_z0_ch01.tif'    
        img_gray=mem_det.grayscale(im_path)
        genotype="E3"
        cell_number=1
        l=list(mem_det.image_measurements(img_gray, genotype=genotype, cell_number=cell_number)) 
        assert l[0] <= img_gray.size  and   l[1] <= img_gray.size  and l[2]<=1

    def test_cell_genotype(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        image_name="e3 apoe testtest"
        geno= mem_det.cell_genotype(image_name)
        assert geno=="E3"

    def test_all_image_analysis_df_shape(self):
        fname = pathlib.Path('files for testing\images for testing')
        mem_det = MembraneDetect(fname)
        mem_det.import_images()
        mem_det.all_images_analysis()
        assert mem_det.data.shape[0]==4 and mem_det.data.shape[1]==9 and list(mem_det.data.columns)==['cell genotype', 'N', 'cell number', 'total area', 'stained area', 'percent area', 'total_intensity', 'mean_intensity', 'intigrated_optical_density']
    
    #N=2
    def test_data_merge_N(self):
        fname = pathlib.Path('files for testing\images for testing')
        old_data="files for testing\test merge1.xlsx"
        p = pathlib.Path(old_data)
        df_old = pd.read_excel(p)

        mem_det1 = MembraneDetect(fname,old_data=old_data,N=1)
        mem_det1.import_images()
        mem_det1.all_images_analysis()
        mem_det1.data_merge()
        
        mem_det2 = MembraneDetect(fname,old_data=old_data,N=2)
        mem_det2.import_images()
        mem_det2.all_images_analysis()
        mem_det2.data_merge()

        assert mem_det1.data.shape[0]== df_old.shape[0] #and mem_det2.data.shape[0] > df_old.shape[0]

    def test_pipeline_output_folder(self):
        
        fname = pathlib.Path('files for testing\images for testing')
        old_data="files for testing\test merge1.xlsx"
        mem_det = MembraneDetect(fname, old_data)
        mem_det.all_pipeline()
        assert path.exists ("files for testing\images for testing\membrane_images") 


    def test_pipeline_output_imgs(self):
        directory = 'files for testing\images for testing\membrane_images'
        imges= list(f for f in listdir(directory) if f.endswith('.tif'))
        assert len (imges)==4

    def test_pipeline_output_excel(self):
        directory = 'files for testing\images for testing\membrane_images'
        imges= list(f for f in listdir(directory) if f.endswith('.xlsx'))
        assert len (imges)>=2
    
    #not sure its supposed to be>=1
    def test_pipeline_output_graphs(self):
        directory = 'files for testing\images for testing\membrane_images'
        imges= list(f for f in listdir(directory) if f.endswith('.pdf'))
        assert len (imges)>=1

if __name__ == '__main__':
    ttests = TestPandasMunch()
    methods = ["missing_folder", "wrong_input_type", "missing_images", "old_data_missing", "old_data_missing", "wrong_data_type", "N_positive", "old_data_structure",
    "import_images_output_islist", "import_images_output_len", "import_images_output_list_tuples", "import_images_output_len_tuples", "import_images_output_pairs", 
    "grayscale_output_shape", "grayscale_output", "membrane_detect_shape", "membrane_detect_binary", "membrane_detect_output", "compare_imgs", "compare_imgs_output_shape", 
    "image_measurements", "image_measurements_area", "cell_genotype", "all_image_analysis_df_shape","data_merge_N", "pipeline_output_folder", "pipeline_output_imgs", 
    "pipeline_output_excel", "pipeline_output_graphs"]
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