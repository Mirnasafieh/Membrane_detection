import pandas as pd
import pytest
import traceback
import pathlib
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

    def test_wrong_data_type(self):
        fname = pathlib.Path('images for testing')
        old = 'word for test.docx'
        with pytest.raises(TypeError):
            MembraneDetect(fname, old_data=old)
    
    # def test_old_data_empty(self):
    #     fname = pathlib.Path('images for testing')
    #     old_data=pathlib.Path('empty excel.xlsx')
    #     with pytest.raises(ValueError):
    #         MembraneDetect(fname, old_data=old_data)
    
    def test_N_positive(self):
        fname = 'images for testing'
        with pytest.raises(ValueError):
            MembraneDetect(fname, N=-1)
    


if __name__ == '__main__':
    ttests = TestPandasMunch()
    methods = ["missing_folder", "wrong_input_type", "missing_images", "old_data_missing", "old_data_missing", "wrong_data_type", "N_positive"]
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
