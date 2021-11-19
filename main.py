#!/usr/bin/env python3

import requests
from getpass import getpass
import webbrowser
import os

rollno = input('Rollno: ')
passwd = getpass()
session_month = input('Enter the month of session you want to check results for (In the format- yyyy/m, for example- 2021/1 for the January 2021 session): ')

print('Logging in...')
login_url ='https://misreg.nitt.edu/NITTSTUDENT/userLoginAction'
login_headers = {
    'Host': 'misreg.nitt.edu',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://misreg.nitt.edu/NITTSTUDENT/Logout',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Content-Length': '82',
    'Origin': 'https://misreg.nitt.edu',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1',
    'Sec-Fetch-Dest': 'document',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}
login_deets = f'userLoginBean.userId={rollno}&userLoginBean.password={passwd}&Submit=Sign+in'
login_resp = requests.post(login_url, headers=login_headers, data=login_deets)

for key, value in login_resp.headers.items():
    if key == 'Set-Cookie':
        cookie = value

cookie = cookie.replace('; Path=/NITTSTUDENT; Secure', '')

result_url = f'https://misreg.nitt.edu/NITTSTUDENT/displayresults?sessionName={session_month}'
result_headers = {
    'Host': 'misreg.nitt.edu',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:94.0) Gecko/20100101 Firefox/94.0',
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'DNT': '1',
    'Connection': 'keep-alive',
    'Referer': 'https://misreg.nitt.edu/NITTSTUDENT/resultPublish',
    'Cookie': f'{cookie}',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'Sec-GPC': '1',
}
html_resp = requests.get(result_url, headers=result_headers)

print(f'Downloading result for session {session_month} in result.html...')
file = open(f'result.html', 'a')
file.write(f'<h1>{session_month}<h1>')
file.write(html_resp.text)
file.close()

print('Openning in default browser...')
webbrowser.open('file://'+os.path.realpath(f'result.html'))
