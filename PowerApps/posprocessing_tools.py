import pandas as pd
import numpy as np
from typing import List, Union

def extract_data_MZ(file_path: str, num_columns: int, start_string: str, finish_string: str) -> pd.DataFrame or None:
    """
    Extracts data from a text file located at 'file_path' based on provided criteria.

    Args:
    - file_path (str): The path to the text file.
    - num_columns (int): The expected number of columns in each row of data.
    - start_string (str): The string marking the beginning of the relevant data.
    - finish_string (str): The string marking the end of the relevant data.

    Returns:
    - pandas.DataFrame or None: A DataFrame containing the extracted data if successful, else None.
    """

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




def extract_data_to_dataframe(file_path: str, column_names: List[str], string_finder: str) -> Union[pd.DataFrame, None]:
    """
    Extracts data from a text file located at 'file_path' based on provided criteria and converts it into a DataFrame.

    Args:
    - file_path (str): The path to the text file.
    - column_names (list of str): Names of the columns for the DataFrame.
    - string_finder (str): The string used to identify the start of relevant data.

    Returns:
    - pandas.DataFrame or None: A DataFrame containing the extracted data if successful, else None.
    """

    # Open the text file and read its content
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Find the starting index of relevant data after the line containing "string_finder"
    start_index = None
    for i, line in enumerate(lines):
        if string_finder in line:
            start_index = i + 4  # Considering there are three empty lines after the target line
            break

    # Process the data after the identified start index
    if start_index is not None:
        data = []
        for line in lines[start_index:]:
            line = line.strip()
            if line:
                row_data = line.split()
                if len(row_data) == len(column_names):  # Assuming each line contains the same number of elements as column_names
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




def convert_columns_to_float(df: pd.DataFrame, columns_to_convert: Union[List[str], str]) -> pd.DataFrame:
    """
    Converts specified columns in a DataFrame to float data type.

    Args:
    - df (pandas.DataFrame): The DataFrame containing the columns to be converted.
    - columns_to_convert (list or str): The column name(s) or index of columns to convert to float.

    Returns:
    - pandas.DataFrame: The DataFrame with specified columns converted to float.
    """
    df[columns_to_convert] = df[columns_to_convert].apply(pd.to_numeric, errors='coerce')
    return df




def filter_data_by_section(df: pd.DataFrame, section: Union[str, int]) -> Union[pd.DataFrame, None]:
    """
    Filters a DataFrame by a specified 'SECTION' column value.

    Args:
    - df (pandas.DataFrame): The DataFrame to be filtered.
    - section (str or int): The value of the 'SECTION' column to filter by.

    Returns:
    - pandas.DataFrame or None: A filtered DataFrame containing rows up to the last occurrence of the specified section value if found, else None.
    """
    filtered_df = df[df['SECTION'] == section]
    
    if not filtered_df.empty:
        section_index = filtered_df.index[-1]  # Get the index of the last row with the specified section
        
        # Slice the DataFrame up to the last row of the specified section
        filtered_df = df.iloc[:section_index + 1]
        return filtered_df
    else:
        print(f"Section '{section}' not found.")
        return None

    

    
def remove_rows_with(df: pd.DataFrame, str_garbage: str) -> pd.DataFrame:
    """
    Removes rows containing specified string garbage in any column of the DataFrame.

    Args:
    - df (pandas.DataFrame): The DataFrame to be processed.
    - str_garbage (str): The string or substring to be searched for in the DataFrame.

    Returns:
    - pandas.DataFrame: DataFrame with rows containing the specified string garbage removed.
    """
    # Remove rows containing specified string garbage in any column
    df_no_equals = df[~df.apply(lambda row: row.astype(str).str.contains(str_garbage)).any(axis=1)]
    return df_no_equals




def convert_to_real_imag(df: pd.DataFrame, columns_to_convert: List[str]) -> pd.DataFrame:
    """
    Converts columns representing polar coordinates to their corresponding real and imaginary parts.

    Args:
    - df (pandas.DataFrame): The DataFrame containing polar coordinate columns.
    - columns_to_convert (list of str): List of column names representing polar coordinates.

    Returns:
    - pandas.DataFrame: DataFrame with polar coordinate columns converted to real and imaginary parts.
    """
    df_ = df.copy()
    
    for column in columns_to_convert:
        aux = column.rsplit(' ', 1)[0]
        magnitude_column = column
        angle_column = aux + ' Angle(deg.)'
        
        real_column_name = aux + " Real"
        imag_column_name = aux + " Imaginary"

        # Convert polar coordinates to real and imaginary parts
        df_[real_column_name] = df_[magnitude_column] * np.cos(np.radians(df_[angle_column]))
        df_[imag_column_name] = df_[magnitude_column] * np.sin(np.radians(df_[angle_column]))
        
    df_ = df_.drop(columns=columns_to_convert, axis=1)
    
    return df_




def remove_nan_rows(df: pd.DataFrame) -> pd.DataFrame:
    """
    Removes rows containing NaN values in the DataFrame.

    Args:
    - df (pandas.DataFrame): The DataFrame to be processed.

    Returns:
    - pandas.DataFrame: DataFrame with rows containing NaN values removed.
    """
    # Drop rows with NaN values
    df_without_nan = df.dropna(axis=0, how='any')
    return df_without_nan




def processing_MZ_data(df: pd.DataFrame, new_columns: List[str]) -> pd.DataFrame:
    """
    Performs data processing operations on a DataFrame.

    Args:
    - df (pandas.DataFrame): The DataFrame to be processed.
    - new_columns (list of str): List of new column names for the DataFrame.

    Returns:
    - pandas.DataFrame: Processed DataFrame after performing operations like removing specific rows, renaming columns, and converting columns to float type.
    """
    df_ = df.copy()
    df_ = remove_rows_with(df_, str_garbage='=')
    df_.columns = new_columns
    df_ = convert_columns_to_float(df_, new_columns)
    return df_
