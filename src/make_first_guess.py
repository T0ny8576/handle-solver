from search import *


def search_first_guess(dict_subset: dict[str: list[list[str]]]) -> (list[(str, float)],
                                                                    dict[str: dict[str: list[list[str]]]]):
    max_entropy = 0.
    max_entropy_vocab = {}
    guess_entropy_dict = {}
    for guess in dict_subset:
        grouped, entropy = evaluate_guess(guess, dict_subset)
        guess_entropy_dict[guess] = entropy
        if entropy >= max_entropy:
            max_entropy = entropy
            max_entropy_vocab = grouped
    sorted_guess_entropy_list = sorted(guess_entropy_dict.items(), key=lambda x: x[1], reverse=True)
    return sorted_guess_entropy_list, max_entropy_vocab


if __name__ == "__main__":
    sorted_guess, guess_vocab = search_first_guess(idiom_dict)
    with open("../data/first_guess.txt", "w") as guess_file:
        for idiom, value in sorted_guess:
            guess_file.write("{},{}\n".format(idiom, value))
    with open("../data/first_guess_vocab.pkl", "wb") as guess_vocab_file:
        pickle.dump(guess_vocab, guess_vocab_file)
    print(sorted_guess[:10])
