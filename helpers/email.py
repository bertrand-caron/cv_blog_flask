def obfuscate_email(email):
    assert email.count('@') == 1
    username, domain = email.split('@')
    return username + ' <AT> ' + '. '.join(domain.split('.'))
