import os
import glob

def read_files():   # reading the excel files
    path = os.getcwd()
    path_xlsx = glob.glob(os.path.join(path,'*.xlsx'))

    return path_xlsx

