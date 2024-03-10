from django.test import TestCase, SimpleTestCase
from selenium import webdriver

def setupBrowser():
  edge_options = webdriver.EdgeOptions()
  edge_options.add_argument("--enable-chrome-browser-cloud-management")
  edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])
  browser = webdriver.Edge(options=edge_options)
  return browser


#class FunctionalTestCase(SimpleTestCase):
#
#    def setUp(self):
#      self.browser = setupBrowser()
#    
#    def test_homepage_exists(self):
#      self.browser.get('http://localhost:8000')
#      self.assertIn('Booklist', self.browser.page_source)
#
#    def tearDown(self):
#      self.browser.quit()
#

class UnitTestCase(TestCase):
  
  def test_homepage_templates(self):
    response = self.client.get('/')
    
    self.assertTemplateUsed(response, 'base.html')
    self.assertTemplateUsed(response, 'books/booklist.html')

  def test_login_link(self):
    response = self.client.get('/')

    self.assertContains(response, '<a href="/login/">', status_code=200)




    

  
  
