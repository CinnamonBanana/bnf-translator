import lexer

RESERVED = 'RESERVED'
INT      = 'INT'
ID       = 'ID'

TOKEN_BEGIN = 'Begin'
TOKEN_END = 'End'
TOKEN_REAL = 'Real'
TOKEN_INTEGER = 'Integer'

TOKEN_INT = 'Цел. Число'
TOKEN_ID = 'Переменная'

TOKEN_PLUS = '+'
TOKEN_MINUS = '-'
TOKEN_MUL = '*'
TOKEN_DIV = '/'
TOKEN_COMMA = ','
TOKEN_EQ = '='
TOKEN_DEGREE = '^'
TOKEN_COLON = ':'
TOKEN_LPAREN = '('
TOKEN_RPAREN = ')'

SKIP_SPACE = 'Пробел'
SKIP_NEW_LINE = 'Новая строка'
SKIP_TAB = 'Табуляция'

TOKEN_BOF = 'Начало документа'
TOKEN_EOF = 'Конец документа'
TOKEN_BOP = 'Начало операции'
TOKEN_BOMARK = 'Метка'

EX_VAR = r'[A-Za-z][A-Za-z0-9_]*'
EX_INT = r'[0-9]+'
EX_LITERALS = r'[A-Za-z]'
OPERATIONS = [
    TOKEN_PLUS,
    TOKEN_MINUS,
    TOKEN_DEGREE,
    TOKEN_DIV,
    TOKEN_MUL,
]
token_exprs = [
    (r'[ \n\t]+',              None),
    (r'#[^\n]*',               None),
    (r'[.,]',                     TOKEN_COMMA), 
    #(r'.',                     TOKEN_COMMA), 
    (r'\bBegin\b',                 TOKEN_BEGIN),
    (r'\bEnd\b',                   TOKEN_END),
    (r'\bReal\b',                  TOKEN_REAL),
    (r'\bInteger\b',               TOKEN_INTEGER),
    (r'\+',                    TOKEN_PLUS),
    (r'-',                     TOKEN_MINUS),
    (r'\*',                    TOKEN_MUL),
    (r'/',                     TOKEN_DIV),
    (r'\^',                    TOKEN_DEGREE),
    (r'\(',                    TOKEN_LPAREN),
    (r'\)',                    TOKEN_RPAREN),
    (r'\=',                    TOKEN_EQ),
    (r':',                     TOKEN_COLON),
    (r';',                     TOKEN_COLON),
    (r'[а-яА-ЯёЁ]+',            TOKEN_COLON),
    (EX_INT,                   INT),
    (EX_VAR,                   ID),
    ]

def imp_lex(characters):
    return lexer.lex(characters, token_exprs)
