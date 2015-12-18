from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import generic
from django.contrib.auth import views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Post

class IndexView(generic.ListView):
    template_name = 'blogapp/index.html'
    context_object_name = 'posts'

    def get_queryset(self):
        print(self.request.user.is_authenticated())
        return Post.objects.order_by('-created_at')


@method_decorator(login_required(login_url='/blog/login'), name='dispatch')
class ShowView(generic.DetailView):
    model = Post
    template_name = 'blogapp/show.html'

@login_required(login_url='/blog/login/')
def addComment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.POST['comment'] != '':
        comment = request.POST['comment']
        post.comment_set.create(comment=comment, created_at=timezone.now())
        return HttpResponseRedirect(reverse('blogapp:show', args=(post.id,)))

    return render(request, 'blogapp/showPost.html', {
        'post': post,
        'error_message': "Add a comment.",
    })

def login(request):
    template_response = views.login(request)
    return template_response

def register(request):
    if request.POST:
        errors = {}
        if not request.POST["username"]:
            errors['Username'] = 'Veuillez entrer votre username'
            pass

        if not request.POST["email"]:
            errors['Email'] = 'Veuillez entrer votre email'
            pass

        if not request.POST['password'] or not request.POST['verif']:
            errors['Password'] = 'Veuillez entrer un password et sa verification'
            pass

        if request.POST['password'] != request.POST['verif']:
            errors['Verif'] = 'Les password ne sont pas identiques'
            pass

        if errors:
            return render(request, 'registration/register.html', {'errors': errors})
            pass

        user = User.objects.create_user(request.POST["username"], request.POST['email'], request.POST['password'])
        user.save()
        return HttpResponseRedirect(reverse('blogapp:index'))

    return render(request, 'registration/register.html', {})

@login_required(login_url='/blog/login/')
def newPost(request):
    if request.POST:
        errors = {}

        if not request.POST['content']:
            errors['Content'] = 'Veuillez entrer le contenu du post'
            pass

        if errors:
            return render(request, 'blogapp/newPost.html', {'errors': errors})
            pass

        post = Post(content= request.POST['content'], created_at= timezone.now())
        post.save()

        return HttpResponseRedirect(reverse('blogapp:show', args=(post.id,)))
    return render(request, 'blogapp/newPost.html')
