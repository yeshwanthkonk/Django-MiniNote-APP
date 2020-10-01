from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User, Note
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.response import Response
from .serializers import NoteSerializer, NoteCreateSerializer
from rest_framework import status

# Create your views here.

def home(request):
    if(request.user.is_authenticated):
        return render(request, 'home.html', {'user':request.user.id})
    else:
        return render(request, 'Anonymus_User.html', {})

def logout_view(request):
    logout(request)
    return redirect('/')

def login_view(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username= username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, "login.html", {'note':"Invalid Credentional or User Not exists"})

    else:
        note = request.GET.get('note')
        return render(request, "login.html", {'note': note})


def signup(request):
    if(request.method == 'POST'):
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        if username and password:
            if(User.objects.filter(username = username).exists()):
                return render(request, "signup.html", {'note': "User Already Exists"})
            else:
                User.objects.create_user(username = username, password = password, email = email)
                return redirect("/login/?note=User Succefully Created", note="User Succefully Created")
        else:
            return render(request, "signup.html", {'note': "UserName and Password cann't be empty"})
    else:
        return render(request, "signup.html", {})

# curl -X GET http://localhost:8000/api/v1/note/get -d user=1

class NoteList(RetrieveAPIView):
    queryset = Note.objects.all()
    def get(self, request,format=None):
        print(request.user.id)
        if(request.data.get('user') is None):
            notes = self.queryset.filter(user_id = request.user.id)
        else:
            notes = Note.objects.filter(user_id = request.data.get('user'))
        serializer = NoteSerializer(notes, many=True)
        return Response(serializer.data)
    

class NoteCreateAPI(CreateAPIView):
    serializer_class = NoteCreateSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        if(request.user.id is not None):
            request.data['user'] = request.user.id
        if(request.data.get('user') is not None):
            return super().create(request, *args, **kwargs)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

class NoteDeleteAPI(DestroyAPIView):
    queryset = Note.objects.all()
    lookup_field = 'id'
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

class NoteUpdateAPI(UpdateAPIView):
    serializer_class = NoteCreateSerializer
    queryset = Note.objects.all()
    lookup_field = 'id'
    def put(self, request, *args, **kwargs):
        print(kwargs, request.data)
        return super().update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        print(kwargs, request.data)
        # instance = self.get_object()
        # serializer = self.serializer_class(instance, data=request.data, partial=True)
        # print(repr(serializer))
        # if serializer.is_valid():
        #     serializer.save()
        #     return Response(data=serializer.data)
        # return Response(data="wrong parameters")
        return super().partial_update(request, *args, **kwargs)