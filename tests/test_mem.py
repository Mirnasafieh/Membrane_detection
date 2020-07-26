import pandas as pd
import pytest
import traceback
import pathlib

from class_membrane_new import *

class TestPandasMunch:


    def test_missing_file():
        fname = pathlib.Path('teststs.fdfd')
        with pytest.raises(ValueError):
            MembraneDetect(fname)




if __name__ == "__main__":
    test_functions = ["test_missing_file"]
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
