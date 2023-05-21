from pypinyin import pinyin, Style

NON_MATCH_CODE = "0"
MISMATCH_CODE = "1"
MATCH_CODE = "2"

PINYIN_INITIALS = ["y", "d", "b", "sh", "x", "n", "zh", "m", "l", "q", "h", "s", "g", "w", "ch", "j", "f",
                   "t", "r", "c", "z", "k", "p"]
PINYIN_FINALS = ["i", "ing", "u", "iao", "in", "iu", "ong", "iong", "en", "e", "ao", "ua", "ou", "iang", "an", "uan",
                 "ian", "eng", "ei", "ie", "ai", "o", "ang", "un", "a", "ue", "uang", "ia", "uai", "ui", "er", "uo",
                 "v", "ve"]


def parse_idiom_pinyin(word: str) -> (list[str], list[str], list[str]):
    assert len(word) == 4
    init_list = [item[0] for item in pinyin(word, style=Style.INITIALS, strict=False)]
    finals_list = [item[0] for item in pinyin(word, style=Style.FINALS, strict=False)]
    tone_list = [item[0][-1] if len(item[0]) > 0 and item[0][-1] in "1234" else ""
                 for item in pinyin(word, style=Style.TONE3)]
    assert len(init_list) == len(finals_list) == len(tone_list) == 4
    finals_list = [finals_list[i].replace("u", "v")
                   if init_list[i] in ["y", "j", "q", "x"] and finals_list[i].startswith("u")
                   else finals_list[i] for i in range(4)]
    return init_list, finals_list, tone_list


def parse_idiom_pinyin_from_str(tone2_str: str) -> (list[str], list[str], list[str]):
    tone2_list = tone2_str.split()
    assert len(tone2_list) == 4
    init_list = []
    finals_list = []
    tone_list = []
    for y in tone2_list:
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
                if this_init in ["y", "j", "q", "x"] and y.startswith("u"):
                    this_finals = finals.replace("u", "v")
                else:
                    this_finals = finals
                break
        init_list.append(this_init)
        finals_list.append(this_finals)
        tone_list.append(this_tone)
    return init_list, finals_list, tone_list


def format_pattern(guess_list: list[str],
                   pattern: str) -> list[str]:
    assert len(guess_list) == len(pattern) == 4
    result_list = []
    for i in range(4):
        if pattern[i] == MATCH_CODE:
            result_list.append(guess_list[i])
        elif pattern[i] == MISMATCH_CODE:
            result_list.append("[{}]".format(guess_list[i]))
        else:
            result_list.append("[]")
    return result_list


def format_match_result(guess: str,
                        guess_init: list[str],
                        guess_finals: list[str],
                        guess_tone: list[str],
                        match_pattern: str) -> str:
    assert len(match_pattern) == 16
    char_match_str = format_pattern(list(guess), match_pattern[:4])
    init_match_str = format_pattern(guess_init, match_pattern[4:8])
    finals_match_str = format_pattern(guess_finals, match_pattern[8:12])
    tone_match_str = format_pattern(guess_tone, match_pattern[12:])
    phone_match_str = [init_match_str[i] + finals_match_str[i] for i in range(4)]
    tone_match_formatted = "{:>10}{:>10}{:>10}{:>10}\n".format(*tone_match_str)
    phone_match_formatted = "{:>10}{:>10}{:>10}{:>10}\n".format(*phone_match_str)
    char_match_formatted = "{:>10}{:>10}{:>10}{:>10}".format(*char_match_str)
    return tone_match_formatted + phone_match_formatted + char_match_formatted


def index_to_pattern(matched_indices: str,
                     misplaced_indices: str) -> str:
    base_pattern = [NON_MATCH_CODE] * 4
    matched_list = [int(i) for i in "1234" if i in matched_indices]
    misplaced_list = [int(i) for i in "1234" if i in misplaced_indices]
    for idx in misplaced_list:
        base_pattern[idx - 1] = MISMATCH_CODE
    for idx in matched_list:
        base_pattern[idx - 1] = MATCH_CODE
    pattern = "".join(base_pattern)
    return pattern
