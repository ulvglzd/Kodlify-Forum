from django.shortcuts import render, redirect
from .models import Post, Up
from django.urls import reverse_lazy
from accounts.models import Account
from .forms import PostModelForm, AnswerModelForm
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.
@login_required
def post_answer_view(request):
    query = Post.objects.all()
    account = Account.objects.get(user=request.user)

    #initial values
    post_form = PostModelForm()
    answer_form = AnswerModelForm ()
    posted = False


   
    
    if 'submit_post' in request.POST:
        print(request.POST)
        post_form = PostModelForm(request.POST, request.FILES)
        if post_form.is_valid():
            instance = post_form.save(commit=False)
            instance.author = account
            instance.save()
            post_form = PostModelForm()
            posted = True

    if 'submit_answer' in request.POST:
        answer_form = AnswerModelForm (request.POST)
        if answer_form.is_valid():
            instance = answer_form.save(commit=False)
            instance.user = account
            instance.post = Post.objects.get(id=request.POST.get('post_id'))
            instance.save()
            answer_form = AnswerModelForm()

    context = {
        'query' : query,
        'account': account,
        'post_form': post_form,
        'answer_form': answer_form,
        'posted': posted,
    }

    return render(request, 'posts/main.html', context)

@login_required
def up_unup_post(request):
    user = request.user
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id=post_id)
        account = Account.objects.get(user=user)

        if account in post_obj.uped.all():
            post_obj.uped.remove(account)
        else:
            post_obj.uped.add(account)
        
        up, created = Up.objects.get_or_create(user=account, post_id=post_id)

        if not created:
            if up.value=='Up':
                up.value='Unup'
            
            else:
                up.value='Up'
        else:
            up.value='Up'

        post_obj.save()
        up.save()

        data = {
            'value': up.value,
            'ups': post_obj.uped.all().count()
        }

        return JsonResponse(data, safe=False)

    return redirect('posts:post-view')


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_delete.html'
    success_url = reverse_lazy('posts:post-view')

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        obj = Post.objects.get(pk=pk)
        if not obj.author.user == self.request.user:
            messages.warning(self.request, 'You need to be the author of the post in order to delete it')
        return obj

class PostUpdate(LoginRequiredMixin, UpdateView):
    form_class = PostModelForm
    model = Post
    template_name = 'posts/update.html'
    success_url = reverse_lazy('posts:post-view')

    def form_valid(self, form):
        account = Account.objects.get(user=self.request.user)
        if form.instance.author == account:
            return super().form_valid(form)
        else:
            form.add_error(None, "You need to be the author of the post in order to update it")
            return super().form_invalid(form)