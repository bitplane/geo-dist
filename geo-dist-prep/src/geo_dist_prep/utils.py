from math import pi

degree_to_rad = float(pi / 180.0)


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


def format_int(num):
    if num < 1000:
        return f"{num:.2f}"
    magnitude = 0
    while abs(num) >= 1000 and magnitude < 5:
        magnitude += 1
        num /= 1000
    return f"{num:.2f}{['', 'k', 'M', 'G', 'T'][magnitude]}"
