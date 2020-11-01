from pathlib import Path
import pytest

from src.crawlers import real_state_funds

BASE_DIR = Path(__file__).resolve(strict=True).parent


class TestCrawler():
    """
    Test the crawler functions
    """

    @pytest.fixture(scope="module")
    def html_output(self):
        with open(Path(BASE_DIR).joinpath("test.html"), encoding="utf-8") as f:
            html = f.read()
            bot = real_state_funds.BotFIIsWebsite()
            yield bot._parse_content(html)


    def test_content_is_not_none(self, html_output):
        assert html_output


    def test_output_is_a_list_of_dicts(self, html_output):
        print(type(html_output))
        assert all(isinstance(elem, dict) for elem in html_output)
