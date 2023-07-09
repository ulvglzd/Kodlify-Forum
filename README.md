# Kodlify
## A local forum website where users can find solutions to their technical questions

### Video Demo:  <https://www.youtube.com/watch?v=LawmxaThN6U>

#### Project Description:
Recently, I noticed that there are so many programming groups and communities on facebook and telegram where people ask coding questions.
Most of them cannot use stackoverflow and other identical discussion forums because of lacking english language skills.
So I decided to create a forum website to gather all of the groups and communities in one place.
I created a forum website for azerbaijani coding community where users can register, login, ask questions (posts), answer questions, up(like) posts, make connections, manage their account and etc.



#### Technologies used and application structure

I used Python 3.10, Django, SQLite3, a bit of Javascript, HTML, CSS, Semantic UI.

The project is mainly based on 2 applications in which there are 5 models namely Account, Connection, Post, Answer, Up.
1. Accounts
    - Account
    - Connection

2. Posts
    - Post
    - Answer
    - Up

The last one is Django allauth which is a third-party package of Django framework used for registration and authentication.

Each user should have his/her account to use the website. Whenever a user is created in database, an account of this user will also be generated using Django signals and stored in Account model. Account model consists of 10 fields. This model also contains a number of methods to determine the number of connections, the number of posts (questions), number of ups given and received and so on.
The connection model is created to manage connections between users whose fields are sender, receiver, status of the connection (accepted, declined or pending) and the time when it is created and updated.
In account app, I created a set of views (you can read about view <https://docs.djangoproject.com/en/4.1/topics/http/views/>) in views.py to return the http responses like html templates. For example, my_account_view is created to return the account page of the user signed in, to access the account model forum created in forms.py using forms library of Django and handles the logic to save any changes to account and at the end returns myaccount.html by render function of django.shortcuts package.
Admin.py file is used to register the models created in Accounts app while helpers.py contain the function which returns unique slug or hash for a user identification. urls.py file contains the registered urls where requests initially comes to and then goes to corresponding function in views.py.
In templates directory, I stored the html files of various pages all which extends from the base.html that is located in templates of BASE_DIR (src).

Another application is Posts of which structure is identical to Accounts where admin, models, forms, views, urls are present.

Post model of Posts application is created to manage questions (posts) asked by users. It contains the following fields: content, image, uped (status of wheather it is uped or not), author of question and again time.
Answer model is created to manage answers (comments) to questions (posts). It contains user, post, body and time fields. I used Froms class of Django to allow users to submit answers to questions. In forms.py file I created PostModelForm and AnswerModelForm where certain fields is selected to be displayed. For example, I only chose to display the body of Answer model in AnswerModelForm.
Up model is created to manage ups give to posts which resemble the common 'liking' activity. There is predefined tuple UP_CHOICES which is used to store up and unup values.




