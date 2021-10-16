import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        return sum([record.amount for record in self.records
                    if record.date == dt.date.today()])

    def get_week_stats(self):
        today = dt.date.today()
        week = dt.date.today() - dt.timedelta(days=7)
        return sum([record.amount for record in self.records
                    if (week < record.date <= today)])


class Record:
    format = '%d.%m.%Y'

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.date.today()
        else:
            self.date = dt.datetime.strptime(date, self.format).date()

    def __str__(self):
        return f'{self.amount}, {self.comment}, {self.date}'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return 'Хватит есть!'
        return (
            f'Сегодня можно съесть что-нибудь ещё, но с общей'
            f' калорийностью не более {calories_remained} кКал')


class CashCalculator(Calculator):
    RUB_RATE = 1
    USD_RATE = 72.3
    EURO_RATE = 83.3

    def get_today_cash_remained(self, currency):
        currencies = {
            'usd': ('USD', self.USD_RATE),
            'rub': ('руб', self.RUB_RATE),
            'eur': ('Euro', self.EURO_RATE)}
        today_cash_remained = self.limit - self.get_today_stats()
        if today_cash_remained == 0:
            return 'Денег нет, держись'
        if currency not in currencies:
            return 'запрошен рассчет в неизвестной валюте'
        currency_tmp, rate = currencies[currency]
        today_cash_remained /= rate
        if today_cash_remained < 0:
            return (
                f'Денег нет, держись: твой долг '
                f'- {abs(today_cash_remained):.2f} {currency_tmp}')
        return (f'На сегодня осталось {today_cash_remained:.2f}'
                f' {currency_tmp}')
