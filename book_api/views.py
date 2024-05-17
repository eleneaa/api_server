import math

from django.contrib.sites import requests
from django.core.exceptions import ValidationError
from django.core.serializers import json
import json as des_json
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, resolve_url
from django.contrib.auth.models import User
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from passlib.hash import pbkdf2_sha256

from book_api.models import Book


def get_free_book(request):
    response = dict()

    if request.method == 'GET':
        db_book = Book.objects.filter(occupied=False, last=False, confirmed=False)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response, safe=False)


def get_confirmed_book(request):
    response = dict()
    if request.method == 'POST':
        request_data = des_json.loads(request.body)
        username = request_data.get('username')
        id = request_data.get('book_id')
        description = request_data.get('description')
        number = request_data.get('number')
        book = Book.objects.filter(pk=id).update(user=username, description=description, number=number, occupied=True)
    if request.method == 'GET':
        db_book = Book.objects.filter(occupied=True, confirmed=True, last=False)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response, safe=False)


@csrf_exempt
def get_occupied_book(request):
    response = dict()
    if request.method == 'POST':
        request_data = des_json.loads(request.body)
        username = request_data.get('username')
        id = request_data.get('book_id')
        description = request_data.get('description')
        number = request_data.get('number')
        book = Book.objects.filter(pk=id).update(user=username, description=description, number=number, occupied=True)
    if request.method == 'GET':
        db_book = Book.objects.filter(occupied=True, confirmed=False, last=False)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response, safe=False)


def get_last_book(request):
    response = dict()
    if request.method == 'POST':
        request_data = des_json.loads(request.body)
        username = request_data.get('username')
        id = request_data.get('book_id')
        description = request_data.get('description')
        number = request_data.get('number')
        book = Book.objects.filter(pk=id).update(user=username, description=description, number=number, occupied=True)
    if request.method == 'GET':
        db_book = Book.objects.filter(last=True, occupied=True, confirmed=True)
        response = des_json.loads(serializers.serialize('json', db_book))

    return JsonResponse(response, safe=False)

@csrf_exempt
def get_all_books(request):
    response = dict()
    if request.method == 'GET':
        db_book = Book.objects.all()
        response = des_json.loads(serializers.serialize('json', db_book))
    if request.method == 'POST':
        request_data = des_json.loads(request.body)
        id = request_data.get('id')
        book = Book.objects.filter(pk=id).update(occupied=False, confirmed=False)

    return JsonResponse(response, safe=False)


@csrf_exempt
def authenticate(request):
    if request.method == 'POST':
        # Получение и декодирование данных аутентификации из формата JSON
        request_data = des_json.loads(request.body)
        username = request_data.get('username')
        pswd = request_data.get('password')

        # Логика проверки аутентификации
        if User.objects.filter(username=username).exists():
            user = User.objects.get(username=username)
            if user.check_password(pswd):
                # В случае успешной аутентификации
                return JsonResponse({'message': 'Успешная аутентификация'}, status=200)
            else:
                return JsonResponse({'message': 'Неправильный пароль'}, status=401)
        else:
            # В случае неуспешной аутентификации
            return JsonResponse({'message': 'Ошибка аутентификации'}, status=401)
    else:
        # Логика для обработки GET запроса
        JsonResponse({'message': 'Метод не разрешен'}, status=405)  # Метод не разрешен


@csrf_exempt
def register_user(request):
    try:
        request_data = des_json.loads(request.body)
        user = User.objects.create_user(username=request_data.get('username'), email=request_data.get('email'),
                                        password=request_data.get('password'))
        user.save()
        return JsonResponse({"status": "success", "user_id": user.id}, status=200)
    except ValidationError as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=500)


def get_users(request):
    if request.method == 'GET':
        db_book = User.objects.all()
        response = des_json.loads(serializers.serialize('json', db_book))
        return JsonResponse(response, safe=False)
