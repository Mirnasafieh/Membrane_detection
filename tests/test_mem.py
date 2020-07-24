import pandas as pd
import pytest
import traceback

from statistics, roi_transfer, import_images, image_analysis, graphs_stats, data_handeling, canny_mirna, plot_edge_filter import *


class TestPandasMunch:

    fname = '311_service_requests.zip'

    def test_common_complaint(self):
        ans = common_complaint(self.fname)
        assert ans == ('HEATING', 73371)

    def test_parking_borough(self):
        ans = parking_borough(self.fname)
        assert ans == 'BROOKLYN'

if __name__ == "__main__":
    test_functions = ["test_parking_borough", "test_common_complaint"]
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
