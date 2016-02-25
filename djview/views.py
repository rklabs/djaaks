from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import redirect
from djview.models import Category
from djview.models import Page
from djview.forms import CategoryForm
from djview.forms import PageForm
from djview.forms import UserForm
from djview.forms import UserProfileForm

def category(request, category_name_slug):
    context_dict = {}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        
        pages = Page.objects.filter(category=category)
        context_dict['pages'] = pages

        context_dict['category'] = category
        context_dict['category_name_slug'] = category_name_slug
    except Category.DoesNotExist:
        pass

    return render(request, 'category.html', context_dict)

def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        
        if form.is_valid():
            form.save(commit=True)
            return djview_index(request)
        else:
            print form.errors
    else:
        form = CategoryForm()

    return render(request, 'add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        cat = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        cat = None

    if request.method == 'POST':
        form = PageForm(request.POST)
        
        if form.is_valid():
            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.views = 0
                page.save()
                return redirect('djview_index')
        else:
            print form.errors
    else:   
        form = PageForm()

    context_dict = {'form': form, 'category': cat}

    return render(request, 'add_page.html', context_dict)

def register(request):
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)
        
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']
        
            profile.save()
        
            registered = True

        else:
            print user_form.errors
            print profile_form.errors
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    context_dict = {'user_form': user_form,
                    'profile_form': profile_form,
                    'registered': registered }
    return render(request, 'register.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        
        if not user:
            print 'Back login credentials {0}:{1}'.format(username, password)
            return HttpResponse('Invalid login details')

        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/djview')
        else:
            return HttpResponse('You account is not active')

    else:
        return render(request, 'login.html', {})    
    
def djview_index(request):
    category_list = Category.objects.all()
    context_dict = {'categories': category_list}

    return render(request, 'index.html', context_dict)

def djview_about(request):
    return HttpResponse('About djview <br /> <a href="/djview">Index</a>')
