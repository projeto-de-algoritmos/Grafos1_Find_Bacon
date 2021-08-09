from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils.http import urlencode
from django.shortcuts import redirect, reverse
from urllib.parse import quote_plus, quote

from kevin_degree.forms import SearchGraphForm
from kevin_degree.models import Graph
from kevin_degree.graph import KevinBaconGraph


def index(request):
    return HttpResponse("It's working!!!")

def search_from_kevin_bacon_wikipedia_page(request):
    if request.method == "POST":
        form = SearchGraphForm(request.POST)
        if form.is_valid():
            encoded = urlencode({'search':form.cleaned_data['search']})
            decoded = quote_plus(form.cleaned_data["search"])
            print(
                f'{form.cleaned_data["search"]} ENCODED: {encoded} \n DECODED {decoded}'
            )
            return redirect(
                reverse(
                    'search_result',
                    args=(form.cleaned_data["search"],)
                )
            )
    else:
        form = SearchGraphForm()
    return render(request, 'search_from_kevin_bacon_wikipedia_page.html', {'form': form})

def page_search_result(request, page):
    g = Graph.objects.all().first()
    if not g:
        return HttpResponse('Carregue um grafo na base de dados')
    else:
        graph = g.json_graph
        if page not in graph:
            return HttpResponse(f'A página "<strong>{page}</strong>" não está no grafo do Kevin Bacon : (')
        else:
            kevin_bacon_graph = KevinBaconGraph()
            path = kevin_bacon_graph.dfs(graph, 'Kevin Bacon', page)
            if not path:
                return HttpResponse(f'Não existe um caminho com no mínimo 6 links a partir da página do Kevin Bacon para a página {page}')
            else:
                str_path = ' -> '.join([p for p in path])
                return HttpResponse(str_path)

def available_pages(request):
    if request.method == 'GET':

        g = Graph.objects.all().first()
        if not g:
            return HttpResponse('Carregue um grafo na base de dados')
        else:
            graph = g.json_graph
            pages = list(graph.keys())
            return render(request, 'kevin_bacon_graph_pages.html', {'pages': pages})
    else:
        return HttpResponseNotAllowed('Method not allowed')