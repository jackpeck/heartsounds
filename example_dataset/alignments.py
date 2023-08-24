# User Offset Direction (data to cut)
# < 0 remove from ecg, > 0 remove from audio

better_alignments = [
    (1, -0.48914),
    (2, 1.8511),
    (3, 2.7234),
    (4, -3.22),
    (5, -3.6703),
    (6, -8.992),
    (7, -8.7597),
    (8, -5.2211),
    (9, -4.3918),
    (10, -7.4155),
    (12, -8.872),
    (13, -8.183),
    (14, -8.09),
    (15, -8.809),
    (16, -5.587),
    (17, -2.236),
    (18, -7.452),
    (19, -8.53),
]

subjects = [i for i, _ in better_alignments]

def get_alignment_offset (subject):
    return [i for i in better_alignments if i[0] == subject][0][1]