# Let's calculate the total number of ways to choose a single interval from 1 to n-1
# and then the total number of ways to choose two intervals, which will be used
# to calculate the probability of overlap.

# For a single interval, the start point can be any number from 1 to n-1,
# and for each start point, the end point can be from the start point to n-1.


def total_ways_single_interval(n):
    total_ways = 0
    for start in range(1, n):  # From 1 to n-1
        for end in range(start, n):  # From start point to n-1
            total_ways += 1
    return total_ways


def total_ways_two_intervals(n):
    # The total number of ways to choose two intervals is simply the square of the
    # number of ways to choose a single interval, since each interval is chosen independently.
    single_interval_ways = total_ways_single_interval(n)
    return single_interval_ways**2


# To calculate the number of overlapping intervals, we need to consider each possible starting point
# of the first interval, each possible ending point of the first interval, and then for each of those,
# how many ways the second interval can be chosen to overlap with it.


def overlapping_intervals(n):
    overlapping_cases = 0
    for start1 in range(1, n):  # Start point of the first interval
        for end1 in range(start1, n):  # End point of the first interval
            for start2 in range(1, n):  # Start point of the second interval
                for end2 in range(start2, n):  # End point of the second interval
                    # Check if the intervals overlap
                    if start2 <= end1 and start1 <= end2:
                        overlapping_cases += 1
    return overlapping_cases


if __name__ == "__main__":
    for n in range(2, 100):
        total_ways_double = total_ways_two_intervals(n)
        overlapping_cases = overlapping_intervals(n)
        print(f"Probability of overlap is {overlapping_cases/total_ways_double:.2f}")
