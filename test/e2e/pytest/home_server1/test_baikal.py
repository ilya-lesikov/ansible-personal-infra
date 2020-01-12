#!/usr/bin/env python3
from requests import Session
from requests.compat import urljoin
from requests_html import HTML
from caldav import DAVClient
import pytest

VCAL_UID = '0000000008'
VCAL = f"""\
BEGIN:VCALENDAR
VERSION:2.0
PRODID:-//Example Corp.//CalDAV Client//EN
BEGIN:VEVENT
UID:{VCAL_UID}
DTSTAMP:20170805T160000Z
DTSTART:20170805T170000Z
DTEND:20170805T180000Z
SUMMARY:This is an event
END:VEVENT
END:VCALENDAR
"""


@pytest.fixture
def web_login(request):
    opts = request.config.option

    url = urljoin(opts.baikal_baseurl, '/admin/')
    data = {'auth': '1', 'login': opts.baikal_user, 'password': opts.baikal_pass}
    with Session() as session:
        resp = session.post(url, data=data, verify=False)
        yield session, resp


@pytest.fixture
def dav_login(request):
    opts = request.config.option

    url = urljoin(opts.baikal_baseurl, '/dav.php/')
    client = DAVClient(
        url, username=opts.baikal_dav_user, password=opts.baikal_dav_pass,
        ssl_verify_cert=False
    )
    return client


def test_web_login(web_login):
    _, resp = web_login
    assert resp.status_code == 200
    assert '/admin/?/logout/' in HTML(html=resp.content).links


def test_web_create_user(request, web_login):
    opts = request.config.option

    session, _ = web_login
    url = urljoin(opts.baikal_baseurl, '/admin/?/users/new/1/')
    resp_get = session.get(url, verify=False)
    html_get = HTML(html=resp_get.content)
    csrf_token = html_get.find('input[name=CSRF_TOKEN]', first=True).attrs['value']
    assert csrf_token

    data = {
        'Baikal_Model_User::submitted': '1',
        'refreshed': '0',
        'CSRF_TOKEN': csrf_token,
        'data[username]': opts.baikal_dav_user,
        'witness[username]': '1',
        'data[displayname]': opts.baikal_dav_user,
        'witness[displayname]': '1',
        'data[email]': opts.baikal_dav_email,
        'witness[email]': '1',
        'data[password]': opts.baikal_dav_pass,
        'witness[password]': '1',
        'data[passwordconfirm]': opts.baikal_dav_pass,
        'witness[passwordconfirm]': '1'
    }
    resp_post = session.post(url, data, verify=False)
    html_post = HTML(html=resp_post.content)
    notification = html_post.find('#message', first=True).text
    assert notification == f'User {opts.baikal_dav_user} has been created.'


def test_dav_login(dav_login):
    client = dav_login
    client.principal()


def test_dav_add_event(dav_login):
    client = dav_login
    cal = client.principal().calendars()[0]
    cal.add_event(VCAL)
    cal.event(VCAL_UID)
