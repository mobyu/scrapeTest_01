# cookie方式登录
import requests
from urllib.parse import urljoin

BASE_URL = 'https://login2.scrape.center/'
LOGIN_URL = urljoin(BASE_URL, '/login')
INDEX_URL = urljoin(BASE_URL, '/page/1')
USERNAME = 'admin'
PASSWORD = 'admin'

session = requests.Session()

response_login = session.post(LOGIN_URL, data={
    'username': USERNAME,
    'password': PASSWORD
})

cookie = session.cookies
print('Cookie:', cookie)

response_index = session.get(INDEX_URL)
print('Response Status', response_index.status_code)
print('Response URL', response_index.url)