import pandas as pd
import numpy as np



def calculate_length(df):
    initial_point = df.iloc[0]
    final_point = df.iloc[-1]

    # Calcula o comprimento usando a fórmula da distância euclidiana
    length = np.linalg.norm(final_point - initial_point)

    return length


def find_row_with_text(file_path, text):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            for index, line in enumerate(lines):
                if text.lower() in line.lower():
                    return index + 1, line  # Adding 1 to index for human-readable line numbering
            return None, None  # Return None if the text is not found
    except FileNotFoundError:
        return None, None  # Return None if the file is not found
    
    
def modify_file_and_save(input_file, output_file, search_text, replacement_text):
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