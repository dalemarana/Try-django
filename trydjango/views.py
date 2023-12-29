"""
To render html web pages
"""
import random
from django.http import HttpResponse
from django.template.loader import render_to_string, get_template

from articles.models import Article

def home_view(request, *args, **kwargs):
    """
    Take in a request (Django sends request)
    Return HTML as a response (we pick to return the response)
    """
    name = "Dale"
    number_id = random.randint(1,4)

    article_obj = Article.objects.get(id=number_id)
    article_queryset = Article.objects.all()
    my_list = article_queryset


    context = {
        "object_list": article_queryset,
        "object": article_obj,
        "title": article_obj.title,
        "id": article_obj.id,
        "content": article_obj.content
    }

    # Django Templates
    ## using get_template - can be used in the database rendering
    # tmpl = get_template("home-view.html")
    # tmpl_string = tmpl.render(context=context)

    HTML_STRING = render_to_string("home-view.html", context=context)

    # HTML_STRING = """
    # <h1>{title} (id: {id})!</h1>
    # <h1>{content}</h1>
    # """.format(**context)

    return HttpResponse(HTML_STRING)