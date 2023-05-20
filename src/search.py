import pickle
import math
from collections import defaultdict
import time
import logging

from utils import *

with open("../data/idioms_pinyin_dict.pkl", "rb") as dict_file:
    idiom_dict = pickle.load(dict_file)


def check_exact_match(guess_list: list[str],
                      truth_list: list[str],
                      match_list: list[str],
                      truth_used_list: list[bool]):
    assert len(guess_list) == len(truth_list) == len(match_list) == len(truth_used_list) == 4
    for i in range(4):
        if guess_list[i] == truth_list[i]:
            match_list[i] = MATCH_CODE
            truth_used_list[i] = True


def check_misplaced_match(guess_list: list[str],
                          truth_list: list[str],
                          match_list: list[str],
                          truth_used_list: list[bool]):
    assert len(guess_list) == len(truth_list) == len(match_list) == len(truth_used_list) == 4
    for i in range(4):
        if match_list[i] == NON_MATCH_CODE:
            for j in range(4):
                if not truth_used_list[j] and guess_list[i] == truth_list[j]:
                    match_list[i] = MISMATCH_CODE
                    truth_used_list[j] = True
                    break


def match(guess_char: list[str],
          guess_init: list[str],
          guess_finals: list[str],
          guess_tone: list[str],
          truth_char: list[str],
          truth_init: list[str],
          truth_finals: list[str],
          truth_tone: list[str]) -> str:
    char_match = [NON_MATCH_CODE] * 4
    init_match = [NON_MATCH_CODE] * 4
    finals_match = [NON_MATCH_CODE] * 4
    tone_match = [NON_MATCH_CODE] * 4
    truth_char_used = [False] * 4
    truth_init_used = [False] * 4
    truth_finals_used = [False] * 4
    truth_tone_used = [False] * 4

    # Look for exact match
    check_exact_match(guess_char, truth_char, char_match, truth_char_used)
    check_exact_match(guess_init, truth_init, init_match, truth_init_used)
    check_exact_match(guess_finals, truth_finals, finals_match, truth_finals_used)
    check_exact_match(guess_tone, truth_tone, tone_match, truth_tone_used)

    # Look for misplaced match
    check_misplaced_match(guess_char, truth_char, char_match, truth_char_used)
    check_misplaced_match(guess_init, truth_init, init_match, truth_init_used)
    check_misplaced_match(guess_finals, truth_finals, finals_match, truth_finals_used)
    check_misplaced_match(guess_tone, truth_tone, tone_match, truth_tone_used)

    match_pattern = "".join(char_match) + "".join(init_match) + "".join(finals_match) + "".join(tone_match)
    return match_pattern


def match_all(guess: str,
              vocab: dict[str: list[list[str]]],
              guess_pinyin_parts: (list[str], list[str], list[str]) = None) -> dict[str: dict[str: list[list[str]]]]:
    assert len(guess) == 4
    if guess_pinyin_parts is not None:
        guess_init, guess_finals, guess_tone = guess_pinyin_parts
        assert len(guess_init) == len(guess_finals) == len(guess_tone) == 4
    elif guess in idiom_dict:
        _, guess_init, guess_finals, guess_tone = idiom_dict[guess]
    else:
        guess_init, guess_finals, guess_tone = parse_idiom_pinyin(guess)

    match_pattern_dict = defaultdict(dict)
    for idiom, parts in vocab.items():
        match_pattern = match(list(guess), guess_init, guess_finals, guess_tone,
                              parts[0], parts[1], parts[2], parts[3])
        match_pattern_dict[match_pattern][idiom] = parts
    return match_pattern_dict


def evaluate_guess(guess: str,
                   vocab: dict[str: list[list[str]]],
                   guess_pinyin_parts: tuple[list[str]] = None) -> (dict[str: dict[str: list[list[str]]]], float):
    grouped_vocab = match_all(guess, vocab, guess_pinyin_parts)
    sorted_selected = sorted(grouped_vocab.items(), key=lambda x: len(x[1]), reverse=True)
    guess_entropy = 0.
    for ptn, result in sorted_selected:
        guess_entropy += len(result) / len(vocab) * math.log2(len(vocab) / len(result))
    return grouped_vocab, guess_entropy


def test_run(guess: str,
             answer: str,
             vocab: dict[str: list[list[str]]],
             grouped_vocab: dict[str: dict[str: list[list[str]]]] = None,
             guess_entropy: float = None) -> int:
    assert len(guess) == len(answer) == 4

    truth_parts = vocab[answer]
    total_uncertainty = math.log2(len(idiom_dict))
    logging.info("Game Start\nTotal uncertainty: {}\n".format(total_uncertainty))
    start_time = time.time()
    epoch = 1
    if grouped_vocab is None or guess_entropy is None:
        grouped_vocab, guess_entropy = evaluate_guess(guess, idiom_dict)

    while epoch <= 10:
        logging.info("Epoch {}:\nGuess: {}\nEntropy of this guess: {}".format(epoch, guess, guess_entropy))
        if guess == answer:
            end_time = time.time()
            logging.info("\nYou win!")
            logging.info("Answer: {}".format(answer))
            logging.info("Time: {:.2f}s".format(end_time - start_time))
            return epoch

        if guess in idiom_dict:
            _, guess_init, guess_finals, guess_tone = idiom_dict[guess]
        else:
            guess_init, guess_finals, guess_tone = parse_idiom_pinyin(guess)
        match_result = match(list(guess), guess_init, guess_finals, guess_tone,
                             truth_parts[0], truth_parts[1], truth_parts[2], truth_parts[3])
        next_vocab = grouped_vocab[match_result]
        if len(next_vocab) < 1:
            logging.warning("Error: Out of Vocabulary.\nAnswer: {}".format(answer))
            return epoch
        uncertainty_remaining = math.log2(len(next_vocab))
        logging.info("Result:\n{}".format(
            format_match_result(guess, guess_init, guess_finals, guess_tone, match_result)))
        logging.info("Uncertainty after this guess: {}".format(uncertainty_remaining))
        logging.info("Next ({}) available idioms: {}\n".format(len(next_vocab), list(next_vocab.keys())))

        # Find the next guess with maximum entropy
        epoch += 1
        max_entropy = 0.
        for new_guess in next_vocab:
            grouped, entropy = evaluate_guess(new_guess, next_vocab)
            if entropy >= max_entropy:
                max_entropy = entropy
                guess = new_guess
                grouped_vocab = grouped
        guess_entropy = max_entropy
    logging.warning("Failed to find answer within 10 epochs.\nAnswer: {}".format(answer))
    return epoch


if __name__ == "__main__":
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    my_guess = "身不由己"
    real_answer = "花前月下"
    test_run(my_guess, real_answer, idiom_dict)
