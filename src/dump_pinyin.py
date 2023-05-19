import json
import pickle
from collections import defaultdict

from utils import parse_idiom_pinyin

PINYIN_INITIALS = ["y", "d", "b", "sh", "x", "n", "zh", "m", "l", "q", "h", "s", "g", "w", "ch", "j", "f",
                   "t", "r", "c", "z", "k", "p"]
PINYIN_FINALS = ["i", "ing", "u", "iao", "in", "iu", "ong", "iong", "en", "e", "ao", "ua", "ou", "iang", "an", "uan",
                 "ian", "eng", "ei", "ie", "ai", "o", "ang", "un", "a", "ue", "uang", "ia", "uai", "ui", "er", "uo",
                 "v", "ve"]


if __name__ == "__main__":
    with open("../data/polyphones.json", "r") as pinyin_file:
        corrections = json.load(pinyin_file)
    # with open("../data/answer.txt", "r") as answer_file:
    #     answer = answer_file.readlines()
    with open("../data/idioms.txt", "r") as idioms_file:
        idioms = idioms_file.readlines()

    char_counter = defaultdict(int)
    init_counter = defaultdict(int)
    finals_counter = defaultdict(int)
    tone_counter = defaultdict(int)
    idioms_pinyin_dict = {}

    for example in idioms:
        example = example.strip()
        if len(example) == 4:
            this_init_list, this_finals_list, this_tone_list = parse_idiom_pinyin(example)
            example_list = [list(example), this_init_list, this_finals_list, this_tone_list]

            idioms_pinyin_dict[example] = example_list

    for example in corrections:
        example = example.strip()
        if len(example) == 4:
            correct_pinyin = corrections[example].strip().split()
            correct_initials = []
            correct_finals = []
            correct_tones = []
            for y in correct_pinyin:
                this_init, this_finals, this_tone = "", "", ""
                if len(y) > 0 and y[-1] in "1234":
                    this_tone = y[-1]
                    y = y[:-1]
                for init in PINYIN_INITIALS:
                    if y.startswith(init):
                        this_init = init
                        y = y.removeprefix(init)
                        break
                for finals in PINYIN_FINALS:
                    if y == finals:
                        this_finals = finals
                        break
                correct_initials.append(this_init)
                correct_finals.append(this_finals)
                correct_tones.append(this_tone)
            example_list = [list(example), correct_initials, correct_finals, correct_tones]

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
