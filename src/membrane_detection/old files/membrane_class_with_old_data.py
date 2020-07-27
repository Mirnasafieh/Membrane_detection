import pathlib
import pandas as pd
from tifffile import imsave
import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.io
from scipy.ndimage import gaussian_filter
from skimage.filters import meijering, sato, frangi, hessian, threshold_otsu, rank, unsharp_mask
from skimage import data, exposure, img_as_float, morphology, filters, feature, color
from skimage.morphology import erosion, dilation, opening, closing, white_tophat, flood_fill, black_tophat, skeletonize, convex_hull_image, disk, closing, square
import seaborn as sns
from openpyxl import load_workbook
import researchpy


class MembraneDetect:

    def __init__(self, old_data, foldername):
        # old_data - file may not be received
        self.image_bf = []
        self.image_fl = []
        # self.results
        if pathlib.Path(foldername).is_dir():
            self.foldername = pathlib.Path(foldername)
            if len(list(self.foldername.glob('**/*.tif'))) == 0:
                raise ValueError(f"ValueError exception thrown:'{foldername}' is empty")
        else:
            raise ValueError(f"ValueError exception thrown:'{foldername}' does not exist")
        # only if old_data exiists
        if pathlib.Path(old_data).exists():
            self.data = pd.read_excel(old_data)
            if self.data.empty:
                raise ValueError(f"ValueError exception thrown:'{old_data}' is empty")
        else:
            raise ValueError(f"ValueError exception thrown:'{old_data}' does not exist")
        
    def import_images(self):
        """Return list of pairs of images (fluorecent anf BF)"""
        images_data = []
        for file1 in self.foldername.iterdir():
            filename1 = pathlib.Path(file1).name
            tup = ()
            if filename1.endswith('01.tif'):
                temp = filename1[:-6]
                for file2 in self.foldername.iterdir():
                    if pathlib.Path(file2).name == (temp + "02.tif"):
                        tup = (file1, file2)
                        images_data.append(tup)
        print(images_data)
        return images_data

    def grayscale(self, img):
        """converts the image into a grayscale"""
        original = skimage.io.imread(img)
        grayscale = rgb2gray(original)
        return grayscale

    def membrane_detect(self, img_grayscale):
        """This fuction detects the membrane from a series of manipulations on a grayscale bright-field image"""
        """input: grayscale image"""
        """output: binary image"""

        # sharpened image:
        im_sharp = unsharp_mask(img_grayscale, radius=2, amount=2)

        # Equalization threshold:
        p2, p98 = np.percentile(im_sharp, (2, 98))
        im_eq = exposure.rescale_intensity(img_grayscale, in_range=(p2, p98))

        # Gaussian:
        im_gaus = gaussian_filter(im_eq, sigma=2.7)

        # Edge detection:
        im_edge = feature.canny(im_gaus, sigma=1)

        # Remove small objects:
        im_clean1 = morphology.remove_small_objects(im_edge, 200, in_place=True, connectivity=50)

        # Close:
        phantom = im_clean1
        phantom[10:30, 200:210] = 0
        selem_c = disk(10)
        im_closed = closing(phantom, selem_c)

        # Dialated:
        selem_d = disk(4)
        im_dialated = dilation(im_closed, selem_d)

        # Remove small objects:
        im_final = morphology.remove_small_objects(im_dialated, 1700, in_place=True, connectivity=200)

        return im_final

    def compare_images(self, img1, img2):
        """Returns new image with values of the fluorecent image where co-localization with membrane"""
        compare_im = np.copy(img2)
        compare_im = np.where(img1 == False, 0, compare_im)
        return (compare_im)

    def image_measurements(self, img, genotype, cell_number):
        # results_dict = {}
        # cell_genotype = genotype
        # N = N
        # cell_number = cell_number
        total_area = img.size()
        stained_area = np.count_nonzero(img)
        percent_area = stained_area / total_area
        total_intensity = np.sum(img)
        mean_intensity = np.mean(img)
        intigrated_optical_density = mean_intensity * stained_area  # check math

        # results_dict.update({"Cell genotype": cell_genotype, "N": N, "Cell number": cell_number, "total area": total_area, "stained area":stained_area, "percent area": percent_area, "total_intensity":total_intensity, "mean_intensity":mean_intensity, "intigrated_optical_density": intigrated_optical_density })
        # df = pd.DataFrame.from_dict(results_dict, orient='index')
        
        return total_area, stained_area, percent_area, total_intensity, mean_intensity, intigrated_optical_density

    def cell_genotype(self, image_name):
        """returns cell genotype from the name"""
        c_name = image_name.upper()
        if (c_name.find('E3') != -1):
            genotype = "E3"
        elif (c_name.find('E4') != -1):
            genotype = "E4"
        else:
            genotype = "Unknown"
        return genotype

    def data_merge(self, df):
        """This function merges between two dataframes - the existing one and the output dataframe according to cell genotype, N, and cell number"""
        self.data = pd.merge(self.data, df, how='left', left_on=['cell genotype' , 'N', 'Cell number'], right_on=['cell genotype' ,'N' ,'Cell number'])

    def barplot_E3E4(SELF, data, parameterx, parametery):
        """ This function creates a bar graph according to the parameters given"""
        graph = sns.barplot(x=parameterx, y=parametery, palette="Greens", data=data).set_title("Receptor IOD")
        return graph

    def all_compartments_lines(self, data):
        """This function creates a line graph of both genottypes in all the compartments for given receptor"""
        graph = sns.catplot(x="compartment", y="M1", hue="cell genotype", palette="Greens", markers=["^", "o"], 
        linestyles=["--", "--"], kind="point", data=data)
        return graph 

    def all_compartments_bars(data):
        """This function creates a barplot map of both genottypes in all the compartments for given receptor"""    
        g = sns.FacetGrid(data, col="compartment", height=4, aspect=.5)
        result= g.map(sns.barplot, "cell genotype", "M1", palette='Greens')
        return result

    def save_graph(graph, file_name, parameter):
        saving_name= file_name.split()[0]
        plt.savefig(saving_name+ parameter +".pdf")

    def groups_IOD(results_file):
    """Returns two groups of IOD parameter for receptor variable sorted by genotype"""
    sum_data = pd.read_excel(results_file)
    group1 = sum_data['IOD'].where((sum_data['cell genotype'] == 'e3') | (sum_data['cell genotype'] == 'E3')).dropna()
    group2 = sum_data['IOD'].where((sum_data['cell genotype'] == 'e4') | (sum_data['cell genotype'] == 'E4')).dropna()
    return group1, group2


    def groups_colocalization(results_file, name_com):
        """Returns two groups of M1 parametr for compartment parametr sorted by genotype"""
        sum_data = pd.read_excel(results_file)
        group1 = sum_data['M1'].where(((sum_data['cell genotype'] == 'e3') | (sum_data['cell genotype'] == 'E3'))
            & (sum_data['compartment'] == name_com)).dropna()
        group2 = sum_data['M1'].where(((sum_data['cell genotype'] == 'e4') | (sum_data['cell genotype'] == 'E4'))
            & (sum_data['compartment'] == name_com)).dropna()
        return group1, group2


    def stat_groups(stat_file, group1, group2):
        """Returns statistic analysis of two groups"""
        descriptive_table, result_table = researchpy.ttest(group1, group2)
        descriptive_table = descriptive_table.rename(index={0: 'ApoE3', 1: 'ApoE4', 2: 'ApoE3 + ApoE4'})
        return descriptive_table, result_table


    def export_stat(descriptive_table, result_table, name_var):
        """Export data to excel file"""
        sum_file = 'sum statistics.xlsx'
        if pathlib.Path(sum_file).exists():
            book = load_workbook(pathlib.Path(sum_file))
            with pd.ExcelWriter(pathlib.Path(sum_file), engine='openpyxl') as writer:
                writer.book = book
                writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
                descriptive_table.to_excel(writer, sheet_name=name_var + '_1')
                result_table.to_excel(writer, sheet_name=name_var + '_2') 
                writer.save()
        else:
            with pd.ExcelWriter(sum_file, engine='xlsxwriter') as writer:
                descriptive_table.to_excel(writer, sheet_name=name_var + '_1')
                result_table.to_excel(writer, sheet_name=name_var + '_2')
                writer.save()


if __name__ == "__main__":
    mem_det = MembraneDetect('hila.xlsx', 'images')
    images_data = mem_det.import_images()
    results_dict = {}
    for i in len(images_data):
        image_bf = mem_det.grayscale(images_data[i][0])
        image_bf.membrane_detect()
        image_fl = mem_det.grayscale(images_data[i][1])
        new_im = mem_det.compare_images(image_bf, image_fl)
        image_name = images_data[i][0].name()
        cell_genotype = mem_det.cell_genotype(image_name)
        total_area, stained_area, percent_area, total_intensity, mean_intensity, intigrated_optical_density = mem_det.image_measurements(new_im, cell_genotype, i)
        results_dict.update({"Cell genotype": cell_genotype, "Cell number": i, "total area": total_area, "stained area": stained_area, "percent area": percent_area,
        "total_intensity": total_intensity, "mean_intensity": mean_intensity, "intigrated_optical_density": intigrated_optical_density})
    new_results = pd.DataFrame.from_dict(results_dict, orient='index')
    mem_det.data_merge(new_results)
