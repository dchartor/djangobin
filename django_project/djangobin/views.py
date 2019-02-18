import datetime
from django.shortcuts import render, HttpResponse, redirect, get_object_or_404, reverse, get_list_or_404
from django.conf import settings
from django.contrib import messages
from django.core.mail import mail_admins
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import SnippetForm, ContactForm, CreateUserForm, SettingForm
from .models import Language, Snippet, Tag
from .utils import paginate_result
from .decorators import private_snippet


def index(request):
    if request.method == 'POST':
        f = SnippetForm(request, request.POST)

        if f.is_valid():
            snippet = f.save(request)
            return redirect(reverse('djangobin:snippet_detail', args=[snippet.slug]))

    else:
        f = SnippetForm(request)
    return render(request, 'djangobin/index.html', {'form': f})


@private_snippet
def snippet_detail(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    snippet.hits += 1
    snippet.save()
    return render(request, 'djangobin/snippet_detail.html', {'snippet': snippet})


@private_snippet
def download_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    file_extension = snippet.language.file_extension
    filename = snippet.slug + file_extension
    res = HttpResponse(snippet.original_code)
    res['content-disposition'] = 'attachment; filename=' + filename + ';'
    return res


@private_snippet
def raw_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug = snippet_slug)
    return HttpResponse(snippet.original_code, content_type=snippet.language.mime)


def trending_snippets(request, language_slug=''):
    lang = None
    snippets = Snippet.objects
    if language_slug:
        snippets = snippets.filter(language__slug=language_slug)
        lang = get_object_or_404(Language, slug=language_slug)

    snippet_list = get_list_or_404(snippets.filter(exposure='public').order_by('-hits'))
    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/trending.html', {'snippets': snippets, 'lang': lang})


def tag_list(request, tag):
    t = get_object_or_404(Tag, name=tag)
    snippet_list = get_list_or_404(t.snippet_set)
    snippets = paginate_result(request, snippet_list, 5)
    return render(request, 'djangobin/tag_list.html', {'snippets': snippets, 'tag': t})


def profile(request, username):
    return HttpResponse("<p>Profile page of {}</p>".format(username))


def contact(request):
    if request.method == 'POST':
        f = ContactForm(request.POST, request)
        if f.is_valid():

            if request.user.is_authenticated:
                name = request.POST.get('name', '')
                email = request.POST.get('password', '')
            else:
                name = f.cleaned_data['name']
                email = f.cleaned_data['email']

            subject = "You have a new Feedback from {}:<{}>".format(name, email)

            message = "Purpose: {}\n\nDate: {}\n\nMessage:\n\n {}".format(
                dict(f.purpose_choices).get(f.cleaned_data['purpose']),
                datetime.datetime.now(),
                f.cleaned_data['message']
            )

            mail_admins(subject, message)
            messages.add_message(request, messages.INFO, 'Thanks for submitting your feedback.')

            return redirect('djangobin:contact')

    else:
        f = ContactForm(request)

    return render(request, 'djangobin/contact.html', {'form': f})


def login(request):
    # if request.user.is_authenticated:
    #      return redirect('djangobin:profile', username=request.user.username)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('djangobin:user_details')
        else:
            messages.error(request, 'Error! Wrong username/password.')

    return render(request, 'djangobin/login.html')


@login_required
def logout(request):
    auth.logout(request)
    return render(request, 'djangobin/logout.html')


@login_required
def user_details(request):
    user = get_object_or_404(User, id=request.user.id)
    return render(request, 'djangobin/user_details.html', {'user': user})


def signup(request):
    if request.method == 'POST':
        f = CreateUserForm(request.POST)
        if f.is_valid():
            f.save(request)
            messages.success(request, 'Account created successfully. Check email to verify the account.')
            return redirect('djangobin:signup')

    else:
        f = CreateUserForm()

    return render(request, 'djangobin/signup.html', {'form': f})


def activate_account(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if (user is not None and default_token_generator.check_token(user, token)):
        user.is_active = True
        user.save()
        messages.add_message(request, messages.INFO, 'Account activated. Please login.')
    else:
        messages.add_message(request, messages.INFO, 'Link Expired. Contact admin to activate your account.')

    return redirect('djangobin:login')


@login_required
def settings(request):
    user = get_object_or_404(User, id=request.user.id)
    if request.method == 'POST':
        f = SettingForm(request.POST, instance=user.profile)
        if f.is_valid():
            f.save()
            messages.add_message(request, messages.INFO, 'Settings Saved.')
            return redirect(reverse('djangobin:settings'))

    else:
        f = SettingForm(instance=user.profile)

    return render(request, 'djangobin/settings.html', {'form': f})


def profile(request, username):
    user = get_object_or_404(User, username=username)

    if user.profile.private and request.user.username != user.username:
        raise Http404
    elif not user.profile.private and request.user.username != user.username:
        snippet_list = user.snippet_set.filter(exposure='public')
        user.profile.views += 1
        user.profile.save()
    else:
        snippet_list = user.snippet_set.all()

    snippets = paginate_result(request, snippet_list, 5)

    return render(request, 'djangobin/profile.html', {'user': user, 'snippets': snippets})

@login_required
def delete_snippet(request, snippet_slug):
    snippet = get_object_or_404(Snippet, slug=snippet_slug)
    if not snippet.user == request.user:
        raise Http404
    snippet.delete()
    return redirect('djangobin:profile', request.user)
