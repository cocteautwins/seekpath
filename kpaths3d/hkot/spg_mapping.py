def get_crystal_family(number):
    """
    Given a spacegroup number, returns a string to identify its
    crystal family (triclinic, monoclinic, ...).

    :param number: the spacegroup number, from 1 to 230
    """
    if not isinstance(number, (int,long)):
        raise TypeError("number should be integer")
    if number < 1:
        raise ValueError("number should be >= 1")
    if number <= 2:
        return "a" # triclinic
    elif number <= 15:
        return "m" # monoclinic
    elif number <= 74:
        return "o" # orthorhombic
    elif number <= 142:
        return "t" # tetragonal
    elif number <= 194:
        return "h" # trigonal + hexagonal
    elif number <= 230:
        return "c" # cubic
    else:
        raise ValueError("number should be <= 230")

def pointgroup_has_inversion(number):
    """
    Return True if the pointgroup with given number has inversion, 
    False otherwise.

    :param number: The integer number of the pointgroup, from 1 to 32.
    """
    if number in [2,5,8,11,15,17,20,23,27,29,32]:
        return True
    elif number in [1,3,4,6,7,9,10,12,13,14,16,18,19,21,22,24,25,26,28,30,31]:
        return False
    else:
        raise ValueError("number should be between 1 and 32")


def pgnum_from_pgint(pgint):
    """
    Return the number of the pointgroup (from 1 to 32) from the
    international pointgroup name.
    """
    table = {u'C1': 1,
             u'C2': 3,
             u'C2h': 5,
             u'C2v': 7,
             u'C3': 16,
             u'C3h': 22,
             u'C3i': 17,
             u'C3v': 19,
             u'C4': 9,
             u'C4h': 11,
             u'C4v': 13,
             u'C6': 21,
             u'C6h': 23,
             u'C6v': 25,
             u'Ci': 2,
             u'Cs': 4,
             u'D2': 6,
             u'D2d': 14,
             u'D2h': 8,
             u'D3': 18,
             u'D3d': 20,
             u'D3h': 26,
             u'D4': 12,
             u'D4h': 15,
             u'D6': 24,
             u'D6h': 27,
             u'O': 30,
             u'Oh': 32,
             u'S4': 10,
             u'T': 28,
             u'Td': 31,
             u'Th': 29}

    return table[pgint]

def get_spgroup_data():
    """
    Return a dictionary that has the spacegroup number as key, and a tuple 
    as value, with (crystal family letter, centering, has_inversion).

    It loads if from a table in the source code for efficiency.
    """
    from .spg_db import spgroup_data
    return spgroup_data

def get_spgroup_data_realtime():
    """
    Return a dictionary that has the spacegroup number as key, and a tuple 
    as value, with (crystal family letter, centering, has_inversion),
    got in real time using spglib methods.
    """
    import json
    import spglib

    info = {}
    for hall_n in range(1,531):
        data = spglib.get_spacegroup_type(hall_n)
        number = data['number']
        int_short = data['international_short']
        pg_int = data['pointgroup_international']
        
        if number not in info:
            info[int(number)] = (get_crystal_family(number), # get cyrstal family
                            int_short[0], #centering from the first letter of the first spacegroup that I encounter
                            pointgroup_has_inversion(pgnum_from_pgint(pg_int)), # pointgroup has inversion
                            )
    return info

def get_P_matrix(bravais_lattice):
    """
    Return a tuple of length 2 with the P matrix and its inverse::

      (P, invP)

    with invP = P^-1.

    These P matrices are obtained from Table 3 of the HKOT 
    paper.

    The P matrix is a 3x3 matrix is the matrix that converts
    the lattice vectors from crystallographic conventional
    (a,b,c) to crystallographic primitive (a_P, b_P, c_P)
    as follows::

      (a_P, b_P, c_P) = (a,b,c) P

    The change of (real space) coordinate triples follows instead:

       (x_P, y_P, z_P)^T = (P^-1) (x,y,z)^T

    .. note:: the invP = P^-1 matrix is always integer (with values
        only -1,0,1) while P is rational (non-integer values can be
        +/- 1/2 and +/- 1/3).
    """
    import numpy as np

    if bravais_lattice in [
        "cP", "tP", "hP", "oP", "mP"]:
        P = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1]])
        invP = np.array([
            [1,0,0],
            [0,1,0],
            [0,0,1]])
    elif bravais_lattice in [
        "cF", "oF"]:
        P = 1./2. * np.array([
            [0,1,1],
            [1,0,1],
            [1,1,0]])
        invP = np.array([
            [-1,1,1],
            [1,-1,1],
            [1,1,-1]])
    elif bravais_lattice in [
        "cI", "tI", "oI"]:
        P = 1./2. * np.array([
            [-1,1,1],
            [1,-1,1],
            [1,1,-1]])
        invP = np.array([
            [0,1,1],
            [1,0,1],
            [1,1,0]])
    elif bravais_lattice == "hR":
        P = 1./3. * np.array([
            [2,-1,-1],
            [1,1,-2],
            [1,1,1]])
        invP = np.array([
            [1,0,1],
            [-1,1,1],
            [0,-1,1]])
    elif bravais_lattice == "oC":
        P = 1./2. * np.array([
            [1, 1,0],
            [-1,1,0],
            [0, 0,2]])
        invP = np.array([
            [1,-1,0],
            [1, 1,0],
            [0, 0,1]])
    elif bravais_lattice == "oA":
        P = 1./2. * np.array([
            [ 0,0,2],
            [ 1,1,0],
            [-1,1,0]])
        invP = np.array([
            [0,1,-1],
            [0,1, 1],
            [1,0, 0]])
    elif bravais_lattice == "mC":
        P = 1./2. * np.array([
            [1,-1,0],
            [1, 1,0],
            [0, 0,2]])
        invP = np.array([
            [ 1,1,0],
            [-1,1,0],
            [ 0,0,1]])
    else:        
        raise ValueError("Invalid bravais_lattice {}".format(bravais_lattice))

    return P, invP

def get_primitive(structure, bravais_lattice):
    """
    Return the primitive cell from a standard crystallographic cell.

    :param structure: should be a tuple of the form
      (lattice, positions, types) and it MUST be already a standard
      crystallographic cell (e.g. as returned by spglib).

    :param bravais_lattice: a string with the information of the
      Bravais lattice of the input structure.

    :return: two tuples: the primitive structure, also in the format
      (lattice, positions, types), and the (P, invP) matrices as returned
      by get_P_matrix.
    """
    import numpy as np
    from collections import Counter

    print "WARNING! The function get_primitive has not been debugged yet"
    print "cell looks reasonable - but to double check; atoms to check!"

    threshold = 1.e-6 # Threshold for creation of primitive cell

    lattice, positions, types = structure
    P, invP = get_P_matrix(bravais_lattice)

    volume_ratio = int(np.linalg.det(invP))

    # (a_P, b_P, c_P) = (a,b,c) P
    # a is the first ROW of lattice => I have to transpose lattice
    prim_lattice = np.dot(np.array(lattice.T), P).T
    # (x_P, y_P, z_P)^T = (P^-1) (x,y,z)^T
    prim_positions = np.dot(invP, np.array(positions).T).T

    ## Now I need to remove duplicates
    ## I get if the x coord is the same, modulo one
    # I compare all with all 
    # (I will get a NxN matrix, where N = number of atoms)
    # I shift by 1/2, do %1 and then shift back so that I get values between
    # -0.5 and 0.5 rather than between 0 and 1, which would be problematic
    # to find values close to zero
    x_match = np.abs(
        ((prim_positions[:,0] - prim_positions[:,0][:,None] + 0.5) 
            % 1. ) - 0.5) < threshold
    y_match = np.abs(
        ((prim_positions[:,1] - prim_positions[:,1][:,None] + 0.5) 
            % 1. ) - 0.5) < threshold
    z_match = np.abs(
        ((prim_positions[:,2] - prim_positions[:,2][:,None] + 0.5) 
            % 1. ) - 0.5) < threshold
    # To be the same, they should all match
    all_match = np.logical_and(x_match, np.logical_and(y_match, z_match))

    # list of ids, each row identifies a group of equivalent atoms
    # I convert to tuple so they can become keys of a dict for counting
    group_of_equivalent_atoms = [tuple(np.arange(all_match.shape[0])[row]) for row in all_match]
    group_count = Counter(group_of_equivalent_atoms)
    wrong_count = [group for group,cnt in group_count.iteritems() 
        if cnt != volume_ratio]
    if wrong_count:
        raise ValueError("Problem creating primitive cell, I found the "
            "following group of atoms with len != {}: {}".format(
                volume_ratio, ", ".join(str(_) for _ in wrong_count.keys())))
    # These are the groups of equivalent atoms; values are the positions in
    # the list from 0 to N-1
    groups = sorted(group_count.keys())
    # I check that the type is always the same
    unique_types = [set(np.array(types)[np.array(group)]) for group in groups]
    problematic_groups_idx = list(group_idx for group_idx, type_set 
        in enumerate(unique_types) if len(type_set) != 1)
    if problematic_groups_idx:
        raise ValueError("The following ids of atoms go on top of each other, "
            "but they are of different type! {}".format(", ".join(
                [str(group) for group_idx, group in enumerate(groups)
                if group_idx in problematic_groups_idx])))
    # All good, just return the first, wrapped to [0,1]
    chosen_idx = np.array([group[0] for group in groups])

    prim_positions = prim_positions[chosen_idx]
    prim_types = types[chosen_idx]

    prim_structure = (prim_lattice, prim_positions, prim_types)

    return (prim_structure, (P, invP))





