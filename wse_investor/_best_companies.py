import os

from wse_investor._requirement import Requirement
from wse_investor._rank import RankedCompanies
from wse_investor._financial_indicator import FinancialIndicators
from wse_investor._dividend import Dividend
from wse_investor._results_writer import CsvFileWriter
from wse_investor._limits_reader import LimitsTxtFileReader


def get():
    requirement = Requirement(LimitsTxtFileReader(os.path.join(os.getcwd(), 'limits.txt')))

    companies = RankedCompanies(requirement).get_best_companies()
    companies = FinancialIndicators(companies, requirement).get_best_companies()
    companies = Dividend(companies, requirement).get_best_companies()

    CsvFileWriter(companies).write()
