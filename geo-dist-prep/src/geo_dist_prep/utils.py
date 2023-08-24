def bisection_sort(seq) -> list:
    """
    Sort a seqence in a way that builds a balanced tree
    """
    current = [sorted(seq)]
    output = []

    while current:
        new = []
        for c in current:
            if not c:
                continue
            median_index = len(c) // 2
            middle = c[median_index]
            front = c[:median_index]
            back = c[median_index + 1 :]

            output.append(middle)
            new = [front] + new + [back]

        current = new

    return output
