from datetime import datetime

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

from djview.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from djview.models import Category, Page


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
    if not request.method == 'POST':
        form = CategoryForm()
        return render(request, 'add_category.html', {'form': form})

    form = CategoryForm(request.POST)

    if form.is_valid():
        form.save(commit=True)
        return djview_index(request)
    else:
        print form.errors

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
                    'registered': registered}
    return render(request, 'register.html', context_dict)


def user_login(request):
    if not request.method == 'POST':
        return render(request, 'login.html', {})

    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username=username, password=password)

    if not user:
        print 'Bad login credentials {0}:{1}'.format(username, password)
        return HttpResponse('Invalid login details')

    if not user.is_active:
        return HttpResponse('You account is not active')

    login(request, user)

    return HttpResponseRedirect('/djview')


def djview_index(request):
    category_list = Category.objects.all()
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {'categories': category_list,
                    'pages': page_list}

    visits = request.session.get('visits')
    if not visits:
        visits = 1

    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7],
                                            '%Y-%m-%d %H:%M:%S')

        if (datetime.now() - last_visit_time).seconds > 0:
            visits += 1
            reset_last_visit_time = True
    else:
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits

    context_dict['visits'] = visits

    return render(request, 'index.html', context_dict)


def djview_about(request):
    return render(request, 'about.html')


@login_required
def restricted(request):
    return HttpResponse("Since you are logged in, you can see this text")


@login_required
def user_logout(request):
    logout(request)

    return HttpResponse('<a href="/djview/">Index</a>')
