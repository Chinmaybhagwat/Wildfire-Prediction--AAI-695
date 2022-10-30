from datetime import timedelta


def is_float(element):
    try:
        float(element)
        return True
    except ValueError:
        return False


def daterange(date1, date2):
    date_list = []
    for n in range(int((date2 - date1).days) + 1):
        date_list.append(date1 + timedelta(n))
    return date_list
