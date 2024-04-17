from django.contrib.sites import requests
from django.core.serializers import json
import json as des_json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, resolve_url
from django.contrib.auth.models import User
from django.core import serializers

from book_api.models import Book


def get_free_book(request):
    response = dict()

    if request.method == 'GET':
        db_book = Book.objects.filter(occupied=False)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response, safe=False)


def get_occupied_book(request):
    response = dict()

    if request.method == 'GET':
        db_book = Book.objects.filter(occupied=True)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response)


def get_active_book(request):
    response = dict()

    if request.method == 'GET':
        db_book = Book.objects.filter(actve=True)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response)
