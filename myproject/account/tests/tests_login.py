from django.test import TestCase
from django.contrib.auth.models import User

class LoginUnitTestCase(TestCase):
  def test_login_page(self):
    
    response = self.client.get('/login/')
    
    self.assertTemplateUsed(response, 'base.html')
    self.assertTemplateUsed(response, 'registration/login.html')

    self.assertContains(response, '<a href="/register/">')
    self.assertContains(response, '<a href="/password_reset/">')
    self.assertContains(response, '<a href="/activationlink/">')

  def setUp(self):
    self.user_name = 'testuser'
    self.user_pw = 'test123'
    User.objects.create_user(username=self.user_name, password=self.user_pw)  

  def test_user_login_incorrect(self):    
    
    # wrong password reload login page
    response = self.client.post('/login/', {'username': self.user_name, 'password': self.user_pw + 'incorrect'})
        
    self.assertTemplateUsed(response, 'registration/login.html')
    self.assertEquals(response.status_code, 200)

    # wrong user name reload login page
    response = self.client.post('/login/', {'username': self.user_name + 'incorrect', 'password': self.user_pw})
        
    self.assertTemplateUsed(response, 'registration/login.html')
    self.assertEquals(response.status_code, 200)
  

  def test_user_login_successful(self):      
          
    # Correct credentials but with username in uppercase redirect to dashboard
    response = self.client.post('/login/', {'username': self.user_name.upper(), 'password': self.user_pw})
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/dashboard/')

   # Correct credentials redirect to dashboard
    response = self.client.post('/login/', {'username': self.user_name, 'password': self.user_pw})
    
    self.assertEqual(response.status_code, 302)
    self.assertEqual(response.url, '/dashboard/')
          
