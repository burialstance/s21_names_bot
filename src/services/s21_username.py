import re
from typing import Optional
from email_validator import validate_email, ValidatedEmail, EmailSyntaxError


def extract_email_local_part(text: str) -> Optional[str]:
    """
    :param text: tyberora@student.21-school.ru
    :return: tyberora
    """
    try:
        validated: ValidatedEmail = validate_email(text)
        return validated.local_part
    except EmailSyntaxError:
        pass


def validate_s21_login(text: str) -> Optional[str]:
    text = extract_email_local_part(text) if '@' in text else text
    if match := re.search(r'^[a-zA-Z0-9]{4,}$', text):
        login = match.group()
        return login


def create_s21_profile_url(s21_login: str) -> str:
    return f'https://edu.21-school.ru/profile/{s21_login}@student.21-school.ru'


if __name__ == '__main__':
    assert validate_s21_login('tyberora@student.21-school.ru') == 'tyberora'
    assert validate_s21_login('tyberora') == 'tyberora'
    assert validate_s21_login('залупа') is None
    assert validate_s21_login('комазотходов@student.21-school.ru') is None
    assert validate_s21_login('/adobe@student.21-school.ru') is None
    assert validate_s21_login('/start') is None
    assert validate_s21_login('zalупа') is None
