def add_one(x):
    y = x + 1
    return y


def times_five(x):
    # checks if x is a number
    if not isinstance(x, (int, float)):
        return "Error: Input must be a number"
    return 5 * x


print(add_one(41))
