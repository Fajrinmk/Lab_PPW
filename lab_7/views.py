from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

from .models import Friend
from .api_csui_helper.csui_helper import CSUIhelper
import os
import json

response = {}
csui_helper = CSUIhelper()

def index(request):
    # Page halaman menampilkan list mahasiswa yang ada
    # TODO berikan akses token dari backend dengan menggunakaan helper yang ada

    mahasiswa_list = csui_helper.instance.get_mahasiswa_list()

    friend_list = Friend.objects.all()
    response = {"mahasiswa_list": mahasiswa_list, "friend_list": friend_list}
    html = 'lab_7/lab_7.html'
    return render(request, html, response)

def friend_list(request):
    html = 'lab_7/daftar_teman.html'
    response['friend_list'] = Friend.objects.all().order_by('npm')
    return render(request, html, response)

def get_friend_list(request):
    if(request.method == 'GET'):
        friend_list = []
        for i in Friend.objects.all().order_by('npm'):
            friend_list.append(model_to_dict(i))

        return JsonResponse({'status_code':200, 'friends':friend_list})
    raise Http404
    

@csrf_exempt
def add_friend(request):
    if request.method == 'POST':
        name = request.POST['name']
        npm = request.POST['npm']
        friend = Friend(friend_name=name, npm=npm)
        friend.save()
        data = model_to_dict(friend)
        return HttpResponse(data)

def delete_friend(request, friend_id):
    Friend.objects.filter(id=friend_id).delete()
    return HttpResponseRedirect('/lab-7/')

@csrf_exempt
def validate_npm(request):
    npm = request.POST.get('npm', None)
    data = {
        'is_taken': True #lakukan pengecekan apakah Friend dgn npm tsb sudah ada
    }
    return JsonResponse(data)

def model_to_dict(obj):
    data = serializers.serialize('json', [obj,])
    struct = json.loads(data)
    data = json.dumps(struct[0]["fields"])
    return data
