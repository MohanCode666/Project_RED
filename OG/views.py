from django.shortcuts import render,redirect
from OG.forms import *
from django.http import HttpResponseRedirect,HttpResponse
from django.core.mail import send_mail
from django.urls import reverse
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.
def base(request):
    return render(request,'base.html')

def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        UT=User.objects.get(username=username)
        PO=Profile.objects.get(username=UT)

        d={'UT':UT,'PO':PO,'username':username}
        return render(request,'home.html',d)
    return render(request,'home.html')
def sign(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            messages.success(request,"Check your Username or Password")
            return redirect('sign')
    
    return render(request,'signin.html')

def reg(request):
    uf=UserForm()
    pf=ProfileForm()
    d={'uf':uf,'pf':pf}
    if request.method=='POST' and request.FILES:
        ud=UserForm(request.POST)
        pd=ProfileForm(request.POST,request.FILES)
        if ud.is_valid() and pd.is_valid():
            uo=ud.save(commit=False)
            sp=ud.cleaned_data['password']
            uo.set_password(sp)
            uo.save()
            po=pd.save(commit=False)
            po.username=uo
            po.save()
            send_mail('Registration',
                    'Ur Registration is Successfull',
                      'ether.mail.django@gmail.com',
                      [uo.email],
                      fail_silently=False)
            
        
            
    return render(request,'register.html',d)

@login_required
def user_logout(request):
    logout(request)
    messages.success(request,"Logged out successfully")
    return redirect('base')
    # return HttpResponseRedirect(reverse('base'))

@login_required
def change_pass(request):
    if request.method=="POST":
        pw=request.POST.get('pw')
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('Changed password')
    return render(request,'change_pass.html')

def forgot(request):
    if request.method=="POST":
        pw1=request.POST.get('pass1')
        pw2=request.POST.get('pass2')
        un=request.POST.get('username')
        if pw1==pw2:
            FO=User.objects.filter(username=un)
            if FO :
                FOO=FO[0]
                FOO.set_password(pw2)
                FOO.save()
                messages.success(request,'Password Reset is DONE')
                return redirect('sign')
    return render(request,'forgot.html')