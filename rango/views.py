from django.shortcuts import render
from django.http import HttpResponse
from rango.models import Category, Page

def index(request):
    #Get a list of all categories currently stored, first 5, ordered by likes in descending order
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!", "categories": category_list, "pages": page_list}
    
    return render(request, "rango/index.html", context=context_dict)

def about(request):
    context_dict = {"boldmessage": "This tutorial has been put together by Josh McPhail."}
    
    return render(request, "rango/about.html", context = context_dict)

def show_category(request, category_name_slug):
    try:
        #try to find a category name slug with the given name
        category = Category.objects.get(slug = category_name_slug)
        
        #Get associated pages
        pages = Page.objects.filter(category = category)

        context_dict = {"category": category, "pages": pages}
    except Category.DoesNotExist:
        context_dict = {"category": None, "pages": None}
    
    #Render and return to client
    return render(request, "rango/category.html", context = context_dict)