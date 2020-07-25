import pandas as pd
import pathlib
from tifffile import imsave
import numpy as np

def data_import(filename):
    """this function import an excel file with the data and returns a pandas dataframe"""
        
    p = pathlib.Path(filename)
    df = pd.read_excel(p)
    return df

def data_merge(df1,df2,N):
    """This function merges between two dataframes - the existing one and the output dataframe according to cell genotype, N, and cell number"""

    if any(df1.N == N):

        result = pd.merge(df1, df2,  how='left', left_on=['cell genotype','N','Cell number'], right_on = ['cell genotype','N','Cell number'])
    else:
  
        result = pd.concat([df1, df2], ignore_index=True, sort=False)

    return result

def export_to_excel(df, name):
    """This function only exports the dataframe back into excel with a given name"""
    df.to_excel(name)

def export_tif(img, name):
    """This function exports an img as tif with a given name"""
    imsave(name, img)

if __name__ == "__main__":
    df1=data_import('ApoER2 colocalization.xlsx')
    df2=data_import('try merge.xlsx')
    df3=data_merge(df1,df2,2)
    export_to_excel(df3, "testing export.xlsx")

