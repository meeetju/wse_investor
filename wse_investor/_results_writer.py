from abc import ABC, abstractmethod
import csv
import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


class ResultsWriter(ABC):

    @abstractmethod
    def write(self):
        """Write results to output."""


class CsvFileWriter(ResultsWriter):

    def __init__(self, companies):
        self._companies = companies
        self._results_file_path = os.path.join(os.getcwd(), self._get_results_file_name())

    @staticmethod
    def _get_results_file_name():
        now = datetime.datetime.now()
        name = 'best_companies_%s.csv' % now.strftime("%Y_%m_%d")
        return name

    def _get_header(self):
        header = [k for k in self._companies[0].__dict__.keys()]
        self._hyper_link_index = header.index('base_link')
        return header

    def _get_data(self, company):
        data = [v for v in company.__dict__.values()]
        data[self._hyper_link_index] = r'=HYPERLINK("%s")' % data[self._hyper_link_index]
        return data

    def write(self):

        with open(self._results_file_path, 'w+') as report_file:
            report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            report_writer.writerow(self._get_header())
            for company in self._companies:
                report_writer.writerow(self._get_data(company))

        logger.info('Report stored in : %s' % self._results_file_path)
