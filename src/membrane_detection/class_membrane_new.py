import pathlib
import skimage
import skimage.io
import researchpy
import multiprocessing
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from skimage.util import img_as_ubyte
from scipy.ndimage import gaussian_filter
from skimage.filters import unsharp_mask
from skimage import exposure, morphology, feature
from skimage.morphology import dilation, closing, disk
from openpyxl import load_workbook
from skimage.color import rgb2gray
from skimage.io import imsave
import time
# import cProfile


class MembraneDetect:

    def __init__(self, foldername, old_data=None, N=1):
        self.images_list = []
        self.compartment_names = ["Rab5", "Rab7", "CatD", "Rab11", "Nucleus"]
        self.data = pd.DataFrame()
        self.old_data = pd.DataFrame()
        self.membrane = pathlib.PurePath()
        self.N = N
        if (self.N < 1) | (isinstance(self.N, int) is False):
            raise ValueError(f"ValueError exception thrown: experiment number:'{self.N}' is not valid")
        if pathlib.Path(foldername).is_dir():
            self.foldername = pathlib.Path(foldername)
            if len(list(self.foldername.glob('**/*.tif'))) == 0:
                raise ValueError(f"ValueError exception thrown:'{foldername}' is empty")
        else:
            raise ValueError(f"ValueError exception thrown:'{foldername}' does not exist")
        if (old_data is not None):
            # if old_data.endswith('.xlsx', '.xls') is False:
            #     raise ValueError(f"ValueError exception thrown:'{old_data}' is not an excel file")
            # elif self.old_data.empty:
            #     print(f"'{old_data}' is empty")
            if (pathlib.Path(old_data).exists()):
                self.old_data = pd.read_excel(old_data)
                # print(self.old_data.columns)
                # if list(self.old_data.columns) != ['cell genotype', 'N', 'cell number']:
                #     print(f"'{old_data}' has invalid data")

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
        """Returns measurements of an image"""
        total_area = img.size
        stained_area = np.count_nonzero(img)
        percent_area = (stained_area / total_area)
        total_intensity = np.sum(img)
        mean_intensity = np.mean(img)
        intigrated_optical_density = (mean_intensity * stained_area)
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
        cell_num_E3 = 0
        cell_num_E4 = 0
        mem_im = []
        for i in range(len(self.images_list)):
            image_bf = self.grayscale(self.images_list[i][0])
            mem_im = img_as_ubyte(self.membrane_detect(image_bf))
            image_fl = self.grayscale(self.images_list[i][1])
            new_im = self.compare_images(mem_im, image_fl)
            image_name = self.images_list[i][0].name
            imsave(pathlib.Path(self.membrane, image_name).with_suffix('.tif'), mem_im, check_contrast=False)
            cell_genotype = self.cell_genotype(image_name)
            if (cell_genotype == 'E3'):
                cell_num_E3 += 1
                cell_num = cell_num_E3
            if (cell_genotype == 'E4'):
                cell_num_E4 += 1
                cell_num = cell_num_E4
            total_area, stained_area, percent_area, total_intensity, mean_intensity, intigrated_optical_density = self.image_measurements(new_im, cell_genotype, i)
            results.update({
                                "cell genotype": cell_genotype,
                                "N": self.N,
                                "cell number": cell_num,
                                "total area": total_area,
                                "stained area": stained_area,
                                "percent area": percent_area,
                                "total_intensity": total_intensity,
                                "mean_intensity": mean_intensity,
                                "intigrated_optical_density": intigrated_optical_density
                            })
            self.data = self.data.append((pd.DataFrame.from_dict(results, orient='index')).T)

    def data_merge(self):
        """This function merges between two dataframes- the existing one and the output dataframe"""
        """according to cell genotype, N, and cell number"""
        if any(self.data.N == self.N):
            self.data = pd.merge(self.old_data, self.data, how='left', left_on=['cell genotype', 'N', 'cell number'],
                                        right_on=['cell genotype', 'N', 'cell number'])
        else:
            self.data = pd.concat([self.old_data, self.data], ignore_index=True, sort=False)
    
    # @timer
    def barplot_E3E4_membrane(self):
        """ This function creates a bar graph according to the parameters given"""
        graph = sns.barplot(x="cell genotype", y="intigrated_optical_density", palette="Greens", data=self.data).set_title("Receptor membrane IOD")
        return graph

    def barplot_E3E4_total(self):
        graph = sns.barplot(x="cell genotype", y="IOD", palette="Greens", data=self.data).set_title("Receptor total IOD")
        return graph

    def all_compartments_lines(self):
        """This function creates a line graph of both genottypes in all the compartments for given receptor"""
        graph = sns.catplot(x="compartment", y="M1", hue="cell genotype", palette="Greens", markers=["^", "o"],
                            linestyles=["--", "--"], kind="point", data=self.data)
        return graph

    def all_compartments_bars(self):
        """This function creates a barplot map of both genotypes in all the compartments for given receptor"""
        g = sns.FacetGrid(self.data, col="compartment", height=4, aspect=.5)
        result = g.map(sns.barplot, "cell genotype", "M1", palette='Greens')
        return result

    def save_graph(self, graph, file_name):
        file_name = file_name + ".pdf"
        file_path = pathlib.Path(self.membrane) / file_name
        plt.savefig(file_path)

    def export_graphs_receptor(self):
        """export graphs of receptor to PDF"""
        barplot_graph = self.barplot_E3E4_membrane()
        self.save_graph(barplot_graph, "Receptor membrane bound IOD")

    def export_graphs_compartment(self):
        """export graphs of compoartment to PDF"""
        all_comp_lines = self.all_compartments_lines()
        self.save_graph(all_comp_lines, "compartments lines")
        all_comp_bars = self.all_compartments_bars()
        self.save_graph(all_comp_bars, "compartments bars")
        barplot_E3E4_mem = self.barplot_E3E4_total()
        self.save_graph(barplot_E3E4_mem, "Receptor total bars")

    def groups_receptor_membrane(self):
        """Returns two groups of IOD parameter for receptor variable sorted by genotype"""
        group1 = self.data['intigrated_optical_density'].where(self.data['cell genotype'] == 'E3').dropna()
        group2 = self.data['intigrated_optical_density'].where(self.data['cell genotype'] == 'E4').dropna()
        if (len(group1) == 0) | (len(group2) == 0):
            raise ValueError(f"ValueError exception thrown: data is missing")
        return group1, group2

    def groups_receptor_total(self):
        """Returns two groups of IOD parameter for receptor variable sorted by genotype"""
        group1 = self.data['IOD'].where(self.data['cell genotype'] == 'E3').dropna()
        group2 = self.data['IOD'].where(self.data['cell genotype'] == 'E4').dropna()
        if (len(group1) == 0) | (len(group2) == 0):
            raise ValueError(f"ValueError exception thrown: data is missing")
        return group1, group2

    def groups_colocalization(self, name_com):
        """Returns two groups of M1 parametr for compartment parametr sorted by genotype"""
        group1 = self.data['M1'].where((self.data['cell genotype'] == 'E3') & (self.data['compartment'] == name_com)).dropna()
        group2 = self.data['M1'].where((self.data['cell genotype'] == 'E4') & (self.data['compartment'] == name_com)).dropna()
        return group1, group2

    def stat_groups(self, group1, group2):
        """Returns statistic analysis of two groups"""
        descriptive_table, result_table = researchpy.ttest(group1, group2)
        descriptive_table = descriptive_table.rename(index={0: 'ApoE3', 1: 'ApoE4', 2: 'ApoE3 + ApoE4'})
        return descriptive_table, result_table

    def export_stat(self, descriptive_table, result_table, name_var):
        """Export data to excel file"""
        sum_file = pathlib.Path(self.membrane) / 'sum statistics.xlsx'
        if sum_file.exists():
            book = load_workbook(sum_file)
            with pd.ExcelWriter(sum_file, engine='openpyxl') as writer:
                writer.book = book
                writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
                descriptive_table.to_excel(writer, sheet_name=name_var + '_Statistics')
                result_table.to_excel(writer, sheet_name=name_var + '_T-test')
                writer.save()
        else:
            with pd.ExcelWriter(sum_file, engine='xlsxwriter') as writer:
                descriptive_table.to_excel(writer, sheet_name=name_var + '_Statistics')
                result_table.to_excel(writer, sheet_name=name_var + '_T-test')
                writer.save()

    def statistics_analysis_receptor_membrane(self):
        """Returns statistics of receptor membrane IOD of two groups"""
        g1_membrane, g2_membrane = self.groups_receptor_membrane()
        des, res = self.stat_groups(g1_membrane, g2_membrane)
        self.export_stat(des, res, "Receptor_membrane")

    def statistics_analysis_receptor_total(self):
        """Returns statistics of receptor total IOD of two groups"""
        g1_total, g2_total = self.groups_receptor_total()
        des, res = self.stat_groups(g1_total, g2_total)
        self.export_stat(des, res, "Receptor_total")

    def statistics_analysis_compartment(self):
        """Returns statistics of compartment M1 of two groups"""
        for name_com in self.compartment_names:
            g1_com, g2_com = self.groups_colocalization(name_com)
            if (len(g1_com) == 0) | (len(g2_com) == 0):
                print(f"data of '{name_com}' is missing")
            else:
                des, res = self.stat_groups(g1_com, g2_com)
                self.export_stat(des, res, name_com)

    def create_folder(self):
        self.membrane = self.foldername / 'membrane_images'
        pathlib.Path(self.membrane).mkdir()

    def export_df(self):
        file_path = pathlib.Path(self.membrane) / 'sum results.xlsx'
        self.data.to_excel(file_path)

    # def time_fun(self):
    #     p = cProfile.Profile()
    #     p.runcall(self.statistics_analysis_receptor_membrane)
    #     p.print_stats()

    def all_pipeline(self):
        self.import_images()
        # self.time_fun()
        self.create_folder()
        self.all_images_analysis()
        if self.old_data.empty is False:
            self.data_merge()
            self.export_graphs_compartment()
            self.statistics_analysis_compartment()
            self.statistics_analysis_receptor_total()
        self.export_graphs_receptor()
        self.statistics_analysis_receptor_membrane()
        self. export_df()


if __name__ == "__main__":
    mem_det = MembraneDetect('images for testing')
    mem_det.import_images()
    mem_det.all_images_analysis()
    print (list(mem_det.data.columns))

    
