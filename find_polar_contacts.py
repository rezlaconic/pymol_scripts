# Define a function to find polar contacts
def find_polar_contacts():
    # Set the distance threshold for polar contacts (adjust as needed)
    distance_threshold = 4.0

    # Clear any existing selections and representations
    cmd.delete("polar*")
    cmd.delete("sticks_polar")

    # Select polar atoms (such as oxygen, nitrogen, and sulfur)
    cmd.select("polar_atoms", "element O+N+S")

    # Initialize a dictionary to store distances for each pair of atoms
    distances = {}
    rows = []

    # Get the list of all polar atoms
    polar_atoms_list = cmd.get_model("polar_atoms").atom
    print(f'There are {len(polar_atoms_list)} polar atoms ...')

    # Iterate through each pair of polar atoms and check their distances
    for i in range(len(polar_atoms_list)):
        for j in range(i + 1, len(polar_atoms_list)):
            polar_atom1 = polar_atoms_list[i]
            polar_atom2 = polar_atoms_list[j]

            # Calculate the distance between the atoms
            distance = cmd.distance(f"polar_{polar_atom1.id}_polar_{polar_atom2.id}", f"id {polar_atom1.id}", f"id {polar_atom2.id}")

            if distance <= distance_threshold:
                # Store the distance in the distances dictionary
                distances[(polar_atom1.id, polar_atom2.id)] = distance
                cmd.select(f"polar_{polar_atom1.id}_{polar_atom2.id}", f"id {polar_atom1.id} | id {polar_atom2.id}")
                cmd.show("sticks", f"polar_{polar_atom1.id}_{polar_atom2.id}")
                rows.append(f'Polar,{polar_atom1},{polar_atom2},{distance},polar_{polar_atom1.id}_{polar_atom2.id}')
            else:
                cmd.delete(f"polar_{polar_atom1.id}_polar_{polar_atom2.id}")

    # # Create a selection of interacting atoms based on distances and show sticks representation
    # for pair, distance in distances.items():
    #     if distance <= distance_threshold:
    #         cmd.select(f"polar_{pair[0]}_{pair[1]}", f"id {pair[0]} | id {pair[1]}")
    #         cmd.show("sticks", f"polar_{pair[0]}_{pair[1]}")


    #Dump ionic contacts into csv
    with open('polar_pairs.csv','w') as csv:
        csv.write('Bond Type,Polar Atom 1,Polar Atom 2,Distance,Sele')
        for row in rows: csv.write(row+'\n')

# Call the function to find polar contacts
find_polar_contacts()
