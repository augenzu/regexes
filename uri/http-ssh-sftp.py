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


def alt_b(rules_list):  # (?:<rule1>|<rule2>|...|<rulen>)
    return bracket_group('|'.join(rules_list))


DIGIT = '[0-9]'
HEXDIG = '[0-9A-Fa-f]'

DEC_OCTET = alt_b([DIGIT, '[1-9]' + DIGIT, '1' + DIGIT * 2, '2[0-4]' + DIGIT, '25[0-5]'])

UNRESERVED = '[0-9A-Za-z._~-]'
PCT_ENCODED = '%' + HEXDIG * 2
SUB_DELIMS = '[!$&\'()*+,;=]'

IPV4ADDS = DEC_OCTET + bracket_group('\\.' + DEC_OCTET) + '{3}'
REG_NAME = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS]))

USERINFO = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS, ':']))
HOST = alt_b([IPV4ADDS, REG_NAME])
PORT = any_times(DIGIT)

PCHAR = alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS, ':', '@'])
SEGMENT = any_times(PCHAR)

AUTHORITY = maybe_b(USERINFO + '@') + HOST + maybe_b(':' + PORT)
PATH_ABEMPTY = any_times_b('/' + SEGMENT)
QUERY = any_times(alt_b([PCHAR, '/', '\\?']))
FRAGMENT = any_times(alt_b([PCHAR, '/', '\\?']))

HTTP_URI = 'https?://' + AUTHORITY + PATH_ABEMPTY + maybe_b('\\?' + QUERY) + maybe_b('#' + FRAGMENT)


# ---SSH---


PARAMNAME = any_times('[0-9A-Za-z-]')
PARAMVALUE = any_times('[0-9A-Za-z-]')
C_PARAM = PARAMNAME + '=' + PARAMVALUE
SSH_INFO = maybe(USERINFO) + maybe_b(';' + C_PARAM + any_times_b(',' + C_PARAM))

SSH_AUTHORITY = maybe_b(maybe_b(SSH_INFO) + '@') + HOST + maybe_b(':' + PORT)

SSH_URI = 'ssh://' + SSH_AUTHORITY + PATH_ABEMPTY


# ---SFTP---


S_PARAM = PARAMNAME + '=' + PARAMVALUE
SFTP_AUTHORITY = maybe_b(SSH_INFO + '@') + HOST + maybe_b(':' + PORT)

SFTP_URI = 'sftp://' + SFTP_AUTHORITY + PATH_ABEMPTY + maybe_b(';' + S_PARAM + any_times_b(',' + S_PARAM))


# ------


print(HTTP_URI)
print(SSH_URI)
print(SFTP_URI)
