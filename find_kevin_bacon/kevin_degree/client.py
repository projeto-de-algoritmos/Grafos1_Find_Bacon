import requests

class WikipediaClient(object):
    def __init__(self, max_links_returned=2):
        self.MAX_LINKS_RETURNED = max_links_returned
        self.ARTICLE_NAMESPACE = "0"  # https://en.wikipedia.org/wiki/Wikipedia:Namespace
        self.WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"

    def get_page_links(self, page_title):
        """
        Docs: https://www.mediawiki.org/wiki/API:Links
        """

        formatted_page_title = page_title.replace(" ", "_")

        params = {
            "action": "query",
            "titles": formatted_page_title,
            "format": "json",
            "prop": "links",
            "plnamespace": self.ARTICLE_NAMESPACE,
            "pllimit": self.MAX_LINKS_RETURNED
        }
        r = requests.get(url=self.WIKIPEDIA_API_URL, params=params)
        page_data = r.json()

        page_id_key = list(page_data["query"]["pages"].keys())
        page_id = page_id_key[0]

        if int(page_id) != -1:
            page_links_list = page_data["query"]["pages"][page_id]["links"]
            filtered_pages = [page_link["title"] for page_link in page_links_list]
            return filtered_pages
        else:
            return []
