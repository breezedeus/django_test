from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, resolve_url

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse
from django.template.response import TemplateResponse
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth import (
    login as auth_login,
    logout as auth_logout,
)

from .models import Question, Choice

# def index(request):
#     #return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     #output = r'\n '.join([p.question_text for p in latest_question_list])
#     #return HttpResponse(output)
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls/index.html', context)
#
#
# def detail(request, question_id):
#     #return HttpResponse("You're looking at question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/detail.html', {'question': question})
#
#
# def results(request, question_id):
#     #return HttpResponse("You're looking at the results of question %s." % question_id)
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, 'polls/results.html', {'question': question})
from mysite import settings


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    #return HttpResponse("You're voting on question %s." % question_id)
    p = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))


from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render_to_response


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            return HttpResponseRedirect("/polls")
    else:
        form = UserCreationForm()
    return render(request, "polls/register.html", {'form': form})
    #return render_to_response("polls/register.html", { 'form': form, })


def login(request):
    user = request.user
    if user.is_authenticated():
        return render_to_response("registration/login_success.html",
                                  {'action_name': 'Login', 'username': user.username})

    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user.is_active:
                print(user.username)
                auth_login(request, user)
                #return HttpResponseRedirect("/polls/login_success", {'username': user.username})
                return render_to_response("registration/login_success.html",
                                          {'action_name': 'Login', 'username': user.username})
    else:
        form = AuthenticationForm(request)
    return render(request, "registration/login.html", {'form': form})


def logout(request):
    user = request.user
    auth_logout(request)
    return render_to_response("registration/login_success.html",
                              {'action_name': 'Logout', 'username': user.username})


@sensitive_post_parameters()
@csrf_protect
@never_cache
def login22(request, template_name='registration/login2.html',
          redirect_field_name='registration/login_success.html',
          authentication_form=AuthenticationForm,
          current_app=None, extra_context=None):
    """
    Displays the login form and handles the login action.
    """
    redirect_to = request.POST.get(redirect_field_name,
                                   request.GET.get(redirect_field_name, ''))

    if request.method == "POST":
        form = authentication_form(request, data=request.POST)
        if form.is_valid():

            # Ensure the user-originating redirection url is safe.
            #if not is_safe_url(url=redirect_to, host=request.get_host()):
            #    redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)

            # Okay, security check complete. Log the user in.
            print 'hah1'
            auth_login(request, form.get_user())
            print 'haha2'

            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
        }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)
