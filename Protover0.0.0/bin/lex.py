import ply.lex as lex

#トークンの定義
tokens = (
    'NUMBER',
    'OPTASU',
    'OPKAKERU',
    'OPMIN',
    'OPWARU',
    'KAKKO',
    'KOKKA',
    'ID',
    'EQUALS',
    'SEMI',
    'IF',
    'ELSE',
    'WHILE',
    'LBRACE',
    'RBRACE',
    'LISL',
    'LISR',
    'EQOP',
    'TYPE',
    'CONMA',
    'RETURN',
    'yaji',
    'colon',
    'RESERV',
    'dainari',
    'syounari',
    'STR',
    'PASS',
    'INCLUDE',
    'CLASS',
    'STRUCT',
    'LAMDA',
    "PIRIOD",
    "GLOBAL",
    "TYPEF",
)

#int型変数の宣言。
strc = 0
comc = 0
lisc = 0

#正規表現一発で済ませられるtokenの定義。
t_NUMBER = r'\d+'
t_OPTASU = r'\+'
t_OPKAKERU = r'\*'
t_OPWARU = r'\/'
t_OPMIN = r'\-'
t_KAKKO = r'\('
t_KOKKA = r'\)'

t_ignore = ' \t'
t_EQUALS = r'='
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_LISL = r'\['

t_yaji = r"\=>"
t_colon = r":"
t_EQOP   = r'=='
t_dainari = r"\>"
t_syounari = r"\<"
t_PIRIOD = r"\."


#セミコロン（；）の判別のための関数。
def t_SEMI(t):
    r'\;'
    t.type = "SEMI"
    return t

#LISR（]）の判別のための関数。
def t_LISR(t):
    r'\]'
    global lisc
    lisc = 0
    return t

#STR（文字列）の判定用の関数。
def t_STR(t):
    r'[\/\/*\"\'!][ 0-9a-zA-Z_$,.><\\ \/\"\'!\?\():\*/]*'
    global strc, comc, lisc
    if t.value.startswith( "\"" ) or t.value.startswith( "'" ):
        t.type = "STR"
        strc += 1
    if t.value == "/*":
        comc += 1
        t.type = "PASS"
    if t.value == "*/":
        comc += 1
        t.type = "PASS"
    if t.value.startswith( "//" ):
        t.type = "PASS"
    else:
        strc -= 0
    return t

#struct構文の関数。いらない。
def t_STRUCT(t):
    r"fnstruct"
    return t

def t_ID(t):
    r'[@\,a-zA-Z_$\!][0-9a-zA-Z_$,\"\'!\?]*'
    global strc, comc, lisc
    if lisc != 0:
        t.type = "LIST"
    elif t.value == ";":
        t.type == "SEMI"
    elif t.value == "/*":
        comc += 1
        t.type = "PASS"
    elif t.value == "*/":
        comc += 1
        t.type = "PASS"
    
    elif t.value == "pass":
        t.type = "PASS"
    
    elif str(comc/2).split("." )[1] == "5":
        t.type = "PASS"
    else:
        if t.value == 'if':
            t.type = 'IF'
        elif t.value == 'else':
            t.type = 'ELSE'
        elif t.value == "while":
            t.type = "WHILE"
        elif t.value == "global":
            t.type = "GLOBAL"
        elif t.value == "fninclude":
            t.type = "INCLUDE"
        elif t.value == "class":
            t.type = "TYPE"
        elif t.value == "fnclass":
            t.type = "CLASS"
        elif t.value == "lamda":
            t.type = "LAMDA"
        elif t.value == ",":
            t.type = "CONMA"
        elif t.value == "and":
            t.type = "CONMA"
        elif t.value == 'int':
            t.type = 'TYPE'
        elif t.value == 'str':
            t.type = 'TYPE'
        elif t.value == 'void':
            t.type = 'TYPE'
        elif t.value == "lis":
            t.type = "TYPE"
            lisc += 1
        elif t.value == "let":
            t.type = "TYPE"
        elif t.value == "fn":
            t.type = "TYPE"
        elif t.value == 'return':
            t.type = 'RETURN'
        elif t.value == "insert":
            t.type = "RESERV"
        elif t.value == "msg":
            t.type = "RESERV"
        elif t.value == "put":
            t.type = "RESERV"
        elif t.value == "input":
            t.type = "RESERV"
        elif t.value == "type":
            t.type = "TYPEF"
        else:
            t.value = t.value.split( ";" )[0]
    return t

def t_error(t):
    print("LexErr：%s。それ、あなたの感想ですよね？" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

## 
lexer = lex.lex(debug=0)