def obfuscate_email(email: str) -> str:
    assert email.count('@') == 1, email
    username, domain = email.split('@')
    return username + ' <AT> ' + '. '.join(domain.split('.'))
