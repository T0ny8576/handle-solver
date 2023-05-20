from search import *


def search_first_guess():
    max_entropy = 0.
    max_entropy_vocab = {}
    guess_entropy_dict = {}
    for guess in idiom_dict:
        grouped, entropy = evaluate_guess(guess, idiom_dict)
        guess_entropy_dict[guess] = entropy
        if entropy >= max_entropy:
            max_entropy = entropy
            max_entropy_vocab = grouped
    sorted_guess_entropy_list = sorted(guess_entropy_dict.items(), key=lambda x: x[1], reverse=True)
    with open("../data/first_guess.txt", "w") as guess_file:
        for idiom, value in sorted_guess_entropy_list:
            guess_file.write("{},{}\n".format(idiom, value))
    with open("../data/first_guess_vocab.pkl", "wb") as guess_vocab_file:
        pickle.dump(max_entropy_vocab, guess_vocab_file)
    print(sorted_guess_entropy_list[:10])


if __name__ == "__main__":
    search_first_guess()
