class KevinBaconGraph(object):
    
    # def __init__(self, visited):
    #     self.visited = set() # Set to keep track of visited nodes.


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

    def dfs(self, graph, start, end, path=[], visited=[]):
        if start in visited:
            return path
        path += [start]
        visited += [start]

        if start == end:
            return path
        for edge in graph[start]:
            if edge not in visited:
                return self.dfs(graph,edge,end,path,visited)

    # def dfs_find_node(self, graph, end, visited, path):
    #     start = 'Kevin Bacon'
    #     visited[start] = 1
    #     path.append(start)
    #     print(f"start node {start}")

    #     if start == end:
    #         print(f"this is the path {path}")
    #         return path
    #     else:
    #         print(f"stack {path}")
    #         for node in graph[start]:
    #             print(f" in node - {node}")
    #             if visited[node]== -1 and node != -1 and node != 0 :
    #                 print(f" calling for next recursive funtion {node} ")
    #                 l = dfs_find_node(graph,node,end,visited,path)
    #                 if l is not None:
    #                     return path
    #         po =  path.pop()
    #         print(f" poped last {po}")
    #         visited[start] = -1
    
    # def dfs(self, visited, graph, node):
    #     if node not in visited:
    #         print (node)
    #         visited.add(node)
    #         for neighbour in graph[node]:
    #             dfs(visited, graph, neighbour)