from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.forms import ModelForm
from login.models import blogpage, comment

class blogform(ModelForm):
    class Meta:
        model = blogpage
        fields = ['title','body']

def loginorsignup(request):
    c = {}
    c.update(csrf(request))
    return render_to_response('login/signing.html',c)

def signoutview(request):
    logout(request)
    return HttpResponseRedirect('/blogapp/home/')


def checkuser(request):
    
    if 'signup' in request.POST:
        blogusername= request.POST.get('signupuser')
        bloguserpassword= request.POST.get('signuppassword')
        User.objects.create_user(username= blogusername, password= bloguserpassword)
        user = authenticate(username= blogusername, password= bloguserpassword)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/blogapp/userpage/')

    elif 'signin' in request.POST:
        blogusername= request.POST.get('signinuser')
        bloguserpassword= request.POST.get('signinpassword')
        user = authenticate(username= blogusername, password= bloguserpassword)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/blogapp/userpage/')
        else:
            return HttpResponse("incorrect username or password")


def userpage(request):
    
    bloglist = blogpage.objects.all()
    return render_to_response('login/userpage.html', {'username': request.user, 'bloglist': bloglist})
    
def createblogview(request):
    if request.method == 'POST':
        form = blogform(request.POST)
        if form.is_valid():
            b = blogpage(author= request.user, title= form.cleaned_data['title'] , body= form.cleaned_data['body'])
            b.save()
            return render(request, 'login/blogpage.html', {'username': request.user, 'blog': b})
        else:
            return render(request, 'login/createblog.html', {'username': request.user, 'form': form})
    
    else:
        form = blogform()
        return render(request, 'login/createblog.html', {'username': request.user, 'form': form})


def blogpageview(request, blogid):
    
    getblog = blogpage.objects.get(pk=int(blogid))
    getcomment = comment.objects.filter(blog=getblog)
    return render(request, 'login/blogpage.html', {'username': request.user, 'blog': getblog, 'commentlist': getcomment})


def editblogpageview(request):
    if request.method == 'POST':
        if 'editblog' in request.POST:
            blid = request.POST.get('blogid')
            getblog = blogpage.objects.get(pk=int(blid))
            form = blogform(instance= getblog)
            return render(request, 'login/editblog.html', {'username': request.user, 'form': form, 'blogid': blid})
        
        if 'deleteblog' in request.POST:
            blid = request.POST.get('blogid')
            getblog = blogpage.objects.get(pk=int(blid))
            getblog.delete()
            return HttpResponseRedirect('/blogapp/userpage/')

def updateblogview(request):
    if request.method == 'POST':
        form = blogform(request.POST)
        if form.is_valid():
            blid = request.POST.get('blogid')
            b = blogpage.objects.get(pk=int(blid))
            b.title = form.cleaned_data['title']
            b.body = form.cleaned_data['body']
            b.save()
            getcomment = comment.objects.filter(blog=b)
            return render(request, 'login/blogpage.html', {'username': request.user, 'blog': b, 'commentlist': getcomment})

def addcommentview(request):
    if request.method == 'POST':
        blid = request.POST.get('blogid')
        getblog = blogpage.objects.get(pk=int(blid))
        c = comment(author= request.user, body= request.POST.get('commentbox'), blog=getblog)
        c.save()
        return HttpResponseRedirect('/blogapp/blogpageview/'+blid+'/')
        
