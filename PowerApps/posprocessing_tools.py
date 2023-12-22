import pandas as pd
import numpy as np

def extract_data_MZ(file_path, num_columns, start_string, finish_string):
    # Open the text file and read its content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the starting index of relevant data after the start_string
    start_index = None
    for i, line in enumerate(lines):
        if start_string in line:
            start_index = i + 1  # Move one line below the line containing the start_string
            break

    # Find the ending index of relevant data before the finish_string
    end_index = None
    for i, line in enumerate(lines[start_index:]):
        if finish_string in line:
            end_index = start_index + i  # Set the end_index
            break

    # Process the data between start_index and end_index
    if start_index is not None and end_index is not None:
        data = []
        for line in lines[start_index:end_index]:
            line = line.strip()
            if line:
                row_data = line.split()
                if len(row_data) == num_columns:
                    data.append(row_data)
    else:
        print("Start or end index not found.")

    # Convert the extracted data into a DataFrame
    if 'data' in locals() and data:
        df = pd.DataFrame(data)
        print("Data extracted as DataFrame:")
        return df
    else:
        print("No data extracted or error in data extraction.")
        return None


def extract_data_to_dataframe(file_path, column_names, string_finder):
    # Open the text file and read its content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the starting index of relevant data after the line containing "TERMINAL NO. 2, Term2"
    start_index = None
    for i, line in enumerate(lines):
        if string_finder in line:
            start_index = i  + 4 # Considering there are three empty lines after the target line
            break

    # Process the data after the identified start index
    if start_index is not None:
        data = []
        for line in lines[start_index:]:
            line = line.strip()
            if line:
                row_data = line.split()
                if len(row_data) == len(column_names):  # Assuming each line contains 9 elements
                    data.append(row_data)
    else:
        print("Start index not found.")

    # Convert the extracted data into a DataFrame
    if 'data' in locals() and data:

        df = pd.DataFrame(data, columns=column_names)
        print("Data extracted as DataFrame:")
        return df
    else:
        print("No data extracted or error in data extraction.")
        return None

def convert_columns_to_float(df, columns_to_convert):
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    return df


def filter_data_by_section(df, section):
    filtered_df = df[df['SECTION'] == section]
    
    if not filtered_df.empty:
        section_index = filtered_df.index[-1]  # Get the index of the last row with the specified section
        
        # Slice the DataFrame up to the last row of the specified section
        filtered_df = df.iloc[:section_index + 1]
        return filtered_df
    else:
        print(f"Section '{section}' not found.")
        return None
    
    
def remove_rows_with(df, str_garbage):
    # Remove rows containing "=" in any column
    df_no_equals = df[~df.apply(lambda row: row.astype(str).str.contains(str_garbage)).any(axis=1)]
    return df_no_equals


def convert_to_real_imag(df, columns_to_convert):
    df_ = df
    
    for column in columns_to_convert:
        aux = column.rsplit(' ', 1)[0]
        magnitude_column = column
        angle_column = aux + ' Angle(deg.)'
        

        real_column_name = aux + " Real"
        imag_column_name = aux + " Imaginary"

        # Convert polar coordinates to real and imaginary parts
        df_[real_column_name] = df_[magnitude_column] * np.cos(np.radians(df_[angle_column]))
        df_[imag_column_name] = df_[magnitude_column] * np.sin(np.radians(df_[angle_column]))
        
    df_ = df_.drop(columns_to_convert, axis=1)
    
    return df_


def remove_nan_rows(df):
    # Drop rows with NaN values
    df_without_nan = df.dropna(axis=0, how='any')
    return df_without_nan


def processing_MZ_data(df, new_columns):
    df_ = df
    df_ = remove_rows_with(df_, str_garbage='=')
    df_.columns = new_columns
    df_ = convert_columns_to_float(df_, new_columns)
    return df_
    