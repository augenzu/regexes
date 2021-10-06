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


# nom
FEATURE_M_NOM = alt_b(['этот', 'тот', 'прошлый', 'прошедший', 'текущий', 'следующий'])
FEATURE_F_NOM = alt_b(['эта', 'та', 'прошлая', 'прошедшая', 'текущая', 'следующая'])
FEATURE_N_NOM = alt_b(['это', 'то', 'прошлое', 'прошедшее', 'текущее', 'следующее'])
# gen
FEATURE_M_GEN = alt_b(['этого', 'того', 'прошлого', 'прошедшего', 'текущего', 'следующего'])
FEATURE_F_GEN = alt_b(['этой', 'той', 'прошлой', 'прошедшей', 'текущей', 'следующей'])
FEATURE_N_GEN = alt_b(['этого', 'того', 'прошлого', 'прошедшего', 'текущего', 'следующего'])
# dat
FEATURE_M_DAT = alt_b(['этому', 'тому', 'прошлому', 'прошедшему', 'текущему', 'следующему'])
FEATURE_F_DAT = alt_b(['этой', 'той', 'прошлой', 'прошедшей', 'текущей', 'следующей'])
FEATURE_N_DAT = alt_b(['этому', 'тому', 'прошлому', 'прошедшему', 'текущему', 'следующему'])
# acc
FEATURE_M_ACC = alt_b(['этот', 'тот', 'прошлый', 'прошедший', 'текущий', 'следующий'])
FEATURE_F_ACC = alt_b(['эту', 'ту', 'прошлую', 'прошедшую', 'текущую', 'следующую'])
FEATURE_N_ACC = alt_b(['это', 'то', 'прошлое', 'прошедшее', 'текущее', 'следующее'])
# ins
FEATURE_M_INS = alt_b(['этим', 'тем', 'прошлым', 'прошедшим', 'текущим', 'следующим'])
FEATURE_F_INS = alt_b(['этой', 'той', 'прошлой', 'прошедшей', 'текущей', 'следующей'])
FEATURE_N_INS = alt_b(['этим', 'тем', 'прошлым', 'прошедшим', 'текущим', 'следующим'])
# pre
FEATURE_M_PRE = alt_b(['этом', 'том', 'прошлом', 'прошедшем', 'текущем', 'следующем'])
FEATURE_F_PRE = alt_b(['этой', 'той', 'прошлой', 'прошедшей', 'текущей', 'следующей'])
FEATURE_N_PRE = alt_b(['этом', 'том', 'прошлом', 'прошедшем', 'текущем', 'следующем'])

# nom
DAY_OF_WEEK_M_NOM = alt_b(['понедельник', 'вторник', 'четверг'])
DAY_OF_WEEK_F_NOM = alt_b(['среда', 'пятница', 'суббота'])
DAY_OF_WEEK_N_NOM = 'воскресенье'
# gen
DAY_OF_WEEK_M_GEN = alt_b(['понедельника', 'вторника', 'четверга'])
DAY_OF_WEEK_F_GEN = alt_b(['среды', 'пятницы', 'субботы'])
DAY_OF_WEEK_N_GEN = 'воскресенья'
# acc
DAY_OF_WEEK_F_ACC = alt_b(['среду', 'пятницу', 'субботу'])

DAY_OF_WEEK_MN = '(?:в\\s+)?' + alt_b([
    maybe_b(FEATURE_M_NOM + '\\s+') + DAY_OF_WEEK_M_NOM,
    maybe_b(FEATURE_N_NOM + '\\s+') + DAY_OF_WEEK_N_NOM
])
DAY_OF_WEEK_F = alt_b([
    'в\\s+' + maybe_b(FEATURE_F_ACC + '\\s+') + DAY_OF_WEEK_F_ACC,
    maybe_b(FEATURE_F_NOM + '\\s+') + DAY_OF_WEEK_F_NOM
])

DAY_OF_WEEK = alt_b([DAY_OF_WEEK_MN, DAY_OF_WEEK_F])  # В четверг

# gen
PART_OF_DAY_M_GEN = alt_b(['дня', 'вечера'])
PART_OF_DAY_F_GEN = 'ночи'
PART_OF_DAY_N_GEN = 'утра'
# ins
PART_OF_DAY_M_INS = alt_b(['днем', 'вечером'])
PART_OF_DAY_F_INS = 'ночью'
PART_OF_DAY_N_INS = 'утром'

PART_OF_DAY = alt_b([
    maybe_b(FEATURE_M_INS + '\\s+') + PART_OF_DAY_M_INS,
    maybe_b(FEATURE_F_INS + '\\s+') + PART_OF_DAY_F_INS,
    maybe_b(FEATURE_N_INS + '\\s+') + PART_OF_DAY_N_INS
])  # Этим утром

WEEK_ONLY = 'на\\s+' + maybe_b(FEATURE_F_PRE + '\\s+') + 'неделе'  # На прошлой неделе

# gen
MONTH_M_GEN = alt_b([
    'января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
    'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря'
])
# pre
MONTH_M_PRE = alt_b([
    'январе', 'феврале', 'марте', 'апреле', 'мае', 'июне',
    'июле', 'августе', 'сентябре', 'октябре', 'ноябре', 'декабре'
])

MONTH_ONLY = 'в\\s+' + maybe_b(FEATURE_M_PRE + '\\s+') + MONTH_M_PRE  # в сентябре

YEAR_NUM = '\d+'
YEAR_ONLY = 'в\\s+' + maybe_b(FEATURE_M_PRE + '\\s+') + YEAR_NUM + maybe_b('\\s+' + 'году')  # в 2017 году

DAY_NUM = alt_b(['[1-9]', '1[0-9]', '1[0-9]', '3[0-1]'])
DAY_N_MONTH = DAY_NUM + '\\s+' + MONTH_M_GEN  # 7 августа
YEAR_N_MONTH = MONTH_ONLY + '\\s+' + YEAR_NUM + '\\s+' + maybe('года')  # в августе 2019 года

DAY_N_MONTH_N_YEAR = DAY_N_MONTH + '\\s+' + YEAR_NUM + maybe_b('\\s+' + 'года')  # 14 июня 2021 года

COMPLEX = alt_b([
    DAY_OF_WEEK + ',' + '\\s+' + DAY_N_MONTH_N_YEAR,
    DAY_N_MONTH_N_YEAR + ',' + '\\s+' + DAY_OF_WEEK
    # PART_OF_DAY + '\\s+' + DAY_N_MONTH,
    # PART_OF_DAY + '\\s+' + DAY_N_MONTH_N_YEAR
]) # В четверг, 14 июня 2021 года

FROM_DAY_OF_WEEK = alt_b([
    maybe_b(FEATURE_M_GEN + '\\s+') + DAY_OF_WEEK_M_GEN,
    maybe_b(FEATURE_F_GEN + '\\s+') + DAY_OF_WEEK_F_GEN,
    maybe_b(FEATURE_N_GEN + '\\s+') + DAY_OF_WEEK_N_GEN
])
FROM_PART_OF_DAY = alt_b([
    maybe_b(FEATURE_M_GEN + '\\s+') + PART_OF_DAY_M_GEN,
    maybe_b(FEATURE_F_GEN + '\\s+') + PART_OF_DAY_F_GEN,
    maybe_b(FEATURE_N_GEN + '\\s+') + PART_OF_DAY_N_GEN
])
FROM_WEEK_ONLY = FEATURE_F_GEN + '\\s+' + 'недели'
FROM_MONTH_ONLY = maybe_b(FEATURE_M_GEN + '\\s+') + MONTH_M_GEN
FROM_YEAR_ONLY = maybe_b(FEATURE_M_GEN + '\\s+') + YEAR_NUM + maybe_b('\\s+' + 'года')
FROM_DAY_N_MONTH = DAY_NUM + '\\s+' + MONTH_M_GEN 
FROM_YEAR_N_MONTH = FROM_MONTH_ONLY + '\\s+' + YEAR_NUM + maybe_b('\\s+' + 'года')
FROM_DAY_N_MONTH_N_YEAR = DAY_N_MONTH + '\\s+' + YEAR_NUM + maybe_b('\\s+' + 'года')
FROM_COMPLEX = alt_b([
    FROM_DAY_OF_WEEK + ',' + '\\s+' + FROM_DAY_N_MONTH_N_YEAR,
    FROM_DAY_N_MONTH_N_YEAR + ',' + '\\s+' + FROM_DAY_OF_WEEK
    # PART_OF_DAY + '\\s+' + DAY_N_MONTH,
    # PART_OF_DAY + '\\s+' + DAY_N_MONTH_N_YEAR
])

FROM = 'с\\s+' + alt_b([
    FROM_COMPLEX,
    FROM_DAY_N_MONTH_N_YEAR,
    FROM_YEAR_N_MONTH,
    FROM_DAY_N_MONTH,
    FROM_YEAR_ONLY,
    FROM_MONTH_ONLY,
    FROM_WEEK_ONLY,
    FROM_PART_OF_DAY,
    FROM_DAY_OF_WEEK
])  # с прошлой недели

TO = 'до\\s+' + alt_b([
    FROM_COMPLEX,
    FROM_DAY_N_MONTH_N_YEAR,
    FROM_YEAR_N_MONTH,
    FROM_DAY_N_MONTH,
    FROM_YEAR_ONLY,
    FROM_MONTH_ONLY,
    FROM_WEEK_ONLY,
    FROM_PART_OF_DAY,
    FROM_DAY_OF_WEEK
])  # до этой недели

DATE_REGEXP = alt_b([
    FROM,
    TO,
    COMPLEX,
    DAY_N_MONTH_N_YEAR,
    YEAR_N_MONTH,
    DAY_N_MONTH,
    DAY_OF_WEEK,
    PART_OF_DAY,
    WEEK_ONLY,
    MONTH_ONLY,
    YEAR_ONLY    
])
DATE_REGEXP = '(?i)' + DATE_REGEXP

print(DATE_REGEXP)
