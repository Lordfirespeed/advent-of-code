from math import prod as product

with open(r"Input\2020day13.txt") as inputfile:
    input_data = [line.strip() for line in inputfile.readlines()]

bus_IDs = [int(bus_id) if bus_id != "x" else "x" for bus_id in input_data[1].split(",")]
target_offsets = {index: bus_id for index, bus_id in enumerate(bus_IDs) if bus_id != "x"}
remainders = [(bus_id, bus_id-index if index != 0 else 0) for index, bus_id in target_offsets.items()]


def extended_euclid(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = extended_euclid(b % a, a)
        return g, x - (b // a) * y, y


def modinv(a, m):
    g, x, y = extended_euclid(a, m)
    return x % m


def chinese_remainder(pairs):
    n_series, r_series = [list(series) for series in list(zip(*pairs))]

    while len(r_series) != 1:

        # temp1 will contain the new value
        # of A. which is calculated according
        # to the equation m1' * m1 * x0 + m0'
        # * m0 * x1
        temp1 = modinv(n_series[1], n_series[0]) * r_series[0] * n_series[1] + \
                modinv(n_series[0], n_series[1]) * r_series[1] * n_series[0]

        # temp2 contains the value of the modulus
        # in the new equation, which will be the
        # product of the modulii of the two
        # equations that we are combining
        temp2 = n_series[0] * n_series[1]

        # we then remove the first two elements
        # from the list of remainders, and replace
        # it with the remainder value, which will
        # be temp1 % temp2
        r_series.remove(r_series[0])
        r_series.remove(r_series[0])
        r_series.insert(0, temp1 % temp2)

        # we then remove the first two values from
        # the list of modulii as we no longer require
        # them and simply replace them with the new
        # modulii that  we calculated
        n_series.remove(n_series[0])
        n_series.remove(n_series[0])
        n_series.insert(0, temp2)

        # once the list has only one element left,
        # we can break as it will only contain
        # the value of our final remainder

    # returns the remainder of the final equation
    return r_series[0]


solution = chinese_remainder(remainders)

print(f"t = {solution}")
