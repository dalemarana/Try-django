from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import render, redirect

from .forms import ArticleForm
from articles.models import Article
# Create your views here.

from django.views.decorators.http import require_http_methods

def article_search_view(request):
    # print(dir(request))
    # print(request.GET)
    query = request.GET.get("q") # this is a dictionary
    # query = query_dict.get("q") #<input type="text" name="q"/>


        ## Title and Content Lookups using Q
        # lookups = Q(title__icontains=query) | Q(content__icontains=query)
        # qs = Article.objects.filter(lookups)
    qs = Article.objects.search(query=query)
    context = {
        "object_list": qs,
    }
    return render(request, "articles/search.html", context=context)

@login_required
@require_http_methods(["GET", "POST"])
def article_create_view(request):
    form = ArticleForm(request.POST or None)
    # print("post", form)
    context = {
        "form": form
    }
    if form.is_valid():
        article_object = form.save()
        context["form"] = ArticleForm()
        # print(article_object.slug)
        return redirect(article_object.get_absolute_url())
        # OR
        # return redirect("article-detail", slug=article_object.slug)
        ## below can be commented out because of the ModelForm in the forms.py
        # title = form.cleaned_data.get("title")
        # content = form.cleaned_data.get("content")
        # article_object = Article.objects.create(title=title, content=content)
        # context["object"] = article_object
        # context["created"] = True

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

def article_detail_view(request, slug=None):
    article_obj = None
    if slug is not None:
        try:
            article_obj = Article.objects.get(slug=slug)
        # except:
        #     pass
        except Article.DoesNotExist:
            raise Http404
        except Article.MultipleObjectsReturned:
            article_obj = Article.objects.filter(slug=slug).first()
        except:
            raise Http404
    context = {
        "object": article_obj,
    }
    return render(request, "articles/detail.html", context=context)
