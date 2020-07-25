import pathlib
import pandas as pd
# from tifffile import imsave
import numpy as np
import matplotlib.pyplot as plt
import skimage
import skimage.io
import researchpy
import seaborn as sns
from scipy.ndimage import gaussian_filter
# from skimage.filters import meijering, sato, frangi, hessian, threshold_otsu, rank, unsharp_mask
from skimage.filters import unsharp_mask
from skimage import exposure, morphology, feature
# from skimage.morphology import erosion, dilation, opening, closing, white_tophat, flood_fill, black_tophat, skeletonize, convex_hull_image, disk, closing, square
from skimage.morphology import dilation, closing, disk
from openpyxl import load_workbook
from skimage.color import rgb2gray


class MembraneDetect:

    def __init__(self, foldername):
        self.image_bf = []
        self.image_fl = []
        self.images_list = []
        # self.results = {}
        self.compartment_names = ["Rab5", "Rab7", "CatD", "Rab11", "Nucleus"]
        self.data = pd.DataFrame()
        if pathlib.Path(foldername).is_dir():
            self.foldername = pathlib.Path(foldername)
            if len(list(self.foldername.glob('**/*.tif'))) == 0:
                raise ValueError(f"ValueError exception thrown:'{foldername}' is empty")
        else:
            raise ValueError(f"ValueError exception thrown:'{foldername}' does not exist")
        # # only if old_data exiists
        # if pathlib.Path(old_data).exists():
        #     self.data = pd.read_excel(old_data)
        #     if self.data.empty:
        #         raise ValueError(f"ValueError exception thrown:'{old_data}' is empty")
        # else:
        #     raise ValueError(f"ValueError exception thrown:'{old_data}' does not exist")
        
    def import_images(self):
        """Return list of pairs of image pathlibs (fluorecent anf BF)"""
        for file1 in self.foldername.iterdir():
            filename1 = pathlib.Path(file1).name
            tup = ()
            if filename1.endswith('01.tif'):
                temp = filename1[:-6]
                for file2 in self.foldername.iterdir():
                    if pathlib.Path(file2).name == (temp + "02.tif"):
                        tup = (file1, file2)
                        self.images_list.append(tup)

    def grayscale(self, img_path):
        """converts the image into a grayscale"""
        # img = img_path.name()
        original = skimage.io.imread(img_path)
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
        total_area = img.size
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

    def all_images_analysis(self):
        """go through all images and adds measurements to df"""
        results = {}
        for i in range(len(self.images_list)):
            image_bf = mem_det.grayscale(self.images_list[i][0])
            mem_det.membrane_detect(image_bf)
            image_fl = mem_det.grayscale(self.images_list[i][1])
            new_im = mem_det.compare_images(image_bf, image_fl)
            image_name = self.images_list[i][0].name
            cell_genotype = mem_det.cell_genotype(image_name)
            total_area, stained_area, percent_area, total_intensity, mean_intensity, intigrated_optical_density = mem_det.image_measurements(new_im, cell_genotype, i)
            results.update({
                                "Cell genotype": cell_genotype,
                                "Cell number": i,
                                "total area": total_area,
                                "stained area": stained_area,
                                "percent area": percent_area,
                                "total_intensity": total_intensity,
                                "mean_intensity": mean_intensity,
                                "intigrated_optical_density": intigrated_optical_density
                                })
            self.data = self.data.append((pd.DataFrame.from_dict(results, orient='index')).T)

    # def data_merge(self, df):
    #     """This function merges between two dataframes - the existing one and the output dataframe according to cell genotype, N, and cell number"""
    #     self.data = pd.merge(self.data, df, how='left', left_on=['cell genotype' , 'N', 'Cell number'], right_on=['cell genotype' ,'N' ,'Cell number'])

    def barplot_E3E4(self):
        """ This function creates a bar graph according to the parameters given"""
        graph = sns.barplot(x="Cell genotype", y="intigrated_optical_density", palette="Greens", data=self.data).set_title("Receptor IOD")
        return graph

    def all_compartments_lines(self):
        """This function creates a line graph of both genottypes in all the compartments for given receptor"""

        graph = sns.catplot(x="compartment", y="M1", hue="cell genotype", palette="Greens", markers=["^", "o"],
                            linestyles=["--", "--"], kind="point", data=self.data)
        return graph

    # def all_compartments_bars(self):
    #     """This function creates a barplot map of both genotypes in all the compartments for given receptor"""    
    #     g = sns.FacetGrid(self.data, col="compartment", height=4, aspect=.5)
    #     result = g.map(sns.barplot, "cell genotype", "M1", palette='Greens')
    #     return result

    def save_graph(self, graph, file_name):
        saving_name = file_name.split()[0]
        plt.savefig(saving_name + ".pdf")

    def export_graphs(self):
        """export graphs to PDF"""
        barplot_graph = mem_det.barplot_E3E4()
        # line_graph = mem_det.all_compartments_lines()
        mem_det.save_graph(barplot_graph, "barplot")
        # mem_det.save_graph(line_graph, "line graph")

    def groups_IOD(self):
        """Returns two groups of IOD parameter for receptor variable sorted by genotype"""
        group1 = self.data['intigrated_optical_density'].where(self.data['Cell genotype'] == 'E3').dropna()
        group2 = self.data['intigrated_optical_density'].where(self.data['Cell genotype'] == 'E4').dropna()
        if (len(group1) == 0) | (len(group2) == 0):
            raise ValueError(f"ValueError exception thrown: data is missing")
        return group1, group2

    def groups_colocalization(self, name_com):
        """Returns two groups of M1 parametr for compartment parametr sorted by genotype"""
        group1 = self.data['M1'].where(((self.data['cell genotype'] == 'e3') | (self.data['cell genotype'] == 'E3'))
                                        & (self.data['compartment'] == name_com)).dropna()
        group2 = self.data['M1'].where(((self.data['cell genotype'] == 'e4') | (self.data['cell genotype'] == 'E4'))
                                        & (self.data['compartment'] == name_com)).dropna()
        return group1, group2

    def stat_groups(self, group1, group2):
        """Returns statistic analysis of two groups"""
        descriptive_table, result_table = researchpy.ttest(group1, group2)
        descriptive_table = descriptive_table.rename(index={0: 'ApoE3', 1: 'ApoE4', 2: 'ApoE3 + ApoE4'})
        return descriptive_table, result_table

    def export_stat(self, descriptive_table, result_table, name_var):
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

    def statistics_analysis_and_export(self):
        g1_receptor, g2_receptor = mem_det.groups_IOD()
        des, res = mem_det.stat_groups(g1_receptor, g2_receptor)
        mem_det.export_stat(des, res, "Receptor")
        # compartment_names = ["Rab5", "Rab7", "CatD", "Rab11", "Nucleus"]
        # for name_com in compartment_names:
        #     g1_com, g2_com = mem_det.groups_colocalization(name_com)
        #     if (len(g1_com) == 0) | (len(g2_com) == 0):
        #         print("data of '{name_com}' is missing")
        #     else:
        #         des, res = mem_det.stat_groups(g1_com, g2_com)
        #         mem_det.export_stat(des, res, name_com)


if __name__ == "__main__":
    mem_det = MembraneDetect('images')
    mem_det.import_images()
    mem_det.all_images_analysis()
    mem_det.export_graphs()
    mem_det.statistics_analysis_and_export()
