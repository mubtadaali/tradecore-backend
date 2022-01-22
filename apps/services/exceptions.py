class EmailValidationTimeoutException(Exception):
    def __str__(self):
        return 'Email validation API timed out.'
