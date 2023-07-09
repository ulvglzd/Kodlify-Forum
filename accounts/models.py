from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .helpers import get_random_hash
from django.template.defaultfilters import slugify
from django.db.models import Q
# Create your models here.

class AccountManager(models.Manager):

    def get_all_accounts_to_invite(self, sender):
        accounts = Account.objects.all().exclude(user=sender)
        account = Account.objects.get(user=sender)
        query = Connection.objects.filter(Q(sender=account) | Q(receiver=account))
        print(query)

        accepted = set([])
        for connect in query:
            if connect.status == 'accepted':
                accepted.add(connect.receiver)
                accepted.add(connect.sender)
        print(accepted)

        available_acc = [account for account in accounts if account not in accepted]
        print(available_acc)
        return available_acc


    def get_all_accounts(self, me):
        accounts = Account.objects.all().exclude(user=me)
        return accounts




class Account(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default="Bio", max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to='avatars/')
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = AccountManager()

    def __str__(self):
        return f"{self.user.username}-{self.created.strftime('%d/%m/%Y')}"


    def get_absolute_url(self):
        return reverse("accounts:account-detail-view", kwargs={"slug": self.slug})

    def getfriends(self):
        return self.friends.all()

    def friends_number(self):
        return self.friends.all().count()

    def get_posts_num(self):
        return self.posts.all().count()

    def get_all_authors_posts(self):
        return self.posts.all()

    def get_ups_given_num(self):
        ups = self.up_set.all()
        total_uped = 0
        for item in ups:
            if item.value=='Up':
                total_uped += 1
        return total_uped

    def get_ups_received_num(self):
        posts = self.posts.all()
        total_uped = 0
        for item in posts:
            total_uped += item.uped.all().count()
        return total_uped





    __initial_first_name = None
    __initial_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initial_first_name = self.first_name
        self.__initial_last_name = self.last_name

    def save(self, *args, **kwargs):
        x = False
        to_slug = self.slug
        if self.first_name != self.__initial_first_name or self.last_name != self.__initial_last_name  or self.slug=="":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) + " " +str(self.last_name))
                x = Account.objects.filter(slug=to_slug).exists()
                while x:
                    to_slug = slugify(to_slug + " " +str(get_random_hash()))
                    x = Account.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
        self.slug = to_slug
        super().save(*args, **kwargs)

STATUS_OPTIONS = (
    ('send', 'send'),
    ('accepted', 'accepted')


)

class ConnectionManager(models.Manager):
    def invite_received(self, receiver):
        query = Connection.objects.filter(receiver=receiver, status='send')
        return query


class Connection(models.Model):
    sender = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='receiver')
    status = models.CharField(max_length=8, choices=STATUS_OPTIONS)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ConnectionManager()

    def __str__(self):
        return f"{self.sender}-{self.receiver}-{self.status}"