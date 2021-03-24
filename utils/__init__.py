from .jalali import Gregorian


def convert_to_persian_number(str_):
    numbers = {
        '0': '۰',
        '1': '۱',
        '2': '۲',
        '3': '۳',
        '4': '۴',
        '5': '۵',
        '6': '۶',
        '7': '۷',
        '8': '۸',
        '9': '۹',
    }
    for en, fa in numbers.items():
        str_ = str_.replace(en, fa)

    return str_


def convert_to_perisna_months(number):
    months = {
        '1': 'فروردین',
        '2': 'اردیبهشت',
        '3': 'خرداد',
        '4': 'تیر',
        '5': 'مرداد',
        '6': 'شهریور',
        '7': 'مهر',
        '8': 'آبان',
        '9': 'آذر',
        '10': 'دی',
        '11': 'بهمن',
        '12': 'اسفند',
    }
    return months[str(number)]


def convert_to_jalali(time):
    gregorian_date_in_str = f"{time.year}-{time.month}-{time.day}"
    persian_date_tuple = Gregorian(gregorian_date_in_str).persian_tuple()

    persian_month = convert_to_perisna_months(persian_date_tuple[1])
    persian_date_str = f"{persian_date_tuple[2]} {persian_month} {persian_date_tuple[0]} ساعت {time.hour}:{time.minute}"

    date_in_persian_numbers = convert_to_persian_number(persian_date_str)
    return date_in_persian_numbers
