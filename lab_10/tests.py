from django.test import TestCase
from django.test import Client
from .csui_helper import get_access_token
from .views import dashboard
from .models import Pengguna, MovieKu

import environ

root = environ.Path(__file__) - 3 # three folder back (/a/b/c/ - 3 = /)
env = environ.Env(DEBUG=(bool, False),)
environ.Env.read_env('sso.env')


# Create your tests here.
class Lab10UnitTest(TestCase):
    def setUp(self):
        self.username = env("SSO_USERNAME")
        self.password = env("SSO_PASSWORD")

    def test_lab_10_url_is_exist(self):
        print("test1")
        response = Client().get('/lab-10/')
        self.assertEqual(response.status_code, 200)

    def test_login_go_to_dashboard_and_logout_sso(self):
        print("test2")
        response = self.client.post('/lab-10/custom_auth/login/',
        {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)

        response = self.client.get('/lab-10/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed('/lab-10/dashboard.html')

        response = self.client.get('/lab-10/dashboard/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed('/lab-10/dashboard.html')

        response = self.client.post('/lab-10/custom_auth/logout/')
        html_response = self.client.get('/lab-10/').content.decode('utf-8')
        self.assertIn("Anda berhasil logout. Semua session Anda sudah dihapus", html_response)

    def test_invalid_get_access_token_raise_exception(self):
        print("test3")
        username = "saya"
        password = "keren"
        with self.assertRaises(Exception) as context:
            get_access_token(username, password)
        self.assertIn("username atau password sso salah", str(context.exception))

    def test_auth_login_failed(self):
        print("test4")
        response = self.client.post('/lab-10/custom_auth/login/', {'username': 'u', 'password': 'p'})
        html_response = self.client.get('/lab-10/').content.decode('utf-8')
        # print (html_response)
        self.assertEqual(response.status_code, 302)
        self.assertIn("Username atau password salah", html_response)

    def test_access_dashboard_without_login(self):
        print("test5")
        response = self.client.get('/lab-10/dashboard/')
        self.assertTemplateUsed('/lab-10/login.html')
        self.assertEqual(response.status_code, 302)

    def test_check_movie_list(self):
        print("test6")
        response = self.client.post('/lab-10/custom_auth/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/list/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/lab-10/movie/list/', {'judul':'Guardians of Galaxy', 'tahun':'2016'})
        self.assertEqual(response.status_code, 200)


    def test_check_movie_details(self):
        print("test7")
        response = self.client.get('/lab-10/movie/detail/tt4984898/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post('/lab-10/custom_auth/login/',
        {'username': self.username, 'password': self.password})

        response = self.client.get('/lab-10/')
        response = self.client.get('/lab-10/dashboard/')

        response = self.client.get('/lab-10/movie/detail/tt4984898/')
        self.assertEqual(response.status_code, 200)

    def test_add_movie_watch_later(self):
        response = self.client.get('/lab-10/movie/watch_later/add/tt3896198/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/add/tt2380307/')
        self.assertEqual(response.status_code, 302)
        #manual adding
        response = self.client.get('/lab-10/movie/watch_later/add/tt3896198/')
        html_response = self.client.get('/lab-10/movie/detail/tt3896198/').content.decode('utf-8')
        self.assertIn("Movie already exist on SESSION! Hacking detected!", html_response)

        #logged in
        response = self.client.post('/lab-10/custom_auth/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/dashboard/')
        self.assertEqual(response.status_code, 200)
        #same as session movie
        response = self.client.get('/lab-10/movie/watch_later/add/tt3896198/')
        self.assertEqual(response.status_code, 302)
        #different movie
        response = self.client.get('/lab-10/movie/watch_later/add/tt2015381/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/add/tt6159030/')
        self.assertEqual(response.status_code, 302)
        #manual adding
        response = self.client.get('/lab-10/movie/watch_later/add/tt2015381/')
        html_response = self.client.get('/lab-10/movie/detail/tt2015381/').content.decode('utf-8')
        self.assertIn("Movie already exist on DATABASE! Hacking detected!", html_response)

    def test_watch_later_movie_page(self):
        #not logged in
        response = self.client.get('/lab-10/movie/watch_later/add/tt3896198/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/add/tt1790809/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/')
        self.assertEqual(response.status_code, 200)

        #logged in
        response = self.client.post('/lab-10/custom_auth/login/', {'username': self.username, 'password': self.password})
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/dashboard/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get('/lab-10/movie/watch_later/add/tt2015381/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/add/tt6342474/')
        self.assertEqual(response.status_code, 302)
        response = self.client.get('/lab-10/movie/watch_later/')
        self.assertEqual(response.status_code, 200)

    def test_api_search_movie(self):
        #init search
        response = Client().get('/lab-10/api/movie/-/-/')
        self.assertEqual(response.status_code, 200)
        #search movie by title
        response = Client().get('/lab-10/api/movie/superman/-/')
        self.assertEqual(response.status_code, 200)
        #search movie by title and year
        response = Client().get('/lab-10/api/movie/superman/2016/')
        self.assertEqual(response.status_code, 200)
        # 0 > number of result <= 3
        response = Client().get('/lab-10/api/movie/Guardians of Galaxy/2016/')
        self.assertEqual(response.status_code, 200)
        #not found
        response = Client().get('/lab-10/api/movie/zabolaza/-/')
        self.assertEqual(response.status_code, 200)
