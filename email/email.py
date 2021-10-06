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


ATEXT = '[0-9A-Za-z!#$%&\'*+/=?^_`|{}~-]'
ATOM = one_time_or_more(ATEXT)
DOT_ATOM_TEXT = one_time_or_more(ATEXT) + any_times_b('\\.' + one_time_or_more(ATEXT))
DOT_ATOM = DOT_ATOM_TEXT  # ignoring [CFWS]

SPECIALS = '[()<>[\\]:;@\\\,."]'

WSP = '[ \\t]'
VCHAR = '[!-~]'

QUOTED_PAIR = '\\\\' + alt_b([VCHAR, WSP])
QTEXT = '[!#-[\\]-~]'
QCONTENT = alt_b([QTEXT, QUOTED_PAIR])
QUOTED_STRING = '"' + any_times(QCONTENT) + '"'  # ignoring [FWS] & [CFWS]

LOCAL_PART = alt_b([DOT_ATOM, QUOTED_STRING])

DTEXT = '[!-Z^-~]'
DOMAIN_LITERAL = '\\[' + any_times(DTEXT) + '\\]'
DOMAIN = alt_b([DOT_ATOM, DOMAIN_LITERAL])

ADDR_SPEC = LOCAL_PART + '@' + DOMAIN

print(ADDR_SPEC)
