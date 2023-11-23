from enum import IntEnum
import numpy as np

# Assigning the constants for the scores
class Score(IntEnum):
    MATCH = 1
    MISMATCH = -1
    GAP = -1

# Assigning the constant values for the traceback
class Trace(IntEnum):
    STOP = 0
    LEFT = 1
    UP = 2
    DIAGONAL = 3

# Reading the fasta file and keeping the formatted sequence's name and sequence
def fasta_reader(sequence_file):
    lines = open(sequence_file).readlines()
    sequence_name_row = lines[0][1:]
    sequence = lines[1]
    return sequence_name_row.replace(" ", "").strip(), sequence.strip()

# Implementing the Smith Waterman local alignment
def smith_waterman(seq1, seq2):
    # Generating the empty matrices for storing scores and tracing
    row = len(seq1) + 1
    col = len(seq2) + 1
    matrix = np.zeros(shape=(row, col), dtype='int')
    tracing_matrix = np.zeros(shape=(row, col), dtype='int')

    # Initialising the variables to find the highest scoring cell
    max_score = -1
    max_index = (-1, -1)

    # Calculating the scores for all cells in the matrix
    for i in range(1, row):
        for j in range(1, col):
            # Calculating the diagonal score (match score)
            match_value = Score.MATCH if seq1[i - 1] == seq2[j - 1] else Score.MISMATCH
            diagonal_score = matrix[i - 1, j - 1] + match_value

            # Calculating the vertical gap score
            vertical_score = matrix[i - 1, j] + Score.GAP

            # Calculating the horizontal gap score
            horizontal_score = matrix[i, j - 1] + Score.GAP

            # Taking the highest score
            matrix[i, j] = max(0, diagonal_score, vertical_score, horizontal_score)

            # Tracking where the cell's value is coming from
            if matrix[i, j] == 0:
                tracing_matrix[i, j] = Trace.STOP

            elif matrix[i, j] == horizontal_score:
                tracing_matrix[i, j] = Trace.LEFT

            elif matrix[i, j] == vertical_score:
                tracing_matrix[i, j] = Trace.UP

            elif matrix[i, j] == diagonal_score:
                tracing_matrix[i, j] = Trace.DIAGONAL

            # Tracking the cell with the maximum score
            if matrix[i, j] >= max_score:
                max_index = (i,j)
                max_score = matrix[i, j]

    # Initialising the variables for tracing
    aligned_seq1 = ""
    aligned_seq2 = ""
    current_aligned_seq1 = ""
    current_aligned_seq2 = ""
    aligned_idx_seq1 = []
    aligned_idx_seq2 = []
    current_idx_seq1 = -1
    current_idx_seq2 = -1
    (max_i, max_j) = max_index

    # Tracing and computing the pathway with the local alignment
    while tracing_matrix[max_i, max_j] != Trace.STOP:
        if tracing_matrix[max_i, max_j] == Trace.DIAGONAL:
            current_idx_seq1 = max_i - 1
            current_aligned_seq1 = seq1[current_idx_seq1]
            current_idx_seq2 = max_j - 1
            current_aligned_seq2 = seq2[current_idx_seq2]
            max_i = max_i - 1
            max_j = max_j - 1

        elif tracing_matrix[max_i, max_j] == Trace.UP:
            current_idx_seq1 = max_i - 1
            current_aligned_seq1 = seq1[current_idx_seq1]
            current_idx_seq2 = -1
            current_aligned_seq2 = '-'
            max_i = max_i - 1

        elif tracing_matrix[max_i, max_j] == Trace.LEFT:
            current_idx_seq1 = -1
            current_aligned_seq1 = '-'
            current_idx_seq2 = max_j - 1
            current_aligned_seq2 = seq2[current_idx_seq2]
            max_j = max_j - 1

        aligned_seq1 = aligned_seq1 + current_aligned_seq1
        aligned_seq2 = aligned_seq2 + current_aligned_seq2
        aligned_idx_seq1.append(current_idx_seq1)
        aligned_idx_seq2.append(current_idx_seq2)

    # Reversing the order of the sequences
    aligned_seq1 = aligned_seq1[::-1]
    aligned_seq2 = aligned_seq2[::-1]
    aligned_idx_seq1 = aligned_idx_seq1[::-1]
    aligned_idx_seq2 = aligned_idx_seq2[::-1]

    return aligned_seq1, aligned_seq2, aligned_idx_seq1, aligned_idx_seq2

def phrase_match(src, dest):
    a1, a2, idx1, idx2 = smith_waterman(src, dest)

    idx_pairs = [(a, b) for a, b in zip(idx1, idx2) if a != -1 and b != -1]
    range_pairs = [(idx_pairs[0], idx_pairs[0])]
    for a, b in idx_pairs[1:]:
        prev_pair = range_pairs[-1][1]
        if a == prev_pair[0] + 1 and b == prev_pair[1] + 1:
            range_pairs[-1] = (range_pairs[-1][0], (a, b))
        else:
            range_pairs.append(((a, b), (a, b)))

    rhizomes = [((s[0], e[0]), (s[1], e[1])) for s, e in range_pairs]
    for ((a1, a2), (b1, b2)) in rhizomes:
        if a2 - a1 > 5:
            yield ((a1, a2), (b1, b2))
