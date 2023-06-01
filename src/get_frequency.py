import pickle

if __name__ == "__main__":
    with open("../data/idioms_pinyin_dict.pkl", "rb") as dict_file:
        idiom_dict = pickle.load(dict_file)
    idioms = list(idiom_dict.keys())

    # Reference: https://www.ugent.be/pp/experimentele-psychologie/en/research/documents/subtlexch/overview.htm
    with open("../data/SUBTLEX-CH-WF", "r", encoding="gb18030") as freq_file:
        lines = freq_file.readlines()
    word_list = []
    for line in lines[3:]:
        line = line.strip()
        if line != "":
            word_list.append(line.split()[0])

    common_set = set()
    for word in word_list:
        if word in idioms:
            common_set.add(word)

    with open("../data/answer.txt", "r") as answer_file:
        answer = answer_file.readlines()
    for idiom in answer:
        idiom = idiom.strip()
        common_set.add(idiom)
    with open("../data/common.txt", "w") as common_file:
        for idiom in common_set:
            common_file.write("{}\n".format(idiom))
    print(len(common_set))
