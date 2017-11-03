from django.shortcuts import render, redirect, get_object_or_404
from .models import Category, Page
from .forms import CategoryForm, PageForm


def about(request):
    context = {'myName': 'NoobleeGt'}
    return render(request, 'rango/about.html', context)


def index(request):
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    context_dict = {
        'categories': category_list,
        'pages': page_list
    }
    return render(request, 'rango/index.html', context_dict)


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
