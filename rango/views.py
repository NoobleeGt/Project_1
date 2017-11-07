from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Page
from .forms import CategoryForm, PageForm, UserForm, UserProfileForm
from datetime import datetime


def about(request):
    visitor_cookie_handler(request)
    context_dict = {
        'myName': 'NoobleeGt',
        'visits': request.session['visits']
    }
    return render(request, 'rango/about.html', context_dict)


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    visitor_cookie_handler(request)
    context_dict = {
        'categories': category_list,
        'pages': page_list,
        'visits': request.session['visits']
    }
    return render(request, 'rango/index.html', context_dict)


@login_required
def add_category(request):
    form = CategoryForm
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save(commit=True)
            return redirect('rango:index')
        else:
            print(form.errors)
    return render(request, 'rango/add_category.html', {'form': form})


def show_category(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    print(category, category_name_slug)
    pages = Page.objects.filter(category=category)
    context_dict = {
        'category': category,
        'pages': pages
    }
    return render(request, 'rango/category.html', context_dict)


@login_required
def add_page(request, category_name_slug):
    category = get_object_or_404(Category, slug=category_name_slug)
    form = PageForm()
    if request.method == 'POST':
        form = PageForm(request.POST)
        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect('rango:show_category',
                            category_name_slug=category.slug)
        else:
            print(form.errors)
    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context_dict)


# def register(request):
#     registered = False
#     if request.method == 'POST':
#         user_form = UserForm(request.POST)
#         profile_form = UserProfileForm(request.POST)
#
#         if user_form.is_valid() and profile_form.is_valid():
#             user = user_form.save()
#             user.set_password(user.password)
#             user.save()
#
#             profile = profile_form.save(commit=False)
#             profile.user = user
#
#             if 'picture' in request.FILES:
#                 profile.picture = request.FILES['picture']
#
#             profile.save()
#             registered = True
#         else:
#             print(user_form.errors, profile_form.errors)
#     else:
#         user_form = UserForm()
#         profile_form = UserProfileForm()
#
#     context_dict = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'registered': registered
#     }
#     return render(request, 'rango/register.html', context_dict)
#
#
# def user_login(request):
#     context_dict = {}
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#
#         user = authenticate(username=username, password=password)
#
#         if user:
#             if user.is_active:
#                 login(request, user)
#                 return redirect('rango:index')
#             else:
#                 context_dict['disabled'] = True
#                 return render(request, 'rango/login.html', context_dict)
#         else:
#             print('Invalid login details: {0}, {1}'.format(username, password))
#             context_dict['invalid'] = True
#             return render(request, 'rango/login.html', context_dict)
#     else:
#         return render(request, 'rango/login.html', context_dict)
#
#
# @login_required
# def user_logout(request):
#     logout(request)
#     return redirect('index')
#

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')


# ----------------------------------------------------------------------- #


def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


def visitor_cookie_handler(request):
    visits = int(get_server_side_cookie(request, 'visits', 1))

    last_visit_cookie = get_server_side_cookie(request,
                                               'last_visit',
                                               str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],
                                        '%Y-%m-%d %H:%M:%S')

    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        request.session['last_visit'] = str(datetime.now())
    else:
        visits = 1
        request.session['last_visit'] = last_visit_cookie

    request.session['visits'] = visits
