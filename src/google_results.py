import os
from multiprocessing import Pool, TimeoutError

from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()
serp_api_key = os.getenv("SERP_API_KEY")


def save_result(count_dict, fix_dict, fixed_dict):
    with open("../data/search_result_count.txt", "w") as search_write_file:
        for key, val in count_dict.items():
            search_write_file.write("{},{}\n".format(key, val))
    with open("../data/spelling_fix.txt", "a") as fix_file:
        for key, val in fix_dict.items():
            fix_file.write("{},{}\n".format(key, val))
    print(fix_dict.keys())
    fix_dict.clear()
    with open("../data/fixed_search.txt", "a") as fixed_file:
        for key, val in fixed_dict.items():
            fixed_file.write("{},{}\n".format(key, val))
    print(fixed_dict.keys())
    fixed_dict.clear()


def fetch_result(query):
    search = GoogleSearch({
        "q": query,
        "api_key": serp_api_key
    })
    search_result = search.get_dict()
    return search_result


if __name__ == "__main__":
    with open("../data/search_result_count.txt", "r") as search_read_file:
        lines = search_read_file.readlines()

    result_dict = {}
    for line in lines:
        line = line.strip()
        if line != "":
            args = line.split(",")
            assert len(args) == 2
            result_dict[args[0]] = args[1]

    success_count = 0
    spelling_fix = {}
    fixed_search = {}
    failed_search = []
    error_flag = False
    timeout_sec = 30
    max_retry_count = 20
    retry_count = 0
    while retry_count < max_retry_count:
        with Pool(processes=1) as pool:
            for idiom in result_dict:
                if result_dict[idiom] == "":
                    res = pool.apply_async(fetch_result, (idiom,))
                    try:
                        result = res.get(timeout=timeout_sec)
                        result_count = result["search_information"]["total_results"]
                        result_dict[idiom] = str(result_count)
                        if "spelling_fix" in result["search_information"]:
                            spelling_fix[idiom] = result["search_information"]["spelling_fix"]
                        if "showing_results_for" in result["search_information"]:
                            fixed_search[idiom] = result["search_information"]["showing_results_for"] + "," + str(result_count)
                        success_count += 1
                        if success_count % 10 == 0:
                            print(".", end="")
                        if success_count % 1000 == 0:
                            print(success_count)
                            save_result(result_dict, spelling_fix, fixed_search)
                    except TimeoutError as timeout:
                        print("Timed out after {} seconds.".format(timeout_sec))
                        result_dict[idiom] = "PLACEHOLDER"
                        failed_search.append(idiom)
                        break
                    except Exception as ex:
                        print("An error occurred during search: {}.".format(idiom))
                        print(ex)
                        failed_search.append(idiom)
                        error_flag = True
                        break

        print(success_count)
        save_result(result_dict, spelling_fix, fixed_search)
        if error_flag:
            print("Stopped due to exceptions.")
            break
        task_remaining = sum([val == "" for val in result_dict.values()])
        if task_remaining == 0:
            print("Search finished.")
            break
        retry_count += 1

    print("Retry count: {}".format(retry_count))
    print("Failed search: {}".format(failed_search))
    # TODO: Remove duplicates after converting from traditional to simplified
    #       Double check idioms with spelling corrections: maybe remove or correct wrongly-spelled word
