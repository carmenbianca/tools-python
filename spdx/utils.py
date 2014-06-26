# Copyright 2014 Ahmed H. Ismail

#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
import re
import datetime
import document
from ply import yacc, lex


def datetime_iso_format(date):
    return "{0:0>4}-{1:0>2}-{2:0>2}T{3:0>2}:{4:0>2}:{5:0>2}Z".format(
        date.year, date.month, date.day, date.hour,
        date.minute, date.second)

DATE_ISO_REGEX = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)T(\d\d):(\d\d):(\d\d)Z',
                            re.UNICODE)
DATE_ISO_YEAR_GRP = 1
DATE_ISO_MONTH_GRP = 2
DATE_ISO_DAY_GRP = 3
DATE_ISO_HOUR_GRP = 4
DATE_ISO_MIN_GRP = 5
DATE_ISO_SEC_GRP = 6


def datetime_from_iso_format(string):
    match = DATE_ISO_REGEX.match(string)
    if match:
        date = datetime.datetime(year=int(match.group(DATE_ISO_YEAR_GRP)),
                                 month=int(match.group(DATE_ISO_MONTH_GRP)),
                                 day=int(match.group(DATE_ISO_DAY_GRP)),
                                 hour=int(match.group(DATE_ISO_HOUR_GRP)),
                                 second=int(match.group(DATE_ISO_SEC_GRP)),
                                 minute=int(match.group(DATE_ISO_MIN_GRP)))
        return date
    else:
        return None


class NoAssert(object):
    pass


class LicenseListLexer(object):

    def __init__(self):
        super(LicenseListLexer, self).__init__()

    tokens = ['LP', 'RP', 'AND', 'OR', 'LICENSE']

    def t_LP(self, t):
        r'\('
        return t

    def t_RP(self, t):
        r'\)'
        return t

    def t_AND(self, t):
        r'\sand\s'
        t.value = t.value.strip()
        return t

    def t_OR(self, t):
        r'\sor\s'
        t.value = t.value.strip()
        return t

    def t_whitespace(self, t):
        r'\s+'
        pass

    def t_LICENSE(self, t):
        r'[A-Za-z.0-9\-]+'
        t.value = t.value.strip()
        return t

    def t_error(self, t):
        pass

    def input(self, data):
        self.lexer.input(data)

    def token(self):
        return self.lexer.token()

    def build(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)


class LicenseListParser(object):

    def __init__(self):
        super(LicenseListParser, self).__init__()
        self.lex = LicenseListLexer()
        self.lex.build(reflags=re.UNICODE)
        self.tokens = self.lex.tokens

    def p_license_list_1(self, p):
        """license_list : LP conjuctions RP 
                        | LP disjunctions RP
        """
        p[0] = p[2]

    def p_license_list_2(self, p):
        """license_list : error"""
        p[0] = None

    def p_conjuctions_1(self, p):
        """conjuctions : conjuctions conjuction"""
        p[0] = document.LicenseConjuction(p[1], p[2])

    def p_conjuctions_2(self, p):
        """conjuctions : conjuction"""
        p[0] = p[1]

    def p_disjunctions_1(self, p):
        """disjunctions : disjunctions disjunction"""
        p[0] = document.LicenseDisjunction(p[1], p[2])

    def p_disjunctions_2(self, p):
        """disjunctions : disjunction"""
        p[0] = p[1]

    def p_conjuction(self, p):
        """conjuction : license AND license"""
        p[0] = document.LicenseConjuction(p[1], p[3])

    def p_disjunction(self, p):
        """disjunction : license OR license"""
        p[0] = document.LicenseDisjunction(p[1], p[3])

    def p_license(self, p):
        """license : LICENSE"""
        p[0] = document.License.from_identifier(p[1])

    def p_error(self, p):
        pass

    def build(self, **kwargs):
        self.yacc = yacc.yacc(module=self, **kwargs)

    def parse(self, data):
        try:
            return self.yacc.parse(data, lexer=self.lex)
        except:
            return None
