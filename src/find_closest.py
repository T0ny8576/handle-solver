import json
from collections import defaultdict

if __name__ == "__main__":
    with open("../data/polyphones.json", "r") as pinyin_file:
        corrections = json.load(pinyin_file)
    with open("../data/idioms.txt", "r") as idioms_file:
        idioms = idioms_file.readlines()
    idioms = [item.strip() for item in idioms]
    for idiom in corrections:
        if idiom not in idioms:
            idioms.append(idiom)

    # for idiom in idioms:
    #     assert len(idiom) == 4
    idiom_distance_dict = defaultdict(list)

    for idiom in idioms:
        for pair in idioms:
            distance = sum([idiom[i] != pair[i] for i in range(4)])
            if distance == 1:
                idiom_distance_dict[idiom].append(pair)

    with open("../data/closest.txt", "w") as f1:
        for key, val in idiom_distance_dict.items():
            f1.write("{}: {}\n".format(key, val))
    print(idiom_distance_dict)
    print(len(idiom_distance_dict))
    print(sum([len(pair) for pair in idiom_distance_dict.values()]))
