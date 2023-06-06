import json
import pickle
from collections import defaultdict

from utils import *


if __name__ == "__main__":
    with open("../data/polyphones.json", "r") as pinyin_file:
        corrections = json.load(pinyin_file)
    with open("../data/idioms.txt", "r") as idioms_file:
        idioms = idioms_file.read().splitlines()

    char_counter = defaultdict(int)
    init_counter = defaultdict(int)
    finals_counter = defaultdict(int)
    tone_counter = defaultdict(int)
    idioms_pinyin_dict = {}

    for example in idioms:
        if len(example) == 4:
            this_pinyin_parts = parse_idiom_pinyin(example)
            example_list = [list(example), *this_pinyin_parts]
            idioms_pinyin_dict[example] = example_list

    for example in corrections:
        if len(example) == 4:
            correct_pinyin = corrections[example].strip()
            correct_pinyin_parts = parse_idiom_pinyin_from_str(correct_pinyin)
            example_list = [list(example), *correct_pinyin_parts]
            idioms_pinyin_dict[example] = example_list

    with open("../data/idioms_pinyin_dict.pkl", "wb") as idioms_dict_file:
        pickle.dump(idioms_pinyin_dict, idioms_dict_file)

    for entry in idioms_pinyin_dict.values():
        for character in entry[0]:
            char_counter[character] += 1
        for init in entry[1]:
            init_counter[init] += 1
        for finals in entry[2]:
            finals_counter[finals] += 1
        for tone in entry[3]:
            tone_counter[tone] += 1

    print("Total idiom count: ", len(idioms_pinyin_dict))
    print("Unique character count: ", len(char_counter))
    print(sorted(char_counter.items(), key=lambda x: x[1], reverse=True))
    print(sorted(init_counter.items(), key=lambda x: x[1], reverse=True))
    print(sorted(finals_counter.items(), key=lambda x: x[1], reverse=True))
    print(tone_counter)
