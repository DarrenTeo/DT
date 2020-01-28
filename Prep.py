from tkinter import *
from tkinter import filedialog
import pandas as pd
import glob

##################################################################################
################################## Load CSV ######################################
##################################################################################

################################################################################## CSV Parameters ##################################################################################
def ParametersCSV():
    global delimiter
    global header_row
    global skip_footer
    global nrows

    delimiter = input("delimiter, default = ,: ") or ',' # input '\t' if tab delimiter    
    header_row = int(input("header_row, default = 0: ") or '0')
    skip_footer = int(input("skip_footer, default = 0: ") or '0')
    
    nrows = input("rows to read, default = None") or None # None = All
    try:
        nrows = int(nrows)
    except:
        nrows = nrows
    
    
def ReadCSV():
    global df
    
    df = pd.read_csv (import_file_path, 
                      sep = delimiter,
                      nrows = nrows,
                      header = header_row,
                      skipfooter = skip_footer,
                      engine='python')
                                    
################################################################################## Tkinter CSV ##################################################################################      
def LoadCSV():
    global import_file_path

    window = Tk()
    window.withdraw()
    import_file_path = filedialog.askopenfilename()
    
    ParametersCSV()                      
    ReadCSV(import_file_path,delimiter,nrows,header_row,skip_footer)
    
    print('\n\033[1m\033[4m'+'Loading this file:'+'\033[0m')
    print(import_file_path)
    
    Preview(df)

    window.destroy()
    
    
    
################################################################################## Tkinter All CSV ##################################################################################    
def LoadAllCSV():
    global import_file_path

    window = Tk()
    window.withdraw()
    import_file_path = filedialog.askopenfilename()
    
    print('\n\033[1m\033[4m'+'File Selected:'+'\033[0m\n'+import_file_path+'\n')
    ParametersCSV()
    ReadAllCSV()
    Preview(df)
    
    window.destroy()

################################################################################## Concat All CSV ##################################################################################    
def ReadAllCSV():
    FolderPath(import_file_path)                                  # 1. Get folder path
    FilenamePath(folder_path)                                     # 2. Get folder path with additional substring
    GlobCSV(file_type,filename_path)                       # 3. Pattern matching
    print('\n\033[1m\033[4m'+'Filenames Loaded:'+'\033[0m ')
    ConcatCSV(delimiter,nrows,header_row,skip_footer)                                          # 4. Concat csv files

# Step 1    
def FolderPath(import_file_path):                                         
    global folder_path
    
    path_split = import_file_path.split('/')            # Split path by /
    number_of_substrings = len(path_split)-1            # Count number of subfields
    
    folder_path=[]                                      # Create list based on splited directory without filename
    for i in range(0,number_of_substrings):
        folder_path.append(path_split[i])

    folder_path = '/'.join(folder_path)+'/'             # Create folder path without filename by joining above list
    
    print('\n\033[1m\033[4m'+'Accessing folder:'+'\033[0m\n'+folder_path+'\n')

# Step 2
def FilenamePath(folder_path):
    global filename_path
    global file_type
    
    additional_substring = input("Enter Additional Substring: ")
    filename_path = folder_path+additional_substring    # Input substring based on filename
    
    print('\n\033[1m\033[4m'+'Accessing files starting with:\n'+'\033[0m '+filename_path)
    
    file_type = import_file_path[-3:]
    
# Step 3    
def GlobCSV(file_type,filename_path):
    global all_files
    
    if file_type=='csv':
        all_files = glob.glob(filename_path + "*.csv")
    elif file_type=='txt':
        all_files = glob.glob(filename_path + "*.txt")
        
    
# Step 4    
def ConcatCSV(delimiter,nrows,header_row,skip_footer):
    global df

    li = []
    i=0
    for filename in all_files:
        ReadCSV(filename,delimiter,nrows,header_row,skip_footer)    # Read CSV
        li.append(df)                                                       # Append df
        i+=1                                                                # Loop next
        print(str(i)+': '+filename.split('\\')[-1])
        
    df = pd.concat(li, axis=0, ignore_index=True)                           # Concat
    
    
##################################################################################
################################## Load Excel ####################################
##################################################################################

################################################################################## Excel Parameters ##################################################################################
def ParametersExcel():
    global sheet
    global header_row
    global skip_footer
    global nrows

    sheet = input("sheet_name, default = 0: ") or 0 # 0 = 1st sheet
    header_row = int(input("header_row, default = 0: ") or '0')
    skip_footer = int(input("skip_footer, default = 0: ") or '0')
    
    nrows = input("rows to read, default = None") or None
    try:
        nrows = int(nrows)
    except:
        nrows = nrows
    
def ReadExcel(import_file_path,sheet,nrows,header_row,skip_footer):
    global df
    
    df = pd.read_excel(import_file_path,
                       sheet_name = sheet,
                       header = header_row,
                       skipfooter = skip_footer,
                       nrows = nrows)
                       
def PrintSheetNames():
    sheet_names = pd.ExcelFile(import_file_path).sheet_names
    print('\033[1m\033[4m'+'Excel Sheets:'+'\033[0m '+str(sheet_names))
                       
################################################################################## Tkinter Excel ##################################################################################      
def LoadExcel():
    global import_file_path

    window = Tk()
    window.withdraw()
    import_file_path = filedialog.askopenfilename()
    
    PrintSheetNames()
    ParametersExcel()                      
    ReadExcel(import_file_path,sheet,nrows,header_row,skip_footer)
    Preview(df)

    window.destroy()
    
    print('\n\033[1m\033[4m'+'Loading this file:'+'\033[0m')
    print(import_file_path+'\n')                       
                       
################################################################################## Tkinter All Excel ##################################################################################    
def LoadAllExcel():
    global import_file_path

    window = Tk()
    window.withdraw()
    import_file_path = filedialog.askopenfilename()
    
    print('\n\033[1m\033[4m'+'File Selected:'+'\033[0m\n'+import_file_path+'\n')
    PrintSheetNames()
    ParametersExcel()
    ReadAllExcel()
    Preview(df)
    
    window.destroy()                       
                       
################################################################################## Concat All Excel ##################################################################################    
def ReadAllExcel():
    FolderPath(import_file_path)                                                # 1. Get folder path
    FilenamePath(folder_path)                                                   # 2. Get folder path with additional substring
    GlobExcel(filename_path)                                                    # 3. Pattern matching
    print('\n\033[1m\033[4m'+'Filenames Loaded:'+'\033[0m ')
    ConcatExcel(sheet,nrows,header_row,skip_footer)  # 4. Concat Excel files
                       
# Step 3    
def GlobExcel(filename_path):
    global all_files
    all_files = glob.glob(filename_path + "*.xls*")                       
                       
# Step 4    
def ConcatExcel(sheet,nrows,header_row,skip_footer):
    global df

    li = []
    i=0
    for filename in all_files:
        ReadExcel(filename,sheet,nrows,header_row,skip_footer)   # Read Excel
        li.append(df)                                                    # Append df
        i+=1                                                             # Loop next
        print(str(i)+': '+filename.split('\\')[-1])
        
    df = pd.concat(li, axis=0, ignore_index=True)                        # Concat
    
    
##################################################################################
################################## Preview data ##################################
##################################################################################

def Preview(df,Num_Unique=None):
    print('\n\033[1m\033[4m'+'Preview'+'\033[0m')
    
    if isinstance(Num_Unique,int):
        pass
    else:
        Num_Unique = int(input("Enter Number of Unique Values to preview, default = 5, ") or '5')
    
    print('df'+str(df.shape)+' loaded')
    
    heads=[]
    tails=[]
    uniques=[]
    non_nans=[]
    dtypes = []
    
    columns = df.columns
    for column in columns:
        head = str(df[column].iloc[0])
        heads.append(head)
    
        tail = str(df[column].iloc[-1])
        tails.append(tail)
        
        unique = str(df[column].unique()[:Num_Unique])
        uniques.append(unique)
        
        non_nan = str(df[column].count())
        non_nans.append(non_nan)
        
        dtype = str(df[column].dtype)
        dtypes.append(dtype)
        
    preview = pd.DataFrame({
    'Column':columns,
    'Counts':non_nans,
    'First':heads,
    'Last':tails,
    str(Num_Unique)+' Unique Values':uniques,
    'DataType':dtypes,
    })
    
    display(preview)
        
def Select(dataframe):
    global df
    print('\n'+str(dataframe.columns)+'\n')
    df = dataframe[eval(input("Columns Required: "))]
        
        
##################################################################################
################################## Concat data ###################################
##################################################################################

def Concat(df1,df2):
    global df
    df = pd.concat([df1,df2],ignore_index=True)
    
def ConcatFields(df,deliminter,NewField,*Fields):
    df.loc[:,NewField]=''
    for Field in Fields:
        df.loc[:,NewField]=df.loc[:,NewField]+df.loc[:,Field].astype(str)+deliminter
    df.loc[:,NewField] = df.loc[:,NewField].str[:-1]

##################################################################################
################################## Date Operator #################################
##################################################################################
    
def DateOrdinal(df,NewField,DateField):
    df.loc[:,NewField] = df.loc[:,DateField].map(datetime.datetime.toordinal)