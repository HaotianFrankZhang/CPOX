import os

def extract_info_from_pdb(pdb_file_path, atom_threshold=5334):
    """
    Extracts the required information from a single .pdb file.

    Parameters:
    pdb_file_path (str): The path to the .pdb file.
    atom_threshold (int): The atom number threshold for determining the chain.

    Returns:
    list of tuples: Each tuple contains (residue_name, residue_number, chain).
    """
    extracted_info = []
    with open(pdb_file_path, 'r') as pdb_file:
        for line in pdb_file:
            if line.startswith("ATOM"):
                atom_number = int(line[6:11].strip())
                residue_name = line[17:20].strip()
                residue_number = line[22:26].strip()
                chain = 'A' if atom_number <= atom_threshold else 'B'
                extracted_info.append((residue_name, residue_number, chain))
    return extracted_info


def extract_pocket_scores(frame_txt_path):
    """
    Extracts score information from the frame_XXXX_out.txt file.

    Parameters:
    frame_txt_path (str): The path to the frame_XXXX_out.txt file.

    Returns:
    dict: A dictionary where the key is the pocket number and the value is another dictionary with the scores.
    """
    scores = {}
    current_pocket = None
    with open(frame_txt_path, 'r') as f:
        for line in f:
            if "Pocket" in line:
                current_pocket = line.split()[1]
                scores[current_pocket] = {}
            if any(score in line for score in ["Score", "Total SASA", "Polar SASA", "Volume", "local hydrophobic density", "Charge score"]):
                key, value = line.split(":")
                scores[current_pocket][key.strip()] = value.strip()
    return scores

def extract_Features(root_dir, output_file_path):
    """
     Processes each .pdb file and frame_XXXX_out.txt file in the directory structure starting from root_dir,
     extracts information, and writes it to the output file.

     Parameters:
     root_dir (str): The root directory containing all the frame folders.
     output_file_path (str): The path to the output .txt file.
     """
    with open(output_file_path, 'w') as output_file:
        for frame_dir in sorted(os.listdir(root_dir)):
            frame_path = os.path.join(root_dir, frame_dir)
            if os.path.isdir(frame_path):
                # Extract score information from the frame_XXXX_info.txt file
                new_filename = frame_dir.replace("_out", "_info")
                frame_info_path = os.path.join(frame_path, f"{new_filename}.txt")
                pocket_scores = extract_pocket_scores(frame_info_path)

                pocket_dir = os.path.join(frame_path, "pockets")
                if os.path.exists(pocket_dir) and os.path.isdir(pocket_dir):
                    for pocket_file in sorted(os.listdir(pocket_dir)):
                        if pocket_file.endswith("_atm.pdb"):
                            pocket_number = pocket_file.split('_')[0].lstrip("pocket")  # Extract the pocket number
                            score_info = "\t".join(
                                [f"{key}: {value}" for key, value in pocket_scores[pocket_number].items()])
                            line_to_write = f"{frame_dir} \t {pocket_file.split('_')[0]} \t {score_info}\n"
                            output_file.write(line_to_write)

def process_directory(root_dir, output_file_path, chain_thereshold):
    """
    Processes each .pdb file in the directory structure starting from root_dir,
    extracts information, and writes it to the output file.

    Parameters:
    root_dir (str): The root directory containing all the frame folders.
    output_file_path (str): The path to the output .txt file.
    """
    with open(output_file_path, 'w') as output_file:
        for frame_dir in sorted(os.listdir(root_dir)):
            if '.pdb' not in frame_dir:
                frame_path = os.path.join(root_dir, frame_dir)
                # print ('frame path is', frame_path)
                if os.path.isdir(frame_path):
                    pocket_dir = os.path.join(frame_path, "pockets")
                    # print (pocket_dir)
                    if os.path.exists(pocket_dir) and os.path.isdir(pocket_dir):
                        for pocket_file in sorted(os.listdir(pocket_dir)):
                            if pocket_file.endswith("_atm.pdb"):
                                pocket_info = extract_info_from_pdb(os.path.join(pocket_dir, pocket_file), chain_thereshold)
                                pocket_name = pocket_file.split('_')[0]  # Extract the pocket name
                                formatted_info = [f"{res_name}{res_num} {chain}" for res_name, res_num, chain in
                                                  pocket_info]
                                line_to_write = f"{frame_dir} \t {pocket_name} \t {'  '.join(formatted_info)}\n"
                                output_file.write(line_to_write)

def main():

    Mutation = ['WT', 'N272H', 'G188Q', 'L155W', 'V135A']
    # Mutation = ['N272H']
    Run = ['Run1', 'Run2', 'Run3', 'Run4', 'Run5']
    # Run = ['200ns']
    
    # threshoulds = [5324, 5334, 5330, 5318]
    threshoulds = [5327]
    
    i = 0
    for mutate in Mutation:
        print (mutate + ' evaluation starts')
        for run in Run:
            print (run + ' evaluation starts') 
            root_dir = "./" + mutate + "/" + run + "_frame"
            output_file_path = "./" + mutate + "/" + run + "_output.txt"
            process_directory(root_dir, output_file_path, threshoulds[i])
            extract_Features(root_dir, "./" + mutate + "/" + run + '_Features.txt')
        i += 1

if "__name__" == main():
    main()
