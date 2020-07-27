from test_mem import *



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