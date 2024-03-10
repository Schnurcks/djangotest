from django.test import TestCase
from django.contrib.auth.models import User


class DashboardCheck(TestCase):
  def test_user_not_logged_in(self):
      response = self.client.get('/dashboard/')

      self.assertEqual(response.status_code, 302)
      self.assertEqual(response.url, '/login/?next=/dashboard/')

  def test_user_logged_in(self):
    # Benutzer erstellen
    user = User.objects.create_user(username='testuser1', password='testuser1234')

    # Anmeldung simulieren (optional)
    self.client.login(username='testuser1', password='testuser1234')
    response = self.client.get('/dashboard/')
    
    self.assertEqual(response.status_code, 200)
        