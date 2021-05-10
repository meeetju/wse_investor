from mock import MagicMock, patch, mock_open
import pytest
import requests

from wse_investor._rank import RankedCompanies
from wse_investor._limits_reader import LimitsTxtFileReader
from wse_investor._requirement import Requirement
from tests.data_for_tests import ratings_response_text, limits_file_text


class TestCompaniesListBuilder:

    @pytest.fixture
    def limits_reader(self):
        with patch("builtins.open", new_callable=mock_open, read_data=limits_file_text):
            self.requirement = Requirement(LimitsTxtFileReader('dummy path'))
            yield

    @pytest.fixture
    def www_response(self):
        response = MagicMock(spec=requests.models.Response)
        response.text = ratings_response_text

        with patch('wse_investor._rank.requests.get', return_value=response):
            yield

    def test_all_companies_are_returned_with_correct_data(self, www_response, limits_reader):

        rank = RankedCompanies(self.requirement)
        companies = rank.get_all_companies()

        assert len(companies) == 4

        assert companies[0].ticker == 'MRB'
        assert companies[0].name == 'MIRBUD'
        assert companies[0].rating == 'BBB'
        assert companies[0].rating_date == '2020/Q4'
        assert companies[0].piotroski_f_score is None
        assert companies[0].base_link == r'https://strefainwestorow.pl/notowania/gpw/MIRBUD-MRB'

        assert companies[1].ticker == 'AST'
        assert companies[1].name == 'ASTARTA'
        assert companies[1].rating == 'CCC'
        assert companies[1].rating_date == '2020/Q4'
        assert companies[1].piotroski_f_score == '8'
        assert companies[1].base_link == r'https://strefainwestorow.pl/notowania/gpw/ASTARTA-AST'

        assert companies[2].ticker == 'OAT'
        assert companies[2].name == 'OAT'
        assert companies[2].rating == 'AAA'
        assert companies[2].rating_date == '2020/Q4'
        assert companies[2].piotroski_f_score == '8'
        assert companies[2].base_link == r'https://strefainwestorow.pl/notowania/gpw/OAT-OAT'

        assert companies[3].ticker == 'INC'
        assert companies[3].name == 'INC'
        assert companies[3].rating is None
        assert companies[3].rating_date == '2020/Q3'
        assert companies[3].piotroski_f_score == '6'
        assert companies[3].base_link == r'https://strefainwestorow.pl/notowania/gpw/INC-INC'

    def test_only_good_rated_companies_are_returned(self, www_response, limits_reader):

        rank = RankedCompanies(self.requirement)
        companies = rank.get_best_companies()

        assert len(companies) == 1

        assert companies[0].ticker == 'OAT'
        assert companies[0].name == 'OAT'
        assert companies[0].rating == 'AAA'
        assert companies[0].rating_date == '2020/Q4'
        assert companies[0].piotroski_f_score == '8'
