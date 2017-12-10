from django.test import TestCase, Client
from .api_enterkomputer import (
    get_drones, get_soundcards, get_opticals
)
import base64
import os


class Lab9UnitTest(TestCase):

    def test_lab_9_url_exist(self):
        response = Client().get('/lab-9/')
        self.assertEqual(response.status_code, 200)

    def test_session_access_profile_directly_fail(self):
        response = Client().get('/lab-9/profile/')
        self.assertEqual(response.status_code, 302)

    def test_session_login_with_get_fail(self):
        response = Client().get('/lab-9/custom_auth/login/')
        self.assertEqual(response.status_code, 302)

    def test_session_login_wrong_username(self):
        data = {
            'username': 'username',
            'password': 'password'
        }
        response = Client().post('/lab-9/custom_auth/login/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_session(self):
        data = {
            'username': os.environ.get('SSO_USERNAME'),
            'password': os.environ.get('SSO_PASSWORD'),
			}
        client = Client()

        # llgin
        response = client.post(
            '/lab-9/custom_auth/login/', data=data, follow=True)

        self.assertEqual(response.status_code, 200)

        drone = get_drones().json()
        soundcard = get_soundcards().json()
        optical = get_opticals().json()

        # add items
        response = client.get(
            '/lab-9/add_session_item/drones/{}/'.format(drone[0]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/add_session_item/soundcards/{}/'.format(
                soundcard[0]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/add_session_item/opticals/{}/'.format(optical[0]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        # another items
        response = client.get(
            '/lab-9/add_session_item/drones/{}/'.format(drone[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/add_session_item/soundcards/{}/'.format(
                soundcard[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/add_session_item/opticals/{}/'.format(optical[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        # delete items
        response = client.get(
            '/lab-9/del_session_item/drones/{}/'.format(drone[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/del_session_item/soundcards/{}/'.format(
                soundcard[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/del_session_item/opticals/{}/'.format(optical[1]['id']),
            follow=True)
        self.assertEqual(response.status_code, 200)

        # clear items
        response = client.get(
            '/lab-9/clear_session_item/drones/', follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/clear_session_item/soundcards/', follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get(
            '/lab-9/clear_session_item/opticals/', follow=True)
        self.assertEqual(response.status_code, 200)

        # logout
        response = client.post(
            '/lab-9/custom_auth/logout/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_cookie_login_fail(self):
        response = Client().get('/lab-9/cookie/login/')
        self.assertEqual(response.status_code, 200)

    def test_cookie_access_profile_directly_fail(self):
        response = Client().get('/lab-9/cookie/profile/')
        self.assertEqual(response.status_code, 302)

    def test_cookie_login_with_get(self):
        response = Client().get('/lab-9/cookie/auth_login/')
        self.assertEqual(response.status_code, 302)

    def test_cookie_wrong_username(self):
        data = {
            'username': 'lol',
            'password': 'lol'
        }
        response = Client().post('/lab-9/cookie/auth_login/', data=data)
        self.assertEqual(response.status_code, 302)

    def test_cookie(self):
        data = {
            'username': 'username',
            'password': 'password'
        }
        client = Client()

        response = client.post(
            '/lab-9/cookie/auth_login/', data=data, follow=True)
        self.assertEqual(response.status_code, 200)

        client.cookies['user_login'] = 'username_salah'
        response = client.get('/lab-9/cookie/profile/', follow=True)
        self.assertEqual(response.status_code, 200)

        response = client.get('/lab-9/cookie/clear/', follow=True)
        self.assertEqual(response.status_code, 200)
