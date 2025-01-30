from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm

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

def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            #Redirect user back to the index view
            return redirect("/rango/")
        else:
            #Invalid
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    return render(request, "rango/add_category.html", {"form": form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    #Redirect is category not existent
    if category is None:
        return redirect("/rango/")
    
    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit = True)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_category", kwargs = {"category_name_slug": category_name_slug}))
        else:
            print(form.errors)
    #Handling for edge cases
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context = context_dict)