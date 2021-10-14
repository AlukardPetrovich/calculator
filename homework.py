import datetime as dt


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        today_stats = 0
        for record in self.records:
            if record.date == dt.date.today():
                today_stats += record.amount
        return today_stats

    def get_week_stats(self):
        week_stats = 0
        today = dt.date.today()
        week = today - dt.timedelta(days=7)
        for record in self.records:
            if week < record.date <= today:
                week_stats += record.amount
        return week_stats


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
        return '{} {} {}'.format(self.amount, self.comment, self.date)


class CaloriesCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)

    def get_calories_remained(self):
        calories_remained = self.limit - self.get_today_stats()
        if calories_remained <= 0:
            return 'Хватит есть!'
        else:
            return (
                f'Сегодня можно съесть что-нибудь ещё, но с общей'
                f' калорийностью не более {calories_remained} кКал')


class CashCalculator(Calculator):
    def __init__(self, limit):
        super().__init__(limit)
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
        value = currencies[currency]
        today_cash_remained = today_cash_remained / value[1]
        if today_cash_remained < 0:
            return (
                f'Денег нет, держись: твой долг '
                f'- {abs(today_cash_remained):.2f} {value[0]}')
        else:
            return f'На сегодня осталось {today_cash_remained:.2f} {value[0]}'
