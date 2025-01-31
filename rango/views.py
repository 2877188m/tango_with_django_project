from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from rango.models import Category, Page, UserProfile
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime

def index(request):
    #Get a list of all categories currently stored, first 5, ordered by likes in descending order
    category_list = Category.objects.order_by("-likes")[:5]
    page_list = Page.objects.order_by("-views")[:5]

    visitor_cookie_handler(request)
    context_dict = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!", "categories": category_list, "pages": page_list}
    
    return render(request, "rango/index.html", context=context_dict)

def about(request):
    visitor_cookie_handler(request)
    context_dict = {"boldmessage": "This tutorial has been put together by Josh McPhail.",
                    "visits": request.session["visits"]}
    
    responce = render(request, "rango/about.html", context = context_dict)
    return responce

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

@login_required
def add_category(request):
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit = True)

            #Redirect user back to the index view
            return redirect(reverse("rango:index"))
        else:
            #Invalid
            print(form.errors)
    # Will handle the bad form, new form, or no form supplied cases.
    return render(request, "rango/add_category.html", {"form": form})

@login_required
def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug = category_name_slug)
    except Category.DoesNotExist:
        category = None
    
    #Redirect is category not existent
    if category is None:
        return redirect(reverse("rango:index"))
    
    form = PageForm()

    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit = False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse("rango:show_category", kwargs = {"category_name_slug": category_name_slug}))
        else:
            print(form.errors)
    #Handling for edge cases
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context = context_dict)

def register(request):
    #View for a user to register
    registered = False #flag

    if request.method == "POST":
        #Grab info from the raw form
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            #Hash the password, then update the object
            user.set_password(user.password)
            user.save()

            #Dont commit profile yet
            profile = profile_form.save(commit = False)
            profile.user = user #set user

            #Search for input image
            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]
            
            #Save, and complete registration
            profile.save()
            registered = True
        else:
            #Invalid, print issues to command
            print(user_form.errors, profile_form.errors)
    else:
        #Not an HTTP POST, render with blank forms
        user_form = UserForm()
        profile_form = UserProfileForm()
    
    #Render with context
    context_dict = {"user_form": user_form, "profile_form": profile_form, "registered": registered}
    return render(request, "rango/register.html", context_dict)

def user_login(request):
    #Login view
    if request.method == "POST":
        #Get the username + password provided, then validate it as a user
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username = username, password = password)

        if user: #If a user was found
            if user.is_active: #If the account is active
                login(request, user)
                return redirect(reverse("rango:index"))
            else:
                return HttpResponse("Your Rango account is disabled.")
        else:
            #User not found
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        #render the page
        return render(request, "rango/login.html")

@login_required
def restricted(request):
    return render(request, "rango/restricted.html")

#Logout view
@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse("rango:index"))

def get_server_side_cookie(request, cookie, default_val = None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    #Helper function
    visits = int(get_server_side_cookie(request, "visits", "1"))
    last_visit_cookie = get_server_side_cookie(request, "last_visit", str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], "%Y-%m-%d %H:%M:%S")

    #If more than a date has elapsed
    if (datetime.now() - last_visit_time).days > 0:
        visits += 1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie

    request.session["visits"] = visits