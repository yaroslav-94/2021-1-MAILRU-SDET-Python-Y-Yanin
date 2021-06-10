import string
import random


def prepare_user_name(length=0, is_bad_sym=False):
    name = ""
    appruve_sym = string.ascii_letters
    bad_sym = string.punctuation
    if is_bad_sym:
        name = random.choice(bad_sym) + ''.join(random.choices(appruve_sym, k=length - 1))
    elif length > 0:
        name = ''.join(random.choices(appruve_sym, k=length))

    return name


def prepare_password(length=0):
    return ''.join(random.choices(string.ascii_letters + string.punctuation, k=length))


def prepare_email(no_dog=False, no_com=False, length=10, is_bad_sym=False):
    appruve_sym = string.ascii_letters
    bad_sym = string.punctuation + string.ascii_letters
    if is_bad_sym:
        email = ''.join(random.choices(bad_sym, k=length - 7)) + '@' + ''.join(random.choices(bad_sym, k=3)) + '.' + \
                ''.join(random.choices(bad_sym, k=2))
    else:
        email = ''.join(random.choices(appruve_sym, k=length - 7)) + '@' + ''.join(
            random.choices(appruve_sym, k=3)) + '.' + ''.join(random.choices(appruve_sym, k=2))
    if no_dog:
        email = email.replace('@', '')

    if no_com:
        email = email.replace('.', '')

    return email
