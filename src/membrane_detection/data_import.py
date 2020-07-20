import pandas as pd
import pathlib

def data_import(filename):
    """this function import an excel file with the data and returns a pandas dataframe"""
        
    p = pathlib.Path(filename)
    df = pd.read_excel (p)
    return df


