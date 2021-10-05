import re


ALPHA_UPPER = '[A-Z]'
ALPHA_LOWER = '[a-z]'
DIGIT = '[0-9]'
SPECSYMB = '[!@#$%^&*?]'
PWDSYMB = '[A-Za-z0-9!@#$%^&*?]'

BEG = '^'
END = '$'

LEN_GE_8 = '(?=.{8,}$)'
ONE_ALPHA_UPPER = '(?=[^A-Z]*[A-Z])'
ONE_ALPHA_LOWER = '(?=[^a-z]*[a-z])'
ONE_DIGIT = '(?=[^0-9]*[0-9])'
TWO_DIFFERENT_SPEC = '(?=.*?([!@#$%^&*?]).*?(?!\\1)[!@#$%^&*?])'
NO_TWO_IDENT_IN_ROW = '(?:([A-Za-z0-9!@#$%^&*?])(?!\\2))+'

REGEX_PARTS = [BEG, LEN_GE_8, ONE_ALPHA_UPPER, ONE_ALPHA_LOWER, ONE_DIGIT, TWO_DIFFERENT_SPEC, NO_TWO_IDENT_IN_ROW, END]
PASSWORD_REGEXP = r''.join(REGEX_PARTS)

print(re.fullmatch(PASSWORD_REGEXP, 'enroi#$rkdeR#$092uwedchf34tguv394h'))

# print(PASSWORD_REGEXP)
