import os

def load_reference_residues(file_path):
    """Loads residues from a reference .txt file."""
    with open(file_path, 'r') as file:
        # Create a set for residues, considering residue index and chain (e.g., "411B")
        return set(line.strip().replace("\t", "") for line in file)

def process_frame_pockets(file_path):
    """Process the main data file to organize residues by frame and pocket."""
    data = {}
    with open(file_path, 'r') as f:
        for line in f:
            parts = line.strip().split('\t')
            # print (parts)
            frame, pocket = parts[0].strip(), parts[1].strip()
            residues = {' '.join(res.split()[-2:]) for res in parts[2].strip().split('  ')}
            # print (residues)
            data[(frame, pocket)] = residues
    return data

def removeTyes(original_set):
    return {item[3:] for item in original_set}

def calculate_overlap(data, ref_pocket):
    """Calculate the overlap and total unique residues for each frame and pocket, ignoring residue types."""
    results = {}
    # Convert reference pocket to index-chain format for comparison
    ref_index_chain = {' '.join(res.split()[-2:]) for res in ref_pocket}
    for (frame, pocket), residues in data.items():
        # Convert current pocket's residues to index-chain format
        current_index_chain = {' '.join(res.split()[-2:]) for res in residues}
        # print('ref_pocket is', removeTyes(ref_pocket))
        # print ('currIndex', current_index_chain)
        # Calculate overlap based on index and chain
        overlap = len(removeTyes(current_index_chain).intersection(removeTyes(ref_index_chain)))
        total_unique = len(current_index_chain)  # Count of unique residues based on index and chain
        results[(frame, pocket)] = (overlap, total_unique)
    return results

def write_results(filename, overlaps_refA, overlaps_refB):
    """Write the results to a file."""
    with open(filename, 'w') as f:
        f.write("frame\tpocket\toverlaps_refA\toverlaps_refB\ttotal_number\n")
        for key in overlaps_refA:
            frame, pocket = key
            overlap_A, total_A = overlaps_refA[key]
            overlap_B, _ = overlaps_refB[key]
            f.write(f"{frame}\t{pocket}\t{overlap_A}\t{overlap_B}\t{total_A}\n")

def PickPocket(data):
    # Initialize a dictionary to track the highest proportion for each frame
    highest_proportion_per_frame = {}

    for key, (overlap, total) in data.items():
        frame, pocket = key
        # Calculate proportion
        proportion = overlap if total != 0 else 0
        # Check if this frame is already in our tracking dictionary
        if frame in highest_proportion_per_frame:
            # Compare with the currently stored proportion; update if higher
            if proportion > highest_proportion_per_frame[frame][2]:
                highest_proportion_per_frame[frame] = (pocket, (overlap, total), proportion)
        else:
            # If not in dictionary, add it
            highest_proportion_per_frame[frame] = (pocket, (overlap, total), proportion)

    # Convert the tracking dictionary to a list as specified
    result_list = [[frame, pocket, overlap_total] for frame, (pocket, overlap_total, _) in
                   highest_proportion_per_frame.items()]

    return result_list

def PickPocket_Ratio(data):
    # Initialize a dictionary to track the highest proportion for each frame
    highest_proportion_per_frame = {}

    for key, (overlap, total) in data.items():
        frame, pocket = key
        # Calculate proportion
        proportion = overlap / total if total != 0 else 0
        # Check if this frame is already in our tracking dictionary
        if frame in highest_proportion_per_frame:
            # Compare with the currently stored proportion; update if higher
            if proportion > highest_proportion_per_frame[frame][2]:
                highest_proportion_per_frame[frame] = (pocket, (overlap, total), proportion)
        else:
            # If not in dictionary, add it
            highest_proportion_per_frame[frame] = (pocket, (overlap, total), proportion)

    # Convert the tracking dictionary to a list as specified
    result_list = [[frame, pocket, overlap_total] for frame, (pocket, overlap_total, _) in
                   highest_proportion_per_frame.items()]

    return result_list



def write_picks(filename, overlaps_ref):
    """Write the results to a file."""
    with open(filename, 'w') as f:
        f.write("frame\tpocket\tOverlapResidue,TotalResidue\n")
        for item in overlaps_ref:
            frame, pocket = item[0], item[1]
            # print (item[2])
            info = ','.join([str(each) for each in item[2]])
            f.write(f"{frame}\t{pocket}\t{info}\n")


def main():
    # Load reference pockets
    # ref_pocket1 = load_reference_residues("Ref_Pocket1.txt") # {'residue chain'}
    # ref_pocket2 = load_reference_residues("Ref_Pocket2.txt")
    # print (ref_pocket2)

    ref_pocket1 = load_reference_residues("./code_fpocket/Ref_Pocket1.txt") # {'residue chain'}
    ref_pocket2 = load_reference_residues("./code_fpocket/Ref_Pocket2.txt")

    Mutation = ['WT', 'N272H', 'G188Q', 'L155W', 'V135A']
    Run = ['Run1', 'Run2', 'Run3', 'Run4', 'Run5']
    # Mutation = ['N272H']
    # Run = ['200ns']

    for mutate in Mutation:
        print (mutate + ' evaluation starts')
        if not os.path.exists('./' + mutate + '/fpocketResults'):
            os.makedirs('./' + mutate + '/fpocketResults')
        
        for run in Run:
            # Process the evaluation file to extract frames, pockets, and residues
            frame_pockets = process_frame_pockets('./' + mutate + '/' + run + "_output.txt")
            # print (frame_pockets[('frame_0500_out', 'pocket9')])

            # Calculate the overlap with reference pockets
            overlaps_refA = calculate_overlap(frame_pockets, ref_pocket1)
            overlaps_refB = calculate_overlap(frame_pockets, ref_pocket2)
            
            pick_A = PickPocket(overlaps_refA)
            pick_B = PickPocket(overlaps_refB)
            pick_A_ratio = PickPocket_Ratio(overlaps_refA)
            pick_B_ratio = PickPocket_Ratio(overlaps_refB)


            write_picks('./' + mutate + '/fpocketResults/Ratio_' + run + '_chain1.txt', pick_A_ratio)
            write_picks('./' + mutate + '/fpocketResults/Ratio_' + run + '_chain2.txt', pick_B_ratio)
            
            write_picks('./' + mutate + '/fpocketResults/' + run + '_chain1.txt', pick_A)
            write_picks('./' + mutate + '/fpocketResults/' + run + '_chain2.txt', pick_B)


if "__name__" == main():
    main()
