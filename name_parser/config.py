import re
import string


######### TOKEN CONFIG #########

# some config on how to split a string into tokens
# - set characters to split on?
# - set characters to append at the end of tokens?


######### LABEL CONFIG #########

# these are the labels for tagging tokens
LABELS = [
'PrefixMarital',
'PrefixOther',
'GivenName',
'FirstInitial',
'MiddleName',
'MiddleInitial',
'Surname',
'LastInitial',
'SuffixGenerational',
'SuffixOther',
'Nickname',
'And'
]

NULL_LABEL = 'Null'

######## XML CONFIG ############

# this is the tag for each string
PARENT_LABEL = 'Name'

# this is the tag for a group of strings
GROUP_LABEL = 'NameCollection'

######## FEATURE CONFIG ########

def tokenFeatures(token) :

    if token in (u'&') :
        token_clean = token
    else :
        token_clean = re.sub(r'(^[\W]*)|([^.\w]*$)', u'', token)
    token_abbrev = re.sub(r'[.]', u'', token_clean.lower())

    features = {'nopunc' : token_abbrev,
                'abbrev' : token_clean.endswith('.'),
                'comma'  : token.endswith(','), 
                'hyphenated' : '-' in token_clean,
                'contracted' : "'" in token_clean,
                'bracketed' : bool(re.match(r'(\W)\w+\1', token)),
                'case' : casing(token_clean),
                'length' : len(token_abbrev),
                'initial' : len(token_abbrev) == 1 and token_abbrev.isalpha(),
                'has.vowels'  : bool(set(token_abbrev[1:]) & set('aeiou')),
                }
    reversed_token = token_abbrev[::-1]
    for i in range(1, len(token_abbrev)) :
        features['prefix_%s' % i] = token_abbrev[:i]
        features['suffix_%s' % i] = reversed_token[:i][::-1]
        if i > 4 :
            break

    return features

def casing(token) :
    if token.isupper() :
        return 'upper'
    elif token.islower() :
        return 'lower' 
    elif token.istitle() :
        return 'title'
    elif token.isalpha() :
        return 'mixed'
    else :
        return False
