class KevinBaconGraph(object):
    def build_graph_from_wikipedia_page(self, page_titles, graph, pages_set, wikipedia_client, count=0):
        for title in page_titles:
            count+=1
            new_page_titles = wikipedia_client.get_page_links(title)
            graph[title] = new_page_titles
            pages_set.update(new_page_titles)

            if count < 6:
                self.build_graph_from_wikipedia_page(new_page_titles, graph, pages_set, wikipedia_client, count)


    def add_nodes_without_connections_to_graph(self, graph, pages_set):
        graph_existing_keys = set(graph.keys())
        keys_not_present_in_graph = pages_set.difference(graph)
        nodes_without_connection = dict.fromkeys(keys_not_present_in_graph, [])
        graph.update(nodes_without_connection)
