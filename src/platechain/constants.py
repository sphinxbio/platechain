import itertools
import string


def generate_row_letters(num_strings: int, max_length: int = 2):
    counter = 0
    for length in range(1, max_length + 1):
        if counter >= num_strings:
            break
        for item in itertools.product(string.ascii_uppercase, repeat=length):
            if counter >= num_strings:
                return
            yield "".join(item)
            counter += 1


# 1536 well plates have 32 rows, which we will assume is the max for now
ROW_LETTERS = list(generate_row_letters(32))

# We only support standard plate sizes for right now
ROWS_TO_WELLS_DICT = {4: 24, 8: 96, 16: 384, 32: 1536}
COLS_TO_WELLS_DICT = {6: 24, 12: 96, 24: 384, 48: 1536}
