import pandas as pd
import numpy as np
from typing import Optional, Tuple

def calculate_length(df: pd.DataFrame) -> float:
    """
    Calculates the length of a path represented by a DataFrame.

    Args:
    - df (pandas.DataFrame): DataFrame containing coordinates of a path.

    Returns:
    - float: Length of the path calculated using the Euclidean distance formula.
    """
    initial_point = df.iloc[0]
    final_point = df.iloc[-1]

    # Calculate length using the Euclidean distance formula
    length = np.linalg.norm(final_point - initial_point)

    return length




def find_row_with_text(file_path: str, text: str) -> Optional[Tuple[int, str]]:
    """
    Finds the line number and content in a file containing the specified text.

    Args:
    - file_path (str): Path to the file to search.
    - text (str): Text to search for within the file.

    Returns:
    - tuple or None: Tuple containing line number and line content if text is found, else returns None.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if text.lower() in line.lower():
                    return index + 1, line  # Adding 1 to index for human-readable line numbering
            return None, None  # Return None if the text is not found
    except FileNotFoundError:
        return None, None  # Return None if the file is not found




def modify_file_and_save(input_file: str, output_file: str, search_text: str, replacement_text: str) -> None:
    """
    Modifies a file by replacing specified text and saves the modified content to a new file.

    Args:
    - input_file (str): Path to the input file.
    - output_file (str): Path to the output file to be created with modifications.
    - search_text (str): Text to search for in the input file.
    - replacement_text (str): Text to replace the found search_text.

    Returns:
    - None
    """
    try:
        with open(input_file, 'r') as file:
            lines = file.readlines()

        # Find the line number with the specified text
        line_number, _ = find_row_with_text(input_file, search_text)

        if line_number is not None:
            # Replace content in the found line
            lines[line_number - 1] = lines[line_number - 1].replace(search_text, replacement_text)

            # Truncate the content from the found line onwards
            lines = lines[:line_number]

            # Write the modified content to the new file
            with open(output_file, 'w') as new_file:
                new_file.writelines(lines)
                print(f"File '{output_file}' created with the modification.")
        else:
            print(f"'{search_text}' not found in the file.")

    except FileNotFoundError:
        print("File not found.")