def bisection_sort(seq) -> list:
    """
    Sort a seqence in a way that builds a balanced tree
    """
    seq = sorted(seq)
    visited = set()

    step = len(seq) // 2
    pos = step
    output = []

    while step > 0:
        for i in range(pos, len(seq), step):
            if i in visited:
                continue
            output.append(seq[i])
            visited.add(i)
        step = step // 2
        pos = step

    if len(output) != len(seq):
        output.append(seq[0])

    return output
