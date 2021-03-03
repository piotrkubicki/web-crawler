import pytest

from unittest.mock import patch, Mock, call

from main import (
    extract_links_from_url,
    is_not_external_link,
    filter_external_links,
    save_result,
    map_page,
)


@patch("main.requests.get")
def test_extract_links_from_url_returns_set(my_mock_get):
    with open("tests/test_page.html") as f:
        mock_response = Mock()
        mock_response.text = f
        my_mock_get.return_value = mock_response

        res = extract_links_from_url("http://www.test.com")
        assert sorted(res) == sorted(
            [
                "http://www.test.com",
                "http://www.test.com/linux",
                "http://www.test.com/macos",
                "http://www.test.com/windows",
                "http://www.fake.com/profile",
            ]
        )


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


def test_save_result(tmpdir):
    test_links = [
        "http://www.test.com",
        "http://www.test.com/second-page",
        "http://www.test.com/third-page",
        "http://www.test.com/fourth-page",
    ]
    test_dir = tmpdir.mkdir("test")
    save_result(test_links, "https://test.com", path=str(test_dir))
    with open(f"{str(test_dir)}/test.com.html") as f:
        assert f.read() == (
            "<HTML>\n"
            "\t<h2>URL: https://test.com</h2>\n"
            "\t<div><a href=http://www.test.com>http://www.test.com</a></div>\n"
            "\t<div><a href=http://www.test.com/second-page>http://www.test.com/second-page</a></div>\n"
            "\t<div><a href=http://www.test.com/third-page>http://www.test.com/third-page</a></div>\n"
            "\t<div><a href=http://www.test.com/fourth-page>http://www.test.com/fourth-page</a></div>\n"
            "</HTML>\n"
        )


@patch("main.logging")
@patch("main.extract_links_from_url")
@patch("main.save_result")
def test_map_page(mock_save_result, mock_extract_links_from_url, mock_logger):
    mock_mapping_queue = Mock()
    mock_mapping_queue.get.return_value = "https://www.test.com"
    mock_mapping_queue.qsize.return_value = 0
    mock_extract_links_from_url.return_value = []
    test_mapped_pages = ["https://www.index-test-page.com"]
    map_page(test_mapped_pages, mock_mapping_queue)

    assert mock_logger.info.call_count == 2
    mock_logger.assert_has_calls = (
        call("Extracting site https://www.test.com"),
        call("Result saved"),
    )
    assert test_mapped_pages == [
        "https://www.index-test-page.com",
        "https://www.test.com",
    ]
    assert mock_save_result.call_count == 1
    assert mock_mapping_queue.get.call_count == 1
    assert mock_mapping_queue.qsize.call_count == 1
    assert mock_mapping_queue.put.call_count == 0
    assert mock_mapping_queue.task_done.call_count == 1
