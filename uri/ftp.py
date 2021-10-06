import re


def bracket_group(rule):  # (?:<rule>)
    return '(?:' + rule + ')'


def maybe_b(rule):  # (?:<rule>)?
    return bracket_group(rule) + '?'


def maybe(rule):  # <rule>?
    return rule + '?'


def any_times_b(rule):  # (?:<rule>)*
    return bracket_group(rule) + '*'


def any_times(rule):  # <rule>*
    return rule + '*'


def one_time_or_more(rule):  # <rule>*
    return rule + '+'


def alt_b(rules_list):  # (?:<rule1>|<rule2>|...|<rulen>)
    return bracket_group('|'.join(rules_list))


DIGIT = '[0-9]'
HEXDIG = '[0-9A-Fa-f]'

DEC_OCTET = alt_b([DIGIT, '[1-9]' + DIGIT, '1' + DIGIT * 2, '2[0-4]' + DIGIT, '25[0-5]'])

UNRESERVED = '[0-9A-Za-z._~-]'
PCT_ENCODED = '%' + HEXDIG * 2
SUB_DELIMS = '[!$&\'()*+,;=]'
SUB_DELIMS_NSC = '[!$&\'()*+,=]'

USER = one_time_or_more(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS]))
PASS = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS]))

IPV4ADDS = DEC_OCTET + bracket_group('\\.' + DEC_OCTET) + '{3}'
REG_NAME = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS]))

SEGMENT_NSC = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS_NSC, ':', '@']))

CWD_PART = any_times_b('/' + SEGMENT_NSC)
LAST_SEGMENT = SEGMENT_NSC
TYPECODE_PART = ';type=[aeiud]'  # ';type=[A-Za-z]'

USERINFO = USER + maybe_b(':' + PASS)
HOST = alt_b([IPV4ADDS, REG_NAME])
PORT = any_times(DIGIT)
FTP_PATH = CWD_PART + '/' + LAST_SEGMENT + maybe_b(TYPECODE_PART)

FTP_URI = 'ftp://' + maybe_b(USERINFO + '@') + HOST + maybe_b(':' + PORT) + maybe_b(FTP_PATH)

print(FTP_URI)
