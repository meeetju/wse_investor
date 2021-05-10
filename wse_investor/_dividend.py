from bs4 import BeautifulSoup
import logging
import requests

from wse_investor._company import Company
from wse_investor._requirement import Requirement

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class Dividend:

    def __init__(self, companies: [Company], requirement: Requirement):
        self._in_companies = companies
        self._out_companies = []
        self._requirement = requirement

    def get_best_companies(self):
        for company in self._in_companies:
            self._get_dividend_content(company)
            if self._requirement.is_dividend_paid(company.last_dividend_year):
                self._out_companies.append(company)

        logger.info('Identified %s companies that pay dividend' % str(len(self._out_companies)))
        return self._out_companies

    def _get_dividend_content(self, company):
        dividend_values = []
        one_dividend_record_size = 5

        link = company.base_link + r'/dywidendy'
        try:
            dividend_www = requests.get(link)
            dividend = BeautifulSoup(dividend_www.text, "html.parser")

            for tr in dividend.findAll('tr'):
                for td in tr.findAll('td'):
                    dividend_values.append(self._get_value(td))
                    if len(dividend_values) >= one_dividend_record_size:
                        break

            company.last_dividend_year = dividend_values[0]
            company.last_buy_date = dividend_values[1]
            company.dividend_percent = dividend_values[2][:-1]
            company.payment_date = dividend_values[3]
            company.dividend_amount = dividend_values[4][:-2]

            logger.info('Getting data from : %s' % link)
        except IndexError:
            logger.warning('Could not reach : %s' % link)

    def _get_value(self, td):
        return td.text.replace(' ', '')