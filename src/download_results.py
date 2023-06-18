import json
import re
import requests


if __name__ == "__main__":
    query_list = []
    non_idiom_list = []
    json_url_pattern = r"\"(https?://.+\.json)\""

    for page_num in range(298):
        with open("../data/pages/" + str(page_num) + ".html", "r") as serp_page:
            serp_data = serp_page.read()
        print("Page {}: ".format(page_num), end="")
        json_urls = re.findall(json_url_pattern, serp_data)
        if len(json_urls) != 100:
            print("Warning: This page has {} JSON urls.".format(len(json_urls)))
        count = 0
        for json_url in json_urls:
            r = requests.get(json_url)
            if r.ok:
                content = r.content.decode("utf-8")
                json_data = json.loads(content)
                query = json_data["search_parameters"]["q"].strip("\"\'")
                query = query + "1" if query in query_list else query
                query_list.append(query)
                json_filename = query + ".json"
                with open("../data/search_results/" + json_filename, "w") as json_out:
                    json_out.write(content)
                if "成语" not in content and "成語" not in content:
                    non_idiom_list.append(query)
                count += 1
                if count % 10 == 0:
                    print(".", end="")
            else:
                print("Error downloading json file: " + json_url)
                break
        print("Done.".format(page_num))

    print(len(non_idiom_list))
    with open("../data/non_idiom_candidates.txt", "a") as non_idiom_file:
        for word in non_idiom_list:
            non_idiom_file.write(word + "\n")
