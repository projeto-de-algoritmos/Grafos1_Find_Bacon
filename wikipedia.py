import requests
import pprint
import time


WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"


def get_page_links(page_title):
    """
    Docs: https://www.mediawiki.org/wiki/API:Links
    """
    MAX_LINKS_RETURNED = 5
    ARTICLE_NAMESPACE = "0"  # https://en.wikipedia.org/wiki/Wikipedia:Namespace

    formatted_page_title = page_title.replace(" ", "_")

    params = {
        "action": "query",
        "titles": formatted_page_title,
        "format": "json",
        "prop": "links",
        "plnamespace": ARTICLE_NAMESPACE,
        "pllimit": MAX_LINKS_RETURNED
    }
    r = requests.get(url=WIKIPEDIA_API_URL, params=params)
    page_data = r.json()

    page_id_key = list(page_data["query"]["pages"].keys())
    page_id = page_id_key[0]

    if int(page_id) != -1:
        page_links_list = page_data["query"]["pages"][page_id]["links"]
        filtered_pages = [page_link["title"] for page_link in page_links_list]
        return page_title, filtered_pages
    else:
        return page_title, []

def build_graph(page_titles, graph):
    for title in page_titles:
        page_title, pages_list = get_page_links(title)

        if page_title not in graph:
            graph[page_title] = pages_list
            for page in pages_list:
                if page not in graph:
                    graph[page] = []
        else:
            graph[page_title].append(pages_list)
    return graph

if __name__ == "__main__":
    # kevin_bacon_page_id = get_page_id("Kevin Bacon")
    start = time.time()

    _, kevin_bacon_page_links = get_page_links("Kevin Bacon")
    kevin_bacon_graph = {
        "Kevin Bacon": kevin_bacon_page_links
    }

    graph = build_graph(kevin_bacon_page_links, kevin_bacon_graph)

    pretty_print = pprint.PrettyPrinter()
    pretty_print.pprint(graph)
