from django.test import TestCase

class LoginPageUnitTestCase(TestCase):

  def test_activation_link_page(self):
    response = self.client.get('/activationlink/')
    
    self.assertTemplateUsed(response, 'base.html')
    self.assertTemplateUsed(response, 'account/resend_activation.html')

    self.assertContains(response, '<form method="post">')
    self.assertContains(response, '<label for="id_email">')

 #def test_pw_reset_page(self):
 #  response = self.client.get('/password_reset/')
 #  
 #  self.assertTemplateUsed(response, 'base.html')
 #  self.assertTemplateUsed(response, 'account/password_reset_form.html')
