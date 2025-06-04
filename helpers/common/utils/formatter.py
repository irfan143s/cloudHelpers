from __future__ import annotations

from libraries import phonenumbers


def to_11_digits_ph_mobile_no(number) -> str:
    parsed_no = phonenumbers.format_number(phonenumbers.parse(number, 'PH'), phonenumbers.PhoneNumberFormat.E164)
    return '0' + parsed_no[-10:]


def to_10_digits_ph_mobile_no(number) -> str:
    parsed_no = phonenumbers.format_number(phonenumbers.parse(number, 'PH'), phonenumbers.PhoneNumberFormat.E164)
    return parsed_no[-10:]

def to_13_digits_ph_mobile_no(number) -> str:
    try:
        parsed_no = phonenumbers.format_number(phonenumbers.parse(number, 'PH'), phonenumbers.PhoneNumberFormat.E164)
        return '+63' + parsed_no[-10:]
    except Exception as error:
        return number