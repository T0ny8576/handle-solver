from pypinyin import pinyin, Style

NON_MATCH_CODE = "0"
MISMATCH_CODE = "1"
MATCH_CODE = "2"


def parse_idiom_pinyin(word: str) -> (list[str], list[str], list[str]):
    init_list = [item[0] for item in pinyin(word, style=Style.INITIALS, strict=False)]
    finals_list = [item[0] for item in pinyin(word, style=Style.FINALS, strict=False)]
    tone_list = [item[0][-1] if len(item[0]) > 0 and item[0][-1] in "1234" else ""
                 for item in pinyin(word, style=Style.TONE3)]
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
