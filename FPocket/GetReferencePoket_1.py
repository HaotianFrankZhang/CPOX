def extract_and_annotate_pdb(pdb_file_path, output_file_path):
    """
    Extracts ATOM, residue name, and residue number from a .pdb file,
    annotates them with chains "A" or "B", and writes the results to a .txt file.

    Parameters:
    pdb_file_path (str): The path to the input .pdb file.
    output_file_path (str): The path to the output .txt file.
    """
    WrittenLine = []
    with open(pdb_file_path, 'r') as pdb_file:
        with open(output_file_path, 'w') as output_file:
            for line in pdb_file:
                if line.startswith("ATOM"):
                    # Extract the atom number, residue name, and residue number
                    atom_number = int(line[6:11].strip())
                    residue_name = line[17:20].strip()
                    residue_number = line[22:26].strip()

                    # Determine the chain based on the atom number
                    chain = 'A' if atom_number <= 2702 else 'B'

                    # Format and write to the output file
                    output_line = f"{residue_name}{residue_number} \t {chain}\n"
                    if output_line not in WrittenLine:
                        output_file.write(output_line)
                        WrittenLine.append(output_line)

def main():
    # Example usage
    pdb_file_path = "./CPOX_out/pockets/pocket1_atm.pdb"
    output_file_path = "Ref_Pocket1.txt"
    extract_and_annotate_pdb(pdb_file_path, output_file_path)

    pdb_file_path = "./CPOX_out/pockets/pocket2_atm.pdb"
    output_file_path = "Ref_Pocket2.txt"
    extract_and_annotate_pdb(pdb_file_path, output_file_path)

if "__name__" == main():
    main()