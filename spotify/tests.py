import json
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from player.models import Artist, Album, Track


def get_response(path):
    response = APIClient().get(path)
    return json.loads(response.content)


class ArtistTestCase(TestCase):

    def setUpTestData():
        User.objects.create_user(
            'john', 'lennon@thebeatles.com', 'johnpassword')

    def setUp(self):
        Artist.objects.create(name='Metallica')
        Artist.objects.create(name='Weezer')

    def test_list(self):
        response = get_response('/api/artist/')
        self.assertEqual(response.get('results'), [
                         {'id': 1, 'name': 'Metallica'}, {'id': 2, 'name': 'Weezer'}])

    def test_retrieve(self):
        self.assertEqual(get_response('/api/artist/1/'),
                         {'id': 1, 'name': 'Metallica'})
        self.assertEqual(get_response('/api/artist/2/'),
                         {'id': 2, 'name': 'Weezer'})

    def test_post(self):
        response = APIClient().post('/api/artist/', {'name': 'The Strokes'})
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        response = APIClient().delete('/api/artist/1/')
        self.assertEqual(response.status_code, 204)

    def test_put(self):
        response = APIClient().post('/api/artist/', {'name': 'Strokes'})
        self.assertEqual(response.status_code, 201)
        response = APIClient().put('/api/artist/3/', {'name': 'The Strokes'})
        self.assertEqual(response.status_code, 200)

    def test_sorting(self):
        response = get_response('/api/artist/?ordering=-name')
        self.assertEqual(response.get('results'), [
                         {'id': 2, 'name': 'Weezer'}, {'id': 1, 'name': 'Metallica'}])
        response = get_response('/api/artist/?ordering=name')
        self.assertEqual(response.get('results'), [
                         {'id': 1, 'name': 'Metallica'}, {'id': 2, 'name': 'Weezer'}])

    def test_pagination(self):
        response = get_response('/api/artist/?limit=1&offset=0')
        self.assertEqual(response['count'], 2)
        next_page = response['next']
        test_server_prefix = 'http://testserver'
        self.assertTrue(next_page.startswith(test_server_prefix))
        next_page = next_page[len(test_server_prefix):]
        self.assertEqual(response['results'], [{'id': 1, 'name': 'Metallica'}])

        response = get_response(next_page)
        self.assertEqual(response['count'], 2)
        self.assertEqual(response['next'], None)
        self.assertEqual(response['results'], [{'id': 2, 'name': 'Weezer'}])
