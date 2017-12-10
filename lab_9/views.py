from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from .api_enterkomputer import (
    get_drones, get_soundcards, get_opticals
)


response = {}


def index(request):
    '''
    Jika belum login redirect ke login, jika sudah ke profile
    '''

    if 'user_login' in request.session:
        return HttpResponseRedirect(reverse('lab-9:profile'))
    else:
        # clear response cache
        response = {}
        html = 'lab_9/session/login.html'
        return render(request, html, response)


def set_data_for_session(res, request):
    '''
    Menyimpan data-data login pada session
    '''
    response['author'] = request.session['user_login']
    response['access_token'] = request.session['access_token']
    response['kode_identitas'] = request.session['kode_identitas']
    response['role'] = request.session['role']
    response['drones'] = get_drones().json()
    response['soundcards'] = get_soundcards().json()
    response['opticals'] = get_opticals().json()

    response['fav_drones'] = {}
    if 'drones' in request.session.keys():
        response['fav_drones'] = request.session['drones']

    response['fav_soundcards'] = {}
    if 'soundcards' in request.session.keys():
        response['fav_soundcards'] = request.session['soundcards']

    response['fav_opticals'] = {}
    if 'opticals' in request.session.keys():
        response['fav_opticals'] = request.session['opticals']


def profile(request):
    '''
    Views untuk halaman profile
    '''

    # mencegah error, jika url profile langsung diakses
    if 'user_login' not in request.session.keys():
        return HttpResponseRedirect(reverse('lab-9:index'))

    set_data_for_session(response, request)

    html = 'lab_9/session/profile.html'
    return render(request, html, response)

# ======================================================================== #

# Items


def add_session_item(request, key, id):
    # print ("#ADD session item")
    ssn_key = request.session.keys()
    if key not in ssn_key:
        request.session[key] = [id]
    else:
        items = request.session[key]
        if id not in items:
            items.append(id)
            request.session[key] = items

    msg = "Berhasil tambah " + key + " favorite"
    messages.success(request, msg)
    return HttpResponseRedirect(reverse('lab-9:profile'))


def del_session_item(request, key, id):
    # print ("# DEL session item")
    items = request.session[key]
    # print ("before = ", items)
    items.remove(id)
    request.session[key] = items
    # print ("after = ", items)

    msg = "Berhasil hapus item " + key + " dari favorite"
    messages.error(request, msg)
    return HttpResponseRedirect(reverse('lab-9:profile'))


def clear_session_item(request, key):
    if key in request.session:  
        del request.session[key]
        msg = "Berhasil hapus session : favorite " + key
        messages.error(request, msg)
    return HttpResponseRedirect(reverse('lab-9:index'))

# ======================================================================== #
# COOKIES


def cookie_login(request):
    '''
    Login dengan cookie, cek apakah sudah login atau belum
    '''

    # print ("#==> masuk login")
    if is_login(request):
        return HttpResponseRedirect(reverse('lab-9:cookie_profile'))
    else:
        html = 'lab_9/cookie/login.html'
        return render(request, html, response)


def cookie_auth_login(request):
    '''
    Memproses login form dan set cookie jika berhasil
    '''

    if request.method == "POST":
        user_login = request.POST['username']
        user_password = request.POST['password']

        if my_cookie_auth(user_login, user_password):
            res = HttpResponseRedirect(reverse('lab-9:cookie_login'))

            res.set_cookie('user_login', user_login)
            res.set_cookie('user_password', user_password)

            return res
        else:
            msg = "Username atau Password Salah"
            messages.error(request, msg)
            return HttpResponseRedirect(reverse('lab-9:cookie_login'))
    else:
        return HttpResponseRedirect(reverse('lab-9:cookie_login'))


def cookie_profile(request):
    '''
    Menampilkan halaman profile dengan cookie
    '''

    # method ini untuk mencegah error ketika akses URL secara langsung
    if not is_login(request):
        return HttpResponseRedirect(reverse('lab-9:cookie_login'))
    else:
        # print ("cookies => ", request.COOKIES)
        in_uname = request.COOKIES['user_login']
        in_pwd = request.COOKIES['user_password']

        # jika cookie diset secara manual (usaha hacking),
        # distop dengan cara berikut
        # agar bisa masuk kembali, maka hapus secara
        # manual cookies yang sudah diset
        if my_cookie_auth(in_uname, in_pwd):
            html = "lab_9/cookie/profile.html"
            res = render(request, html, response)
            return res
        else:
            # print ("#login dulu")
            msg = "Kamu tidak punya akses :P "
            messages.error(request, msg)
            html = "lab_9/cookie/login.html"
            return render(request, html, response)


def cookie_clear(request):
    '''
    Clear cookie
    '''

    res = HttpResponseRedirect('/lab-9/cookie/login')
    res.delete_cookie('lang')
    res.delete_cookie('user_login')

    msg = "Anda berhasil logout. Cookies direset"
    messages.info(request, msg)
    return res


def my_cookie_auth(in_uname, in_pwd):
    '''
    Authentikasi manual cookie, cek apakah cookie sama
    dengan my_uname dan my_pwd

    '''

    my_uname = "username"  # Ganti dengan USERNAME yang kalian inginkan
    my_pwd = "password"  # Ganti dengan PASSWORD yang kalian inginkan
    return in_uname == my_uname and in_pwd == my_pwd


def is_login(request):
    '''
    Cek apakah sudah login atau belum
    '''
    return ('user_login' in request.COOKIES and
            'user_password' in request.COOKIES)
