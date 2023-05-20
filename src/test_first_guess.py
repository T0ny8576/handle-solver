from search import *


def test_first_guess(guess: str,
                     guess_vocab: dict[str: dict[str: list[list[str]]]] = None,
                     guess_entropy: float = None):
    start_time = time.time()
    trial_counter = defaultdict(int)
    for answer in idiom_dict:
        epoch = test_run(guess, answer, idiom_dict, guess_vocab, guess_entropy)
        trial_counter[epoch] += 1
    end_time = time.time()
    average_time = (end_time - start_time) / len(idiom_dict)
    print("Average time per guess: {:.2f}ms".format(average_time * 1000))
    average_trial = sum(x[0] * x[1] for x in trial_counter.items()) / sum(trial_counter.values())
    print("Average trial count: {:2f}".format(average_trial))
    trial_counter_sorted = sorted(trial_counter.items())
    for trial_count, occurrence in trial_counter_sorted:
        print("[{}]  {:>5}  {:.2%}".format(trial_count, occurrence, occurrence / sum(trial_counter.values())))
    """
    Result with first guess: 研经铸史
    Average time per guess: 1.54ms
    Average trial count: 2.581653
    [1]      1  0.00%
    [2]  13094  44.00%
    [3]  16032  53.87%
    [4]    621  2.09%
    [5]     11  0.04%
    [6]      1  0.00%
    """


if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.WARNING)
    with open("../data/first_guess.txt", "r") as guess_file:
        best_guess, max_guess_entropy = guess_file.readlines()[0].strip().split(",")
        assert len(best_guess) == 4
        max_guess_entropy = float(max_guess_entropy)
    with open("../data/first_guess_vocab.pkl", "rb") as guess_vocab_file:
        best_guess_vocab = pickle.load(guess_vocab_file)
    test_first_guess(best_guess, best_guess_vocab, max_guess_entropy)
