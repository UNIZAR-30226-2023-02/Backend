from django.shortcuts import render, get_object_or_404
from trivial_web.models import *
from .serializers import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from django.db.models.query_utils import Q





# Minuto 57 -> https://www.youtube.com/watch?v=EscHWLV43NQ
class UsuarioListView(APIView):
    def get(self,request,format=None):
        if Usuario.objects.all().exists():
            queryset = Usuario.objects.all()
            serializer = UsuarioSerializer(queryset,many=True)
            return Response({'usuarios': serializer.data})
        else:
            return Response({'error':'No users found'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class UsuarioDetailView(APIView):
    def get(self,request,username,format=None):
        usuario = get_object_or_404(Usuario,username=username)
        serializer = UsuarioSerializer(usuario)
        return Response({'usuario':serializer.data},status=status.HTTP_200_OK)