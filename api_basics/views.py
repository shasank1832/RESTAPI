from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from rest_framework.parsers import JSONParser
from django.views.decorators.csrf import csrf_exempt

from .models import Article
from .serializers import ArticleSerializers

#for function based api view
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from rest_framework.views import APIView

#for generic api view
from rest_framework import generics
from rest_framework import mixins

#for authentication
from rest_framework.authentication import SessionAuthentication,BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated


#for viewsets
from rest_framework import viewsets
from django.shortcuts import get_object_or_404





# Create your views here.


class ArticleAPIView(APIView):
    def get(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializers(articles,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=ArticleSerializers(data=request.data)
        # print(request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)




@api_view(['GET','PUT','DELETE'])
def article_detail(request,pk,*args,**kwargs):
    try:
        article=Article.objects.get(pk=pk)
    except Article.DoesNotExist:
        return HttpResponse(status=status.HTTP_404_NOT_FOUND) 

    if request.method=='GET':
        serializer =ArticleSerializers(article)
        return Response(serializer.data)

    elif request.method=='PUT':
        serializer=ArticleSerializers(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method=='DELETE':
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ArticleDetails(APIView):
    def get_object(self,id):
        try:
            return Article.objects.get(id=id)
        except Article.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    def get(self,id,request):
        article=self.get_object(id)
        serializer=ArticleSerializers(article)
        return Response(serializer.data)

    def put(self,id,request):
        article=self.get_object(id)
        serializer=ArticleSerializers(article,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(request,id,self):
        article=self.get_object(id)
        article.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    
    # for generic views
class GenericAPIListView(generics.GenericAPIView,mixins.ListModelMixin):
    # authentication_classes=[SessionAuthentication,BasicAuthentication]
    authentication_classes=[TokenAuthentication]

    permission_classes=[IsAuthenticated]

    serializer_class = ArticleSerializers
    queryset=Article.objects.all()

    def get(self,request):
        return self.list(request)

class GenericAPIDetailView(generics.GenericAPIView,mixins.ListModelMixin,
                    mixins.CreateModelMixin,mixins.UpdateModelMixin,
                    mixins.RetrieveModelMixin,mixins.DestroyModelMixin):

                    serializer_class = ArticleSerializers
                    queryset=Article.objects.all()
                    lookup_field='id'

                    authentication_classes=[SessionAuthentication,BasicAuthentication]
                    # authentication_classes=[TokenAuthentication]

                    permission_classes=[IsAuthenticated]

                    
                    def get(self,request,id):
                        return self.retrieve(request)

                    def post(self,request,id):
                        return self.create(request)


                    def put(self,request,id=None):
                        return self.update(request,id)

                    def delete(self,request,id):
                        return self.destroy(request,id)

#for viewsets
class ArticleViewSet(viewsets.ViewSet):
    def list(self,request):
        articles=Article.objects.all()
        serializer=ArticleSerializers(articles,many=True)
        return Response(serializer.data)

    def create(request,self):
        serializer=ArticleSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(request,self,pk=None):
        querset=Article.objects.all()
        article=get_object_or_404(querset,pk=pk)
        serializer=ArticleSerializers(article)
        return Response(serializer.data)
#model viewset

class ArticleModelViewSet(viewsets.ModelViewSet):
    serializer_class=ArticleSerializers
    queryset=Article.objects.all()

        


