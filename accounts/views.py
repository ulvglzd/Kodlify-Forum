from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Connection
from .forms import AccountModelForm
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.

@login_required
def my_account_view(request):
    account = Account.objects.get(user=request.user)
    form = AccountModelForm(request.POST or None, request.FILES or None, instance=account)
    approve = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            approve = True

    context = {
        'account': account,
        'form': form,
        'approve': approve,
    }

    return render(request, 'accounts/myaccount.html', context)

@login_required
def invite_received_view(request):
    account = Account.objects.get(user=request.user)
    query = Connection.objects.invite_received(account)
    invitations = list(map(lambda x: x.sender, query))
    is_empty = False
    if len(invitations) == 0:
        is_empty = True

    context = {
        'query': invitations,
        'is_empty': is_empty,
        }

    return render(request, 'accounts/my_invitations.html', context)

@login_required
def confirm_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('account_pk')
        sender = Account.objects.get(pk=pk)
        receiver = Account.objects.get(user=request.user)
        connect = get_object_or_404(Connection, sender=sender, receiver=receiver)
        if connect.status == 'send':
            connect.status = 'accepted'
            connect.save()
    return redirect('accounts:my-invitations-view')

@login_required
def decline_invitation(request):
    if request.method == "POST":
        pk = request.POST.get('account_pk')
        sender = Account.objects.get(pk=pk)
        receiver = Account.objects.get(user=request.user)
        connect = get_object_or_404(Connection, sender=sender, receiver=receiver)
        connect.delete()
    return redirect('accounts:my-invitations-view')



@login_required
def accounts_list_view(request):
    user = request.user
    query = Account.objects.get_all_accounts(user)

    context = {'query': query}

    return render(request, 'accounts/account_list.html', context)


class AccountDetailView(LoginRequiredMixin, DetailView):
    model= Account
    template_name = 'accounts/detail.html'

    # def get_object(self, **kwargs):
    #     slug = self.kwargs.get('slug')
    #     account = Account.objects.get(slug=slug)
    #     return account

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        account = Account.objects.get(user=user)
        con_rec = Connection.objects.filter(sender=account)
        con_sen = Connection.objects.filter(receiver=account)
        con_receiver = []
        con_sender = []
        for i in con_rec:
            con_receiver.append(i.receiver.user)
        for i in con_sen:
            con_sender.append(i.sender.user)
        context["con_receiver"] = con_receiver
        context["con_sender"] = con_sender
        context['posts'] = self.get_object().get_all_authors_posts()
        context['len_posts'] = True if len(self.get_object().get_all_authors_posts()) > 0 else False
        
        return context

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    # context_object_name = 'query'

    def get_queryset(self):
        query = Account.objects.get_all_accounts(self.request.user)
        return query

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        account = Account.objects.get(user=user)
        con_rec = Connection.objects.filter(sender=account)
        con_sen = Connection.objects.filter(receiver=account)
        con_receiver = []
        con_sender = []
        for i in con_rec:
            con_receiver.append(i.receiver.user)
        for i in con_sen:
            con_sender.append(i.sender.user)
        context["con_receiver"] = con_receiver
        context["con_sender"] = con_sender
        context['is_empty'] = False
        if len(self.get_queryset()) == 0:
            context['is_empty'] = True

        return context

@login_required
def send_invitation(request):
    if request.method == 'POST':
        pk = request.POST.get('account_pk')
        user = request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)

        connect = Connection.objects.create(sender=sender, receiver=receiver, status='send')

        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('accounts:my-account-view')

@login_required
def remove_connection(request):
    if request.method == 'POST':
        pk = request.POST.get('account_pk')
        user = request.user
        sender = Account.objects.get(user=user)
        receiver = Account.objects.get(pk=pk)

        connect = Connection.objects.get((Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender)))
        connect.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('accounts:my-account-view')



