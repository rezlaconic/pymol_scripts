# Define a function to find ionic interactions
def find_ionic_interactions():
    # Set the distance threshold for ionic interactions (adjust as needed)
    distance_threshold = 15.0

    # Clear any existing selections and representations
    cmd.delete("ions*")
    cmd.delete("sticks_ions")
    cmd.delete("dist*")  # Delete previous distance measurements

    # Select cationic and anionic atoms
    cmd.select("cations", "name NZ")
    cmd.select("anions", "name OD*")

    # Initialize a dictionary to store distances for each pair of atoms
    distances = {}
    rows = []

    # Iterate through each cation and check for nearby anions
    for cation in cmd.get_model("cations").atom:
        cation_residue = cmd.get_model(f'id {cation.id}').atom[0].resn
        cation_name = cation_residue + str(cation.id)

        for anion in cmd.get_model("anions").atom:
            anion_residue = cmd.get_model(f'id {anion.id}').atom[0].resn
            anion_name = anion_residue + str(anion.id)

            # Calculate the distance between the atoms
            #distance = cmd.distance(f"ions_cation_{cation.id}_anion_{anion.id}", f"id {cation.id}", f"id {anion.id}",distance_threshold)
            distance = cmd.distance(f"ion_dist_{cation_name}_{anion_name}", f"id {cation.id}", f"id {anion.id}") #no distance thres

            # Print the details of the current pair and its distance
            #print(f"Cation: {cation.resn}{cation.resi} (atom {cation.id}), Anion: {anion.resn}{anion.resi} (atom {anion.id}), Distance: {distance:.2f} Å")

            if distance <= distance_threshold:
                print(f"Found pair within distance: Cation {cation.resn}{cation.resi} (atom {cation.id}), Anion: {anion.resn}{anion.resi} (atom {anion.id}), Distance: {distance:.2f} Å")
                
                # Store the distance in the distances dictionary
                distances[(cation.id, anion.id)] = distance
                cmd.select(f"ionic_pair_{cation_name}_{anion_name}", f"id {cation.id} | id {anion.id}")
                cmd.show("sticks", f"ionic_pair_{cation_name}_{anion_name}")
                rows.append(f'Ionic,{cation_residue},{cation.id},{anion_residue},{anion.id},{distance},ionic_pair_cation_{cation_name}_anion_{anion_name}')

            
            else: #delete distance calcs greater than thresh
                cmd.delete(f"ion_dist_{cation_name}_{anion_name}")
            

            rows.append(f'Ionic,{cation_residue},{cation.id},{anion_residue},{anion.id},{distance},ionic_pair_cation_{cation_name}_anion_{anion_name}')

    #Dump ionic contacts into csv
    with open('ionic_pairs.csv','w') as csv:
        csv.write('Bond Type,Cation Residue,Cation ID,Anion Residue,Anion ID,Distance,Sele')
        for row in rows: csv.write(row+'\n')


# Call the function to find ionic interactions
find_ionic_interactions()
