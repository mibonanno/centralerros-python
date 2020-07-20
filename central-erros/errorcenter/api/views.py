from django.shortcuts import render, redirect, render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm

from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView
from django.views.generic.edit import DeleteView, UpdateView

from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView

from .forms import UserModelForm

from .models import Log, Origin, Environment, Level
from .serializers import (LogSerializer, 
                          OriginSerializer, 
                          UserSerializer, 
                          EnvironmentSerializer,
                          LevelSerializer)
from .api_permissions import OnlyAdminCanList

from errorcenter.forms import SignUpForm

class LogApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

class LogsList(ListView):
    # Belong's to which model.
    model = Log
    queryset = Log.objects.filter(active=True)
    # Specify the static display template file.
    template_name = 'logs/new_list.html'   
    
    # Custom defined context object value, this can override default context object value.
    context_object_name = 'logs'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super(LogsList, self).get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['environments'] = Environment.objects.all()
        return context

class LevelsList(ListView):
    # Belong's to which model.
    model = Level
    queryset = Level.objects.all()
    
    # Custom defined context object value, this can override default context object value.
    context_object_name = 'levels'  

class OriginsList(ListView):
    # Belong's to which model.
    model = Origin
    queryset = Origin.objects.all()
    # Specify the static display template file.
    template_name = 'logs/new_list.html'   
    
    # Custom defined context object value, this can override default context object value.
    context_object_name = 'origins'  

class LogArchive(UpdateView):
    model = Log
    template_name = 'logs/log_confirm_archive.html'
    # Allow edit fields.
    fields = ['active']   
    success_url = reverse_lazy('logs')

class LogDelete(DeleteView):
    model = Log
    template_name = 'logs/log_confirm_delete.html'
    success_url = reverse_lazy('logs')

@csrf_exempt
class LogDeleteList(ListView):
    model = Log

    def get(self, request, *args, **kwargs):
        logs_ids=list(map(int, self.request.POST.getlist('checkboxes')))
        self.Log.objects.filter(id__in=logs_ids).delete()
        queryset = Log.objects.all()
        serializer = LogSerializer(queryset, many=True)
        context_object_name = 'environments'  

        return Response(serializer.data)

    template_name = 'logs/log_confirm_delete.html'
    success_url = reverse_lazy('logs')

class SingleLogView(RetrieveAPIView):
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'logs/list.html'

class OriginApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Origin.objects.all()
    serializer_class = OriginSerializer

class LevelApiViewSet(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer

class EnvironmentListOnlyApiView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    model = Environment
    queryset = Environment.objects.all()
    serializer = EnvironmentSerializer(queryset, many=True)
    context_object_name = 'environments'  
    
    
class UserApiViewSet(viewsets.ModelViewSet):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, OnlyAdminCanList]

    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserToken(APIView):

    def post(self, request):

        email = request['email']
        password = request['senha']
        
        if email is None or password is None:
            return Response({'error': 'Please provide both email and password'},
                            status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username=email, password=password)
        
        if not user:
            return Response({'error': 'Invalid Credentials'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        token, _ = Token.objects.get_or_create(user=user)
       
        return Response({'token': token.key}, status=status.HTTP_200_OK)

    def user_login(request):
        if  request.method == 'POST':

            response = UserToken.post(request.POST, request.POST)
            status = response.status_code

            if (status != 200):
                return render(request, 'registration/login.html', {'error': response.data['error']})
            else:
                return redirect('/logs', {'token': response.data['token']})
        else:
            form = UserModelForm()

        context = {
            'form': form
        }
        return render(request, 'registration/login.html', {'form': form})

def SignUp(request):
     if request.method == 'POST':
         form = SignUpForm(request.POST)
         if form.is_valid():
             form.save()
             return redirect('/api')
     else:
         form = SignUpForm()

         args = {'form': form}
         return render(request, 'api/signup.html', args)
