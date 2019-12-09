#!/usr/bin/env python3
from requests import put, get, delete
from requests.compat import urljoin
import pytest

FILECONTENT = "filecontent"


@pytest.fixture
def upload_file(request):
    opts = request.config.option

    url = urljoin(opts.nxc_baseurl, opts.nxc_files_dav_prefix,
                  opts.nxc_test_file)
    resp = put(url, data=FILECONTENT, auth=(opts.nxc_user, opts.nxc_pass))
    return resp


@pytest.fixture
def delete_file(request):
    opts = request.config.option

    url = urljoin(opts.nxc_baseurl, opts.nxc_files_dav_prefix,
                  opts.nxc_test_file)
    resp = delete(url, auth=(opts.nxc_user, opts.nxc_pass))
    return resp


@pytest.fixture
def download_file(request):
    opts = request.config.option

    url = urljoin(opts.nxc_baseurl, opts.nxc_files_dav_prefix,
                  opts.nxc_test_file)
    resp = get(url, auth=(opts.nxc_user, opts.nxc_pass))
    return resp


def test_upload_file(upload_file, delete_file):
    upload_resp = upload_file
    assert upload_resp.ok
    delete_resp = delete_file
    assert delete_resp.ok


def test_download_file(upload_file, download_file, delete_file):
    upload_resp = upload_file
    assert upload_resp.ok
    download_resp = download_file
    assert download_resp.ok
    assert download_resp.content == FILECONTENT
    delete_resp = delete_file
    assert delete_resp.ok
