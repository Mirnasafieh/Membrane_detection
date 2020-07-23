## Import the packages
import numpy as np
from scipy import stats
import pandas as pd
from scipy.stats import ttest_ind
import researchpy
import csv
import openpyxl
from openpyxl import load_workbook


def groups_IOD(results_file):
    sum_data = pd.read_excel(results_file)
    group1 = sum_data['IOD'].where((sum_data['cell genotype'] == 'e3') | (sum_data['cell genotype'] == 'E3')).dropna()
    group2 = sum_data['IOD'].where((sum_data['cell genotype'] == 'e4') | (sum_data['cell genotype'] == 'E4')).dropna()
    return group1, group2


def groups_colocalization(results_file, name_com):
    sum_data = pd.read_excel(results_file)
    group1 = sum_data['M1'].where(((sum_data['cell genotype'] == 'e3') | (sum_data['cell genotype'] == 'E3'))
        & (sum_data['compartment'] == name_com)).dropna()
    group2 = sum_data['M1'].where(((sum_data['cell genotype'] == 'e4') | (sum_data['cell genotype'] == 'E4'))
        & (sum_data['compartment'] == name_com)).dropna()
    return group1, group2


def stat_groups(stat_file, group1, group2):
    descriptive_table, result_table = researchpy.ttest(group1, group2)
    descriptive_table = descriptive_table.rename(index={0: 'ApoE3', 1: 'ApoE4', 2: 'ApoE3 + ApoE4'})
    return descriptive_table, result_table


def export_stat(descriptive_table, result_table, name_var):
    with pd.ExcelWriter("sum statistics.xlsx", engine='xlsxwriter') as writer:
        descriptive_table.to_excel(writer, name_var + '_1')
        result_table.to_excel(writer, name_var + '_2')
        writer.save()


if __name__ == "__main__":
    gr1, gr2 = groups_IOD('ApoER2 colocalization.xlsx')
    a1, a2 = stat_groups('ApoER2 colocalization.xlsx', gr1, gr2)
    export_stat(a1, a2, 'ApoER2')
    gr3, gr4 = groups_colocalization('ApoER2 colocalization.xlsx', 'Rab5')
    a3, a4 = stat_groups('ApoER2 colocalization.xlsx', gr3, gr4)
    export_stat(a3, a4, 'Rab5')