from django.http import Http404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Meme, Detail
from .serializers import MemeSerializer, DetailSerializer, PropertySerializer


class MemeInfo(APIView):
    def post(self, request):
        meme = request.data
        serializer = MemeSerializer(data=meme)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemeProperty(APIView):
    def post(self, request, meme):
        prop = request.data
        prop["meme"] = meme

        serializer = PropertySerializer(data=prop)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemeList(APIView):
    def get(self, request, phase):
        memes = Meme.objects.filter(phase=phase)
        serializer = MemeSerializer(memes, many=True)
        return Response(serializer.data)


class MemeDetail(APIView):
    def get(self, request, id):
        try:
            meme = Meme.objects.get(pk=id)
            serializer = MemeSerializer(meme)
            return Response(serializer.data)
        except Meme.DoesNotExist:
            raise Http404


class MemeDetails(APIView):
    def get(self, request, meme):
        details = Detail.objects.filter(meme=meme).order_by('id')
        serializer = DetailSerializer(details, many=True)
        return Response(serializer.data)

    def post(self, request, meme):
        detail = request.data
        detail['meme'] = meme
        serializer = DetailSerializer(data=detail)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, meme):
        details = Detail.objects.filter(meme=meme)
        details.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
