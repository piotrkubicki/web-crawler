import pytest

from unittest.mock import patch, Mock

from main import (
    extract_links_from_url,
    is_not_external_link,
    filter_external_links,
    create_map,
)


@patch("main.requests.get")
def test_extract_links_from_url_returns_set(my_mock_get):
    with open("tests/test_page.html") as f:
        mock_response = Mock()
        mock_response.text = f
        my_mock_get.return_value = mock_response

        res = extract_links_from_url("http://www.test.com")
        print(res)
        assert res == {
            "http://www.test.com",
            "http://www.test.com/linux",
            "http://www.test.com/macos",
            "http://www.test.com/windows",
            "http://www.fake.com/profile",
        }


@pytest.mark.parametrize(
    "url,base_url,expected",
    [
        ("http://www.test.com", "http://www.test.com", True),
        ("http://www.test.com/next-page", "http://www.test.com", True),
        ("http://www.incorrectpage.com", "http://www.test.com", False),
        ("https://www.test.com", "http://www.test.com", False),
        ("http://incorrectpage.com/next-page", "http://www.test.com", False),
    ],
)
def test_is_not_exernal_link(url, base_url, expected):
    assert is_not_external_link(url, base_url) == expected


def test_filter_external_links():
    test_links = [
        "http://www.test.com",
        "http://www.test.com/second-page",
        "http://www.test.com/third-page",
        "http://www.external.com/first-page",
        "http://www.test.com/fourth-page",
        "http://www.another-external.com/second-page",
        "mailto:test@test.com",
    ]
    base_url = "http://www.test.com"

    assert filter_external_links(test_links, base_url) == [
        "http://www.test.com",
        "http://www.test.com/second-page",
        "http://www.test.com/third-page",
        "http://www.test.com/fourth-page",
    ]


def test_create_map_for_index_page():
    test_links = [
        "http://www.test.com/second-page",
        "http://www.test.com/third-page",
        "http://www.test.com/fourth-page",
    ]
    index_url = "http://www.test.com"

    assert create_map(index_url, test_links, index_url) == {"index": test_links}


def test_create_map_for_sub_page():
    test_links = [
        "http://www.test.com/second-page",
        "http://www.test.com/third-page",
        "http://www.test.com/fourth-page",
    ]
    index_url = "http://www.test.com"

    assert create_map(f"{index_url}/other-page", test_links, index_url) == {
        f"{index_url}/other-page": test_links
    }
