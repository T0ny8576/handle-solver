from search import *


def solve(dict_subset: dict[str: list[list[str]]] = idiom_dict) -> int:
    epoch = 1
    next_vocab = dict_subset
    while epoch <= 10:
        print("\nEpoch {}:".format(epoch))
        guess = input("Enter a 4-character Chinese word: ").strip()
        if guess in ["q", "quit", "exit"]:
            return -1
        valid_guess = False
        while not valid_guess:
            try:
                guess_init, guess_finals, guess_tone = parse_idiom_pinyin(guess)
                valid_guess = True
            except AssertionError:
                guess = input("Invalid input. Try again: ").strip()
                if guess in ["q", "quit", "exit"]:
                    return -1
        if guess in dict_subset:
            _, guess_init, guess_finals, guess_tone = dict_subset[guess]
        correct_pinyin = input("Press [Enter] if this is the correct pinyin: {}\n"
                               "If not, type the correct pinyin here: "
                               .format(" ".join([guess_init[i] + guess_finals[i] + guess_tone[i]
                                                 for i in range(4)]))).strip()
        if correct_pinyin != "":
            try:
                guess_parts = parse_idiom_pinyin_from_str(correct_pinyin)
                guess_init, guess_finals, guess_tone = guess_parts
            except AssertionError:
                pass

        match_result = input("Enter match result pattern, or press [Enter] for detailed input: ").strip()
        if match_result == "" or len(match_result) != 16:
            matched_char = input("Exactly matched character index [1234]: ").strip()
            misplaced_char = input("Misplaced character index [1234]: ").strip()
            matched_init = input("Exactly matched pinyin initials index [1234]: ").strip()
            misplaced_init = input("Misplaced pinyin initials index [1234]: ").strip()
            matched_finals = input("Exactly matched pinyin finals index [1234]: ").strip()
            misplaced_finals = input("Misplaced pinyin finals index [1234]: ").strip()
            matched_tone = input("Exactly matched tone index [1234]: ").strip()
            misplaced_tone = input("Misplaced tone index [1234]: ").strip()
            match_result = (index_to_pattern(matched_char, misplaced_char) +
                            index_to_pattern(matched_init, misplaced_init) +
                            index_to_pattern(matched_finals, misplaced_finals) +
                            index_to_pattern(matched_tone, misplaced_tone))
        if match_result == MATCH_CODE * 16:
            print("You win!\nAnswer: {}".format(guess))
            return epoch
        grouped_vocab, guess_entropy = evaluate_guess(guess, next_vocab, (guess_init, guess_finals, guess_tone))
        next_vocab = grouped_vocab[match_result]
        if len(next_vocab) < 1:
            logging.warning("Error: Out of Vocabulary.")
            return -1
        print("Next ({}) available idioms: {}".format(len(next_vocab), list(next_vocab.keys())))

        # Find the next guess with maximum entropy
        epoch += 1
        max_entropy = 0.
        for new_guess in next_vocab:
            grouped, entropy = evaluate_guess(new_guess, next_vocab)
            if entropy >= max_entropy:
                max_entropy = entropy
                guess = new_guess
        print("Suggestion: {}".format(guess))
    print("\nFailed to find answer within 10 epochs.")
    return epoch


if __name__ == "__main__":
    epoch_used = solve()
