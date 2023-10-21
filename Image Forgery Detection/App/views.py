from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.contrib.auth import authenticate,logout,login
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q
from django.contrib.auth.models import User
from .models import userProfile,ifd
# Create your views here.

def homepage(request):
    
    if request.user.is_authenticated:
        profile = userProfile.objects.filter(user = request.user).first()

    else:
        profile = ''
    return render(request,'index.html',context = {'profile':profile})


message = 0
reg_error = 0

def checkSignup(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    
    u = User.objects.filter(username = username).first()
    
    if u == None:
        message = 0
    else:
        message = 1
    
    return JsonResponse({"message":message})

def register(request):
    if request.method == 'POST':
        try:
            user = User.objects.create(username = request.POST.get('username'),email=request.POST.get('email'))
            user.set_password(request.POST.get('password'))
            user.save()
        except:
            pass

        user = User.objects.filter(username=request.POST.get('username')).first()
        
        profile = userProfile.objects.create(user=user)
        profile.phone = request.POST.get('phone')
        profile.address = request.POST.get('address')
        profile.save()
        
            

    return HttpResponseRedirect(reverse('homepage'))


def checkLogin(request):
    
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(username = username,password = password)
    if user:
        print(username)
        return JsonResponse({"message":0})
            
    else:
        print("No user found")
        return JsonResponse({"message":1})
        

def user_login(request):
   
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username = username,password = password)
        if user:

            if user.is_active:
                login(request, user)
                print("login success!!!")
                return HttpResponseRedirect(reverse('homepage'))
        else:
            
            print("No such user")


    return HttpResponseRedirect(reverse('homepage'))
    
@login_required
def user_logout(request):

    logout(request)


    return HttpResponseRedirect(reverse('homepage'))

def show_login(request):
    return render(request,'login.html')

def show_register(request):
    return render(request,'register.html')

import os

def i_f_d(request):
    return render(request,'ifd.html')

try:
    os.chdir('./MantraNet')
except:
    pass
    

import matplotlib.pyplot as plt
import gc

from mantranet import *
import shutil
from pytorch_lightning import Trainer
from django.core.files.storage import FileSystemStorage

def checkImage(request):
    file = request.FILES.get('image')
    fss = FileSystemStorage()
    filename = fss.save(file.name,file)
    url = fss.url(filename)
    print("loaded =============")
    print(os.getcwd())
    
    device='cpu' #to change if you have a GPU with at least 12Go RAM (it will save you a lot of time !)
    model=pre_trained_model(weight_path='./MantraNetv4.pt',device=device)

    model.eval()
    # for image in os.listdir('../Demo_images/'):
    # file_path = str(os.getcwd()).replace('MantraNet',"media")+'\output.png'
    # os.remove(file_path)
    print("file removed !!!!!!!!!!!!!!")
    plt.figure(figsize=(20,20))
    check_forgery(model,img_path=file,device=device)
    plt.savefig("output.png")
    
    original_folder = os.getcwd()
    new_folder = str(os.getcwd()).replace('MantraNet',"media")
    # file_name = "example.txt"
    print("new------",new_folder)
    shutil.move(original_folder + "\output.png", new_folder + '\images\output.png')
    image = ifd.objects.create(image = str(os.getcwd()).replace('MantraNet',"media")+'\output.png')
    image.save()
    print("successsssssssss =============")
    return JsonResponse({"image":str("http://localhost:8000/media/images/output.png")})