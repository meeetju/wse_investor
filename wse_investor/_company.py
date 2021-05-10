class Company:

    def __init__(self):
        self.ticker = ''
        self.name = ''
        self.rating = ''
        self.rating_date = ''
        self.piotroski_f_score = '0.0'
        self.base_link = ''
        self.p_e = '0.0'
        self.p_bv = '0.0'
        self.p_bv_g = '0.0'
        self.p_s = '0.0'
        self.roe = '0.0'
        self.last_dividend_year = ''
        self.last_buy_date = ''
        self.dividend_percent = ''
        self.payment_date = ''
        self.dividend_amount = ''

    def __str__(self):
        return str(self.__dict__)  # pragma: no cover
