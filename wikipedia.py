import requests
import pprint
import time
import networkx as nx
import matplotlib.pyplot as plt


def draw_graph(graph):
    g = nx.convert.from_dict_of_lists(graph)
    nx.draw(g)
    plt.savefig("graph.png")


WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

def get_page_links(page_title):
    """
    Docs: https://www.mediawiki.org/wiki/API:Links
    """
    MAX_LINKS_RETURNED = 2
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
        return filtered_pages
    else:
        return []

def recursive_consume_list(page_titles, graph, pages_set, count=0):
    for title in page_titles:
        count+=1
        new_page_titles = get_page_links(title)
        graph[title] = new_page_titles
        pages_set.update(new_page_titles)

        if count < 6:
            recursive_consume_list(new_page_titles, graph, pages_set, count)

if __name__ == "__main__":
    kevin_bacon_page_links = get_page_links("Kevin Bacon")
    graph = {
        "Kevin Bacon": kevin_bacon_page_links
    }
    pages_set = set()

    recursive_consume_list(kevin_bacon_page_links, graph, pages_set)

    graph_existing_keys = set(graph.keys())
    keys_not_present_in_graph = pages_set.difference(graph)
    nodes_without_connection = dict.fromkeys(keys_not_present_in_graph, [])
    graph.update(nodes_without_connection)

    print(f'graph: {graph}\n')
    pretty_print = pprint.PrettyPrinter()
    pretty_print.pprint(graph)

    draw_graph(graph)