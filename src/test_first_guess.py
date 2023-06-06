from search import *


def test_first_guess(guess: str,
                     answer_list: list[str],
                     dict_subset: dict[str: list[list[str]]],
                     guess_vocab: dict[str: dict[str: list[list[str]]]] = None,
                     guess_entropy: float = None):
    start_time = time.time()
    trial_counter = defaultdict(int)
    for answer in answer_list:
        epoch = test_run(guess, answer, dict_subset, guess_vocab, guess_entropy)
        trial_counter[epoch] += 1
    end_time = time.time()
    average_time = (end_time - start_time) / len(answer_list)
    print("Average time per guess: {:.2f}ms".format(average_time * 1000))
    average_trial = sum(x[0] * x[1] for x in trial_counter.items()) / sum(trial_counter.values())
    print("Average trial count: {:2f}".format(average_trial))
    trial_counter_sorted = sorted(trial_counter.items())
    for trial_count, occurrence in trial_counter_sorted:
        print("[{}]  {:>5}  {:.2%}".format(trial_count, occurrence, occurrence / sum(trial_counter.values())))


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
    with open("../data/first_guess.txt", "r") as guess_file:
        best_guess, max_guess_entropy = guess_file.readline().strip().split(",")
        assert len(best_guess) == 4
        max_guess_entropy = float(max_guess_entropy)
    with open("../data/first_guess_vocab.pkl", "rb") as guess_vocab_file:
        best_guess_vocab = pickle.load(guess_vocab_file)
    with open("../data/answer.txt", "r") as answer_file:
        answers = answer_file.read().splitlines()

    # test_first_guess(best_guess, list(idiom_dict.keys()), idiom_dict, best_guess_vocab, max_guess_entropy)
    """
    Using first guess: 研经铸史
        Average time per guess: 1.67ms
        Average trial count: 2.595094
        [1]      1  0.00%
        [2]  12753  42.85%
        [3]  16312  54.81%
        [4]    684  2.30%
        [5]      9  0.03%
        [6]      1  0.00%
    """
    test_first_guess(best_guess, answers, idiom_dict, best_guess_vocab, max_guess_entropy)
    """
    Using first guess: 研经铸史
        Average time per guess: 1.72ms
        Average trial count: 2.566038
        [2]    194  45.75%
        [3]    220  51.89%
        [4]     10  2.36%
    """
