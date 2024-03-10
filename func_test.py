import os
import time
from selenium import webdriver
#from selenium.webdriver.edge.service import Service
#from selenium.webdriver.edge.options import Options

#edge_driver_path = os.path.join(os.getcwd(), 'edgedriver_win64\msedgedriver.exe')
#print(f'DIRECTORY {edge_driver_path}')

#edge_service = Service(edge_driver_path)
edge_options = webdriver.EdgeOptions()
edge_options.add_argument("--enable-chrome-browser-cloud-management")
edge_options.add_experimental_option('excludeSwitches', ['enable-logging'])

#browser = webdriver.Edge(service=edge_service, options=edge_options)
browser = webdriver.Edge(options=edge_options)

browser.get('http://localhost:8000')
page_source = browser.page_source


assert page_source.find('Booklist') > 0, "Nope"
assert "Booklist" in page_source, "Das Wort wurde nicht gefunden."

time.sleep(3)

if "Booklist" in browser.page_source:
  print('Yeah')
else:
  print('Neeee')


# Close the browser
browser.quit()
