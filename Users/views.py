from django.shortcuts import render, redirect, HttpResponse, render
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth  import authenticate,  login, logout
from .models import Post, Reply, Profile, Events, Calendar
from .forms import ProfileForm
from django.contrib.auth.decorators import login_required

from newsapi import NewsApiClient
import pandas as pd
import pycountry_convert as pc
from geopy import Nominatim
from folium.plugins import MarkerCluster

def calendar(request):
    return render(request, 'index.html')

def home(request):
    return render(request, 'home.html')

def forum(request):
    profile = Profile.objects.all()
    if request.method=="POST":   
        user = request.user
        image = request.user.profile.image
        content = request.POST.get('content','')
        post = Post(user1=user, post_content=content, image=image)
        post.save()
        alert = True
        return render(request, "forum.html", {'alert':alert})
    posts = Post.objects.filter().order_by('-timestamp')
    return render(request, "forum.html", {'posts':posts})

def discussion(request, myid):
    post = Post.objects.filter(id=myid).first()
    replies = Reply.objects.filter(post=post)
    if request.method=="POST":
        user = request.user
        image = request.user.profile.image
        desc = request.POST.get('desc','')
        post_id =request.POST.get('post_id','')
        reply = Reply(user = user, reply_content = desc, post=post, image=image)
        reply.save()
        alert = True
        return render(request, "discussion.html", {'alert':alert})
    return render(request, "discussion.html", {'post':post, 'replies':replies})

def UserRegister(request):
    if request.method=="POST":   
        username = request.POST['username']
        email = request.POST['email']
        first_name=request.POST['first_name']
        last_name=request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')
        
        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        return render(request, 'login.html')        
    return render(request, "register.html")

def UserLogin(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/myprofile")
        else:
            messages.error(request, "Invalid Credentials")
        alert = True
        return render(request, 'login.html', {'alert':alert})            
    return render(request, "login.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url = '/login')
def myprofile(request):
    if request.method=="POST":
        user = request.user    
        profile = Profile(user=user)
        profile.save()
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "profile.html", {'obj':obj})
    else:
        form=ProfileForm()
    return render(request, "profile.html", {'form':form})

def contact(request):
    return render(request, 'contact.html')

def news(request):
    newsapi = NewsApiClient(api_key ='637eb7ee1a4e461a9faea9b1335548e3')
    top = newsapi.get_everything(q='tech', sources ='bbc-news',
                                sort_by='relevancy', page=1, page_size=2)
  
    l = top['articles']
    desc = []
    news = []
    img = []
    url = []
  
    for i in range(len(l)):
        f = l[i]
        news.append(f['title'])
        desc.append(f['description'])
        img.append(f['urlToImage'])
        url.append(f['url'])
    mylist = zip(news, desc, img, url)

    top1 = newsapi.get_everything(q='tech', sources ='WIRED',
                                sort_by='relevancy', page=1, page_size=2)
    
    l1 = top1['articles']
    desc1 = []
    news1 = []
    img1 = []
    url1 = []
  
    for j in range(len(l)):
        f1 = l1[j]
        news1.append(f1['title'])
        desc1.append(f1['description'])
        img1.append(f1['urlToImage'])
        url1.append(f1['url'])
    mylist1 = zip(news1, desc1, img1, url1)

    return render(request, 'news.html', context ={"mylist":mylist, "mylist1":mylist1})
    # return render(request, 'news.html')

def events(request):
    title = 'Events'
    events_list = Events.objects.all()
    context = {'title': title, 'events_list': events_list}
    return render(request, 'events.html', context)

def members(request):
    return render(request, 'members.html')

def map(request):
    return render(request, 'map.html')

def archives(request):
    return render(request, 'archives.html')