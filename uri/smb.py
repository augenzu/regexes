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

IPV4ADDS = DEC_OCTET + bracket_group('\\.' + DEC_OCTET) + '{3}'
REG_NAME = any_times(alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS]))

HOST = alt_b([IPV4ADDS, REG_NAME])
PORT = any_times(DIGIT)

PCHAR = alt_b([UNRESERVED, PCT_ENCODED, SUB_DELIMS, ':', '@'])
SEGMENT = any_times(PCHAR)
SEGMENT_NZ = one_time_or_more(PCHAR)

PATH_ABSOLUTE = '/' + maybe_b(SEGMENT_NZ + any_times_b('/' + SEGMENT))
PATH_ROOTLESS = SEGMENT_NZ + any_times_b('/' + SEGMENT)

SCOPE_CHAR = alt_b(['[0-9A-Za-z!$&\'()+,;=_~-]', PCT_ENCODED])
SCOPE_LABEL = SCOPE_CHAR + '{1,63}'
SCOPE_ID = maybe_b(SCOPE_LABEL + any_times_b('\\.' + SCOPE_LABEL))

NET_BIOS_NAME_C = alt_b(['[0-9A-Za-z!$&\'()+,;=_~-]', PCT_ENCODED])
NET_BIOS_NAME = NET_BIOS_NAME_C + alt_b([NET_BIOS_NAME_C, '\\*']) + '{1,14}'
NBT_NAME = NET_BIOS_NAME + maybe_b('\\.' + SCOPE_ID)

SMB_SRV_NAME = alt_b([NBT_NAME, HOST])

USERINFO_NOSEM = any_times(alt_b(['[0-9A-Za-z!$&\'()*+,=:._~-]', PCT_ENCODED]))
AUTH_DOMAIN = SMB_SRV_NAME
SMB_USERINFO = maybe_b(AUTH_DOMAIN + ';') + USERINFO_NOSEM

SMB_SERVER = maybe_b(SMB_USERINFO + '@') + SMB_SRV_NAME + maybe_b(':' + PORT)

SMB_WRKGRP = maybe_b(SMB_USERINFO + '@') + maybe_b(SMB_SRV_NAME) + maybe_b(':' + PORT) + maybe('/')
SMB_NET_PATH = SMB_SERVER + maybe_b(PATH_ABSOLUTE)

NBT_PARAM = alt_b([
    'BROADCAST=' + IPV4ADDS + maybe_b(':' + PORT),
    alt_b(['CALLED=', 'CALLING=']) + NET_BIOS_NAME,
    alt_b(['NBNS=', 'WINS=']) + HOST + maybe_b(':' + PORT),
    'NODETYPE=' + alt_b(['B', 'P', 'M', 'H']),
    alt_b(['SCOPEID=', 'SCOPE=']) + SCOPE_ID
    ])

SMB_SERVICE = alt_b([SMB_WRKGRP, SMB_NET_PATH])
NBT_CONTEXT = NBT_PARAM + any_times_b(';' + NBT_PARAM)

SCHEME = alt_b(['smb', 'cifs'])
SMB_ABS_URI = SCHEME + '://' + SMB_SERVICE + maybe_b('\\?' + maybe_b(NBT_CONTEXT))
SMB_REL_URI = alt_b([PATH_ABSOLUTE, PATH_ROOTLESS]) + maybe_b('\\?' + maybe_b(NBT_CONTEXT))

SMB_URI = '\\b' + alt_b([SMB_ABS_URI, SMB_REL_URI]) + '\\b'

# print(SMB_URI)
# print('\\b' + SMB_ABS_URI + '\\b')
# print('\\b' + SMB_REL_URI + '\\b')
