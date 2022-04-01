""" binf.py
These are methods, functions and classes that I've used for different
Bioinformatics Applications including custom implementation of certain
algorithms.
"""

# Imports
import Bio.Align as _Align
import tempfile as _temp
import pandas as _pd
import numpy as _np
import os as _os
import GEOparse
import pickle
import rich
from typing import Union as _Union
from datetime import date


# Definitions
#TODO: Write function to generate phylogenetic tree from distance matrix (use turtle)
#TODO: use turtle to draw tree as you condense the distance matrix (use arithmetic mean)

class BWT:
    """
    A simple implementation of the Burrows-Wheeler Transform
    """
    def transform(sequence: str) -> str:
        sequence += '$'
        table = [sequence[index:] + sequence[:index] for index, _ in enumerate(sequence)]
        table.sort()
	    
        return ''.join([ rotation[-1] for rotation in table ])

    def inverse(sequence: str) -> str:
        table = [col for col in sequence]
        for _ in range(len(sequence) - 1):
            table.sort()
            table = [sequence[i] + table[i] for i in range(len(sequence))]

        return table[[row[-1] for row in table].index('$')] 


def swalign(a: str, b: str, gap: int=-5, submat: _Align.substitution_matrices.Array=None,
            scoreonly: bool=False, identonly: bool=False) -> _Union[int, float, dict]:
    """
    This is a custom implementation of the Smith-Waterman Local Sequence Alignment Algorithm.
    It is based on a code written by Dr. Ahmet Sacan <ahmetmsacan@gmail.com>
    It uses the Dynamic Programming algorithm to obtain an optimal sequence alignment.
    This function only supports linear gap penalties.
    @param a: str, b: str
        Sequences to align
    @param gap: int
        Gap score
    @param submat: Align.substitution_matrices.Array
        Scoring matrix (BLOSUM62 is the default)
    @param scoreonly: bool
        Return alignment score only
    @param identonly: bool
        Return percent identity only
    @return
        Alignment score, percent identiy, and or alignment
    """

    # Default substitution matrix
    if submat is None:
        submat = _Align.substitution_matrices.load('BLOSUM62')
    # Define sequence lengths
    A = len(a)
    B = len(b) 
    # Initialize Dynamic Programming (score) table
    T = _np.zeros( (A+1, B+1) ).tolist()

    if scoreonly:
        for i in range(A):
            # Define variables that reference positions in the score table
            # This is a speed optimization - directly reference position instead of searching
            # for it each time
            submat_ai = submat[a[i]]
            Ti = T[i]
            Ti_plus1 = T[i+1]
            for j in range(B):
                # reset, diag, horz, vert.
                Ti_plus1[j+1] = max( 0, Ti[j]+submat_ai[b[j]], Ti_plus1[j]+gap, Ti[j+1]+gap )
        return _np.max(T, axis=None)

    elif identonly:
        # Initialize counts
        MC = _np.zeros((A+1, B+1), dtype=int).tolist() # match counts
        AL = _np.zeros((A+1, B+1), dtype=int).tolist() # alignment lengths

        for i in range(A):
            submat_ai = submat[a[i]]
            Ti = T[i];	Ti_plus1 = T[i+1];
            MCi = MC[i];	MCi_plus1 = MC[i+1];
            ALi = AL[i];	ALi_plus1 = AL[i+1];

            for j in range(B):
                # reset, diag, horz, vert.
                options = ( 0, Ti[j]+submat_ai[b[j]], Ti_plus1[j]+gap, Ti[j+1]+gap )
                bestmove = _np.argmax(options)
                Ti_plus1[j+1] = options[bestmove]

                if bestmove == 1: # Diagonal
                    MCi_plus1[j+1] = MCi[j] + (a[i] == b[j])
                    ALi_plus1[j+1] = ALi[j] + 1
                elif bestmove == 2: # Horizontal
                    MCi_plus1[j+1] = MCi_plus1[j]
                    ALi_plus1[j+1] = ALi_plus1[j] + 1
                elif bestmove == 3: # Vertical
                    MCi_plus1[j+1] = MCi[j+1]
                    ALi_plus1[j+1] = ALi[j+1] + 1

    else:
        # Store the best direction (we only keep one when there are multiple good options.)
        P = _np.zeros((A+1, B+1), dtype=int).tolist()
        for i in range(A):
            submat_ai = submat[a[i]]
            Ti = T[i]
            Ti_plus1 = T[i+1]
            Pi_plus1 = P[i+1]

            for j in range(B):
                # reset, diag, horz, vert.
                options = ( 0, Ti[j]+submat_ai[b[j]], Ti_plus1[j]+gap, Ti[j+1]+gap )
                bestmove = _np.argmax(options)
                Ti_plus1[j+1] = options[bestmove]
                Pi_plus1[j+1] = bestmove

    # Determine score positions
    scorepos = _np.unravel_index(_np.argmax(T, axis=None), (A+1, B+1))
    r,c = scorepos # r=scorepos[0]; c=scorepos[1]
    if identonly:
        # Compute and return percent identity
        return MC[r][c] / AL[r][c] * 100

    # Store alginment score
    score = T[r][c]

    # Reconstruct Alignment (#? Bactracking)
    align_a = []; align_b = []
    while T[r][c] != 0 and P[r][c] != 0:
        move = P[r][c]
        # Define alignment characters
        if move == 1:
            r = r-1
            c = c-1
            achar = a[r]
            bchar = b[c]
        elif move == 2:
            c = c-1
            achar = '-'
            bchar = b[c]
        elif move == 3:
            r = r-1
            achar = a[r]
            bchar = '-'

        align_a.append(achar); align_b.append(bchar);

    # Reverse alignments and convert to strings
    align_a.reverse(); align_b.reverse()
    align = [''.join(align_a), ''.join(align_b)]

    # Compute percent identity
    L = len(align[0])
    ident = _np.count_nonzero([align[0][i] == align[1][i] for i in range(L)]) / L * 100

    return {'score': score, 'align': align, 'ident': ident}


def nwalign(a: str, b: str, match: int=1, mismatch: int=-1, gap: int=-2,
            score_only: bool=False, ident_only: bool=False, penalize_end_gaps=False,
            submat: _Align.substitution_matrices.Array=None, alphabet: str='nt') -> _Union[int, float, dict]:
    """
    Custom implementation of the Needleman-Wunsch algorithm
    """

    # Default substitution matrix
    if submat is None:
        if alphabet == 'nt': # Create nucleotide scoring matrix
            # TODO: Modify this to handle gap characters
            submat = _pd.DataFrame(
                mismatch * _np.ones((4, 4)) + (match - mismatch) * _np.identity(4),
                index=["A", "C", "T", "G"], columns=["A", "C", "T", "G"]
            )
        elif alphabet == 'aa':
            submat = _Align.substitution_matrices.load('BLOSUM62')

    # Define sequence lengths
    A = len(a)
    B = len(b) 
    # Initialzie Dynamic Programming table
    T = _np.zeros( (A+1, B+1) ).tolist()

    if penalize_end_gaps:
        # Global alignment
        pass
    else: 
        # Free-end gaps (Semiglobal Alignment)
        #   Zeros in first row and first column
        #   Max value in last row or last column is end of alignment
        if score_only:
            for i in range(A):
                submat_ai = submat[a[i]]
                Ti = T[i]
                Ti_plus1 = T[i+1]
                for j in range(B):
                    # diag, horz, vert.
                    Ti_plus1[j+1] = max( Ti[j]+submat_ai[b[j]], Ti_plus1[j]+gap, Ti[j+1]+gap )
            return _np.hstack([_np.array(T)[A, :], _np.array(T)[:, B]]).max(axis=None)

def tempdir(dirname: str):
    """Create path to a temporary directory"""
    name = _os.path.join(_temp.gettempdir().replace("\\","/"), dirname)
    if not _os.path.isdir(name): _os.mkdir(name)
    return name

def geodlparse(acc: str):

    # Path to temporary directory
    geodir = tempdir('GEO')

    # Download files
    try:
        # Specify file names
        names = [f'{acc}.txt', f'{acc}_family.soft.gz']
        geofile = _os.path.join(geodir, names[0 if acc[:3] == 'GPL' else 1])
        cachefile = _os.path.join(geodir, f"{date.today().strftime('%Y%m%d')}_{acc}.pkl")

        if _os.path.isfile(cachefile):
            # Load data if it has already been cached
            try:
                print('Loading cached data...')
                with open(cachefile, 'rb') as cache:
                    geodata =  pickle.load(cache)
                return geodata
            except Exception as e:
                print(f"ERROR: Loading cached file failed.\n{e}")
        else:
            if _os.path.isfile(geofile):
                # If data has already been downloaded, parse it and cache results
                print('Already downloaded. Parsing...')
                geodata = GEOparse.get_GEO(filepath=geofile, silent=True)
            else:
                # Download and parse data
                print('Downloading and parsing...')
                geodata = GEOparse.get_GEO(acc, destdir=geodir, silent=True)
            # Cache data
            with open(cachefile, 'wb') as cache:
                pickle.dump(geodata, file=cache)
            return geodata
    except Exception as e:
        print(f"ERROR: Enter a valid GEO Accension\n{e}")