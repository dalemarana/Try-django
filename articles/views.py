from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .forms import ArticleForm
from articles.models import Article
# Create your views here.

from django.views.decorators.http import require_http_methods

def article_search_view(request):
    # print(dir(request))
    print(request.GET)
    query_dict = request.GET # this is a dictionary
    # query = query_dict.get("q") #<input type="text" name="q"/>
    try:
        query = int(query_dict.get("q"))
    except:
        query = None
    article_obj = None
    if query is not None:
        article_obj = Article.objects.get(id=query)
    context = {
        "object": article_obj,
    }
    return render(request, "articles/search.html", context=context)

@login_required
@require_http_methods(["GET", "POST"])
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        article_object = form.save()
        context["form"] = ArticleForm()
        ## below can be commented out because of the ModelForm in the forms.py
        # title = form.cleaned_data.get("title")
        # content = form.cleaned_data.get("content")
        # article_object = Article.objects.create(title=title, content=content)
        context["object"] = article_object
        context["created"] = True

    return render(request, "articles/create.html", context=context)

## OLD CODE
# def article_create_view(request):
#     # print(request.POST)
#     form = ArticleForm()
#     context = {
#         "form": form
#     }
#     if request.method == "POST":
#         form = ArticleForm(request.POST)
#         context["form"] = form
#         if form.is_valid(): # checking if data is clean
#             title = form.cleaned_data.get("title")
#             content = form.cleaned_data.get("content")
#             # print(title, content)
#             article_object = Article.objects.create(title=title, content=content)
#             context["object"] = article_object
#             context["created"] = True
#     return render(request, "articles/create.html", context=context)

def article_detail_view(request, id=None):
    article_obj = None
    if id is not None:
        article_obj = Article.objects.get(id=id)
    context = {
        "object": article_obj,
    }
    return render(request, "articles/detail.html", context=context)
