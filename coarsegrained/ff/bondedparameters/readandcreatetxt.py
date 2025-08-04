import pandas as pd
import pickle


def read_pickle_and_write_to_txt(pickle_file_path, txt_file_path_angle,txt_file_path_bond):
    # Open the pickle file in read-binary mode
    with open(pickle_file_path, 'rb') as pickle_file:
        # Load the contents of the pickle file
        data = pd.read_pickle(pickle_file)
        print(data.keys())
    for val in data.keys():
        if val =='angles':
            print(data[val])
            # Open the text file in write mode
            with open(txt_file_path_angle, 'w') as txt_file:
                txt_file.write('# angle triplet\t\t\tequilibrium angle (degrees)\tk-constant ([kcal/(mol-rad^2)])\n')
                # Iterate over each key-value pair in the data
                for key, value in data[val].items():
                    # Format the line as 'key value1 value2'
                    line = f"{key}\t\t\t{value[0]}\t\t\t\t\t{value[1]}\n"
                    # Write the formatted line to the text file
                    txt_file.write(line)
        if val =='bonds':
            print(data[val])
            # Open the text file in write mode
            with open(txt_file_path_bond, 'w') as txt_file:
                txt_file.write('# bond pair\t\t\tequilibrium distance (Å)\tk-constant ([kcal/(mol-Å^2)])\n')
                # Iterate over each key-value pair in the data
                for key, value in data[val].items():
                    # Format the line as 'key value1 value2'
                    line = f"{key}\t\t\t{value[0]}\t\t\t\t\t{value[1]}\n"
                    # Write the formatted line to the text file
                    txt_file.write(line)

pickle_file_path = 'cg-bond-coeffs_stiff-tails-v3.p'  
angles_txt_file_path = 'angles.txt'     
bonds_txt_file_path = 'bonds.txt'      
read_pickle_and_write_to_txt(pickle_file_path, angles_txt_file_path,bonds_txt_file_path)