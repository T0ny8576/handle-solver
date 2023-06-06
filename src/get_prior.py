import math

NUM_COMMON = 10000
STRETCH_FACTOR = 2.


def sigmoid(x: float):
    return 1. / (1. + math.exp(-x))


def get_prior_from_count(num_common: int = NUM_COMMON):
    # Reference: https://github.com/3b1b/videos/blob/master/_2022/wordle/simulations.py

    with open("../data/search_result_count.txt", "r") as sorted_file:
        lines = sorted_file.read().splitlines()
    idioms = [line.split(",")[0] for line in lines]
    idiom_count = [int(line.split(",")[1]) for line in lines]
    # Map idioms sorted by frequency to x-coordinates on a number line by applying log10
    idiom_x_coord = [STRETCH_FACTOR * math.log10(count) for count in idiom_count]
    # Shift the x-coordinates so that the num_common most common words are positive after applying sigmoid
    shift_offset = idiom_x_coord[num_common]
    idiom_x_coord = [x - shift_offset for x in idiom_x_coord]
    idiom_prior = [sigmoid(x) for x in idiom_x_coord]

    with open("../data/idiom_prior.txt", "w") as prior_file:
        for i, idiom in enumerate(idioms):
            prior_file.write("{},{}\n".format(idiom, idiom_prior[i]))


if __name__ == "__main__":
    get_prior_from_count()
