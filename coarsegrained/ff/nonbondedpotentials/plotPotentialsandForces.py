import os
import matplotlib.pyplot as plt

def read_txt_file(file_path):
    """
    Reads a .txt file and extracts columns for position, potential energy, and force.
    
    Args:
        file_path (str): Path to the .txt file.
    
    Returns:
        tuple: Two lists containing positions and potential energies.
    """
    positions = []
    potential_energies = []
    forces = []
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.split()
            
            if len(parts) == 3:
                try:
                    # x6 for the unit conversion from unitless to Angstrom then divide by 10 to go to nm
                    position = (float(parts[0]))
                    # x0.1 to go to kcal/mol
                    potential_energy = (float(parts[1]))
                    positions.append(position)
                    potential_energies.append(potential_energy)
                    force = (float(parts[2]))
                    forces.append(force)
                except ValueError:
                    print(f"Skipping line with non-numeric data: {line.strip()}")
            else:
                print(f"Skipping line with incorrect number of columns: {line.strip()}")
    return positions, potential_energies, forces 

def plot_data(scaled_positions, scaled_potential_energies, filename, output_dir_plot):
    """
    Plots the position vs potential energy and saves it as a .png file.
    
    Args:
        positions (list): List of positions.
        potential_energies (list): List of potential energies.
        filename (str): Name of the file being processed, used for the plot title and output filename.
        output_dir (str): Directory where the plot will be saved.
    """
    plt.figure(dpi=350, figsize=(6, 3))
    plt.grid(color='grey', linestyle='--', linewidth=1, alpha=0.4)
    plt.plot(scaled_positions, scaled_potential_energies, linestyle='-', color='b')
    plt.xlabel('r (nm)',fontweight='bold')
    plt.ylabel('V(r) (kJ/mol-nm)',fontweight='bold')
    
    abr_filename = (filename.split('_')[1]).split('.')[0]

    plt.title(f'{abr_filename}')
    plt.xlim([0.0,1.2])
    plt.ylim([-2.5,1])
    
    plt.grid(True)
    plt.tight_layout()
    
    output_file = os.path.join(output_dir_plot, f"{abr_filename}.png")
    plt.savefig(output_file)
    plt.close()
    print(f"Saved plot to {abr_filename}")

def save_scaled_data(positions, potential_energies, forces, filename, output_dir_scale):
    """
    Saves scaled position and potential energy data to a new .txt file.
    
    Args:
        positions (list): List of positions where initially dimensionless so x6 to get to Angstroms, then divide by 10 to get to nm.
        potential_energies (list): List of potential energies where initially dimensionless * 0.1 to get into kcal/mol then x4.18400 to get to kJ/mol.
        forces (list): List of forces where initially dimensionless * (0.1 to get into kcal/mol then x4.18400 to get to kJ/mol) then divide by (6/10) to get into kJ/(mol-nm).
        filename (str): Name of the file being processed, used for the new file name.
        output_dir (str): Directory where the new .txt file will be saved.
    """
    scaled_positions = [pos * 6 * 0.1 for pos in positions]
    scaled_potential_energies = [pe * 0.1 * 4.18400 for pe in potential_energies]
    scaled_forces = [fe * (0.1 * 4.18400)/(6/10) for fe in forces]

    output_file_path = os.path.join(output_dir_scale, f"scaled_{filename}")
    with open(output_file_path, 'w') as file:
        for pos, pe, fe in zip(scaled_positions, scaled_potential_energies,scaled_forces):
            file.write(f"{pos:.18e} {pe:.18e} {fe:.18e}\n")
    return scaled_positions,scaled_potential_energies,scaled_forces

def process_files_in_directory(directory, scaled_directory, output_dir_plot,output_dir_scale):
    """
    Processes all .txt files in the specified directory and generates plots.
    
    Args:
        directory (str): Path to the directory containing .txt files.
        output_dir (str): Path to the directory where plots will be saved.
    """
    if not os.path.exists(output_dir_plot):
        os.makedirs(output_dir_plot)
    elif not os.path.exists(output_dir_scale):
        os.makedirs(output_dir_scale)
    
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            print(f"Processing file: {file_path}")
            positions, potential_energies,forces = read_txt_file(file_path)
            if positions and potential_energies:  # Only plot if data is available
                save_scaled_data(positions, potential_energies,forces, filename, output_dir_scale)
                 

    for filename in os.listdir(scaled_directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(scaled_directory, filename)
            print(f"Processing file: {file_path}")
            positions, potential_energies,forces = read_txt_file(file_path)
            if positions and potential_energies:  # Only plot if data is available
                plot_data(positions, potential_energies, filename, output_dir_plot)
        

if __name__ == "__main__":
    input_directory = 'dimensionlesspotentials' 
    output_directory_plots = 'scaledplots'  
    output_directory_scaled = 'scaledpotentials'
    input_directory_scaled = output_directory_scaled

    process_files_in_directory(input_directory, input_directory_scaled, output_directory_plots,output_directory_scaled)
