import pandas as pd
import pytest
import traceback
import pathlib

from membrane_detection.class_membrane_new import *

class TestPandasMunch:


    def test_missing_folder(fname):
        fname = pathlib.Path('teststs')
        with pytest.raises(ValueError):
            MembraneDetect(fname)

    def test_missing_images(fname):
        fname = pathlib.Path('empty folder')
        with pytest.raises(ValueError):
            MembraneDetect(fname)

    def test_old_data_missing(fname):
        fname = pathlib.Path('empty folder')
        old_data=pathlib.Path('teststs.xlsx')
        with pytest.raises(ValueError):
            MembraneDetect(fname, old_data=old_data)
    
    # def test_old_data_empty(fname):
    #     fname = pathlib.Path('images for testing')
    #     old_data=pathlib.Path('empty excel.xlsx')
    #     with pytest.raises(ValueError):
    #         MembraneDetect(fname, old_data=old_data)
    
    def test_N_positive(fname):
        fname = pathlib.Path('images for testing')
        with pytest.raises(ValueError):
            MembraneDetect(fname, N=-1)
    


if __name__ == "__main__":
    test_functions = ["test_missing_folder", "test_missing_images", "test_old_data_missing","test_N_positive"]
    errors = []
    ttests = TestPandasMunch()

    for func in test_functions:
        try:
            getattr(ttests, func)()
        except Exception as e:
            track = traceback.format_exc()
            print(track)
            errors.append(f"Failed when testing method '{func}': {e}")
    if len(errors) > 0:
        print(errors)
    else:
        print("Tests pass successfully.")
