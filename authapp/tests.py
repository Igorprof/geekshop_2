from django.test import TestCase, Client
from authapp.models import User

class TestUserAuthTestCase(TestCase):
    username = 'django'
    email = 'django@gb.local'
    password = 'geekbrains'

    def setUp(self):
        self.admin = User.objects.create_superuser(self.username, self.email, self.password)

        self.client = Client()
    
    def test_user_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)       

        self.client.login(username=self.username, password=self.password)
        response = self.client.get('/auth/login/')
        self.assertEqual(response.context['user'], self.admin)

        response = self.client.get('/')
        self.assertFalse(response.context['user'].is_anonymous)

    def tearDown(self):
        pass