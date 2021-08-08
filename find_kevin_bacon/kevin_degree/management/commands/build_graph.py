import json
from kevin_degree.client import WikipediaClient
from kevin_degree.graph import KevinBaconGraph
from django.core.management.base import BaseCommand
from kevin_degree.models import Graph


class Command(BaseCommand):
    help = 'Build graph from wikipedia page links using Kevin Bacon as starting node'

    def add_arguments(self, parser):
        parser.add_argument("--qty-links", type=int,
                            help="number of links to be searched within a page")

    def handle(self, *args, **kwargs):
        qty_links = kwargs["qty_links"] if "qty_links" in kwargs else 2

        wikipedia_client = WikipediaClient(max_links_returned=qty_links)
        kevin_bacon_page_links = wikipedia_client.get_page_links("Kevin Bacon")
        graph = {
            "Kevin Bacon": kevin_bacon_page_links
        }
        pages_set = set()

        kevin_bacon_graph = KevinBaconGraph()
        kevin_bacon_graph.build_graph_from_wikipedia_page(
            kevin_bacon_page_links, graph, pages_set, wikipedia_client)
        kevin_bacon_graph.add_nodes_without_connections_to_graph(
            graph, pages_set)
        Graph.objects.create(json_graph=graph)

        #graph_integer = kevin_bacon_graph.parse_graph_to_integer(graph)

        #start = 0 # 0 represents Kevin Bacon wikipedia page
        #goal = 3
        #path = kevin_bacon_graph.dfs(graph_integer, start, goal)

        #print(f'PATH: {path}')
