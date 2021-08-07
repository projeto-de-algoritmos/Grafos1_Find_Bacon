class KevinBaconGraph(object):
    def build_graph_from_wikipedia_page(self, page_titles, graph, pages_set, wikipedia_client, count=0):
        for title in page_titles:
            count+=1
            new_page_titles = wikipedia_client.get_page_links(title)
            if title in graph:
                already_in_graph = False
                for graph_elem in graph[title]:
                    if graph_elem in new_page_titles:
                        already_in_graph = True
                        new_page_titles.remove(graph_elem)
                        break
            graph[title] = new_page_titles
            pages_set.update(new_page_titles)

            if count < 6:
                self.build_graph_from_wikipedia_page(new_page_titles, graph, pages_set, wikipedia_client, count)


    def add_nodes_without_connections_to_graph(self, graph, pages_set):
        graph_existing_keys = set(graph.keys())
        keys_not_present_in_graph = pages_set.difference(graph)
        nodes_without_connection = dict.fromkeys(keys_not_present_in_graph, [])
        graph.update(nodes_without_connection)

    def parse_graph_to_integer(self, graph):
        integers = {}
        graph_keys_sets = list(graph.keys())
        for i, graph_key in enumerate(graph_keys_sets):
            integers[graph_key] = i

        graph_integer = {}
        for k, v in graph.items():
            graph_integer[integers[k]] = []
            for s in v:
                graph_integer[integers[k]].append(integers[s])
        return graph_integer

    def dfs(self, graph, start, goal):
        stack = [(start, [start])]
        visited = set()
        while stack:
            (vertex, path) = stack.pop()
            if vertex not in visited:
                if vertex == goal:
                    return path
                visited.add(vertex)
                for neighbor in graph[vertex]:
                    stack.append((neighbor, path + [neighbor]))
