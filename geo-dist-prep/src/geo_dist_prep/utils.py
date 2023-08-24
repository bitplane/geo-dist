def bisection_sort(seq) -> list:
    """
    Sort a seqence in a way that builds a balanced tree
    """

    def recurse(sorted_list):
        if len(sorted_list) == 0:
            return []
        if len(sorted_list) == 1:
            return [sorted_list[0]]

        # find the median
        median_index = len(sorted_list) // 2
        median = sorted_list[median_index]

        # split into two halves, excluding the median
        lower_half = sorted_list[:median_index]
        upper_half = sorted_list[median_index + 1 :]

        # Recursively sort the two halves
        return [median] + recurse(lower_half) + recurse(upper_half)

    sorted_list = sorted(seq)
    return recurse(sorted_list)
