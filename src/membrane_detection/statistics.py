import pandas as pd
import pathlib
from openpyxl import load_workbook
import researchpy


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
    gr1, gr2 = groups_IOD('ApoER2 colocalization.xlsx')
    a1, a2 = stat_groups('ApoER2 colocalization.xlsx', gr1, gr2)
    export_stat(a1, a2, 'ApoER2')
    gr3, gr4 = groups_colocalization('ApoER2 colocalization.xlsx', 'Rab5')
    a3, a4 = stat_groups('ApoER2 colocalization.xlsx', gr3, gr4)
    export_stat(a3, a4, 'Rab5')
