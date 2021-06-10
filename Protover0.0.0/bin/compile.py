
#import文
import inspect, sys
from os import device_encoding
import ply.yacc as yacc
from lex import tokens

filename = sys.argv[1]

#各種リスト格納用変数初期宣言
intd = {}
strd = {}
funcd = {}
clos = {}

iflis = []
funclis = []
ast_2 = []
classlist= []
#--------

#str型定義
kataw = ""
#--------

#int型定義
iflisc = 0
ifc = 0
lisc = 0
icj = 0
#--------

#何これ
precedence = (
    ('left', 'OPTASU'),
    ('left', 'OPKAKERU'),
)

#文法一括管理
def p_teigilist_0(p):
    '''
        teigilist : teigi
                | teigilist teigi
    '''
    if (len(p) == 2):
        p[0] = (p[1])
    elif (len(p) == 3):
        p[0] = (p[1],p[2])

def p_paramlist(p):
    '''
        paramlist : param
                  | paramlist CONMA param
    '''
    if (len(p) == 2):
        p[0] = [p[1]]
    elif (len(p) == 4):
        l = p[1]
        l.append(p[3])
        p[0] = l

def p_param(p):
    '''
        param : TYPE ID
              | TYPE
    '''
    if (len(p) == 2):
        p[0] = ('PARAM',p[1])
    elif (len(p) == 3):   
        p[0] = ('PARAM',p[1],p[2])

def p_lamda(p):
    """
    bun : ID EQUALS LAMDA KAKKO paramlist KOKKA LBRACE bunlist RBRACE SEMI
    """
    p[0] = ( "LAM", p[1], p[5], p[8])

def p_call(p):
    '''
    bun : ID KAKKO shiki KOKKA SEMI
    '''
    p[0] = ( "CALL", p[1], p[3] )

def p_comment(p):
    """
    teigi : STR
    """
    p[0] = ("PASS", p[1])

def p_instance(p):
    """
    bun : ID EQUALS ID SEMI
    """
    p[0] = ( "INS", p[1], p[3])

def p_teigi_0(p):
    '''
    teigi : TYPE ID KAKKO paramlist KOKKA yaji TYPE LBRACE bunlist RBRACE
    '''
    p[0] = ('DEF',p[7],p[2],p[4],p[9])

def p_teigi_void(p):
    """
    teigi : TYPE ID yaji TYPE LBRACE bunlist RBRACE
    """
    p[0] = ('DEF',p[4],p[2],"void",p[6])

def p_teigi_1(p):
    """
    teigi : STRUCT ID LBRACE teigilist RBRACE
    """
    p[0] = ( "STRUCT", p[2], p[4] )

def p_class_f(p):
    """
    class : classf
    """
    p[0] = p[1]

def p_class_f_2(p):
    """
    class : class classf
    """
    p[0] = p[1],p[2]

def p_class(p):
    """
    teigi : CLASS ID LBRACE class RBRACE
    """
    p[0] = ( "CLASS", p[2], p[4])

def p_include(p):
    """
    teigi : INCLUDE LBRACE shiki RBRACE
    """
    p[0] = ( "include", p[3] )

def p_classfunc(p):
    """
    classf : ID KAKKO paramlist KOKKA yaji TYPE LBRACE bunlist RBRACE
    """
    p[0] = list( ("CLDEF", p[1], p[3],  p[6], p[8] ) )

def p_class_fc(p):
    """
    bun : ID PIRIOD ID KAKKO shiki KOKKA SEMI
    """
    p[0] = ( "CLINST", p[1], p[3], p[5] )

def p_pass(p):
    """
    bun : PASS SEMI
    """
    p[0] = ( "PASS", p[1] )

def p_bunlist_0(p):
    '''
    bunlist : bun
    '''
    p[0] = [p[1]]

def p_bunlist_1(p):
    '''
    bunlist : bunlist bun
    '''
    l = p[1]
    l.append(p[2])
    p[0] =  l

def p_bun_type(p):
    '''
    bun : TYPE ID  EQUALS shiki SEMI
    '''
    p[0] = ('SENGEN',p[1],p[2],p[4])

def p_bun_lis(p):
    '''
    bun : TYPE ID EQUALS LISL STR LISR SEMI
    '''
    p[0] = ( 'LISTD', p[2], p[5] )

def p_bun_deflis(p):
    """
    bun : TYPE ID EQUALS ID LISL shiki LISR SEMI
    """
    p[0] = ( 'LISTARG', p[2], p[4], p[6], p[1] )

def p_bun_newlis(p):
    """
    bun : ID EQUALS LISL LISR SEMI
    """
    p[0] = ( "NEWLIS", p[2])

def p_add(p):
    '''
    bun : ID EQUALS ID OPTASU NUMBER SEMI
        | ID EQUALS ID OPKAKERU NUMBER SEMI
        | ID EQUALS ID OPMIN NUMBER SEMI
        | ID EQUALS ID OPWARU NUMBER SEMI
    '''
    p[0] = ( 'DAINYU', p[1], p[3], p[4], p[5] )


def p_shiki_type(p):
    """
    shiki : TYPEF KAKKO shiki KOKKA
    """
    p[0] = ("TYPEF", p[3])

def p_shiki_int(p):
    """
    shiki : TYPE KAKKO shiki KOKKA
    """
    p[0] = ( "CONVT", p[1], p[3] )

def p_shiki_input(p):
    """
    shiki : RESERV KAKKO shiki KOKKA
    """
    p[0] = ( "INPUT", p[3])

def p_bun_return(p):
    '''
    bun : RETURN shiki SEMI
        | RETURN bun
    '''
    p[0] = ('RETURN',p[2])

def p_bun_if1(p):
    '''
    bun : IF hikaku LBRACE bunlist RBRACE 
    '''
    p[0] = ('IF',p[2],p[4])

def p_bun_if2(p):
    '''
    bun : IF hikaku LBRACE bunlist RBRACE ELSE LBRACE bunlist RBRACE
    '''
    p[0] = ('IF-ELSE',p[2],p[4],p[8])

def p_bun_while(p):
    '''
    bun : WHILE shiki LBRACE bunlist RBRACE 
    '''
    p[0] = ( 'WHILE', p[2], p[4] )

def p_hikaku_1(p):
    '''
    hikaku : shiki
    '''
    p[0] = ('exp',p[1])

def p_hikaku_2(p):
    '''
     hikaku : hikaku EQOP shiki
            | hikaku dainari shiki
            | hikaku syounari shiki
    '''
    p[0] = ('HIKAKU1',p[1],p[2],p[3])

def p_shiki_num(p):
    '''
    shiki : NUMBER
    '''
    p[0] = ('NUM',p[1])

def p_shiki_id(p):
    '''
    shiki : ID
    '''
    p[0] = ('ID',p[1])

def p_shiki_void(p):
    """
    shiki : TYPE
    """
    p[0] = ( "TYPE", p[1] )

def p_shiki_str(p):
    '''
    shiki : STR
    '''
    p[0] = ('STR',p[1])

def p_shiki_pass(p):
    '''
    bun : PASS 
        | PASS KAKKO KOKKA
        | PASS KAKKO PASS KOKKA SEMI
    '''
    p[0] = ('PASS',p[1])

def p_shiki_MINNUM(p):
    """
    shiki : OPMIN NUMBER
    """
    p[0] = "-"+p[1]

def p_shiki_enzan(p):
    '''
    shiki : shiki OPTASU shiki
          | shiki OPKAKERU shiki
          | shiki OPMIN shiki
          | shiki OPWARU shiki
    '''
    p[0] = ( "shiki", p[1], p[2], p[3] )

def p_shiki_kakko(p):
    '''
    shiki : KAKKO shiki KOKKA
    '''
    p[0] = ('exp',p[2])

def p_shiki_args(p):
    """
    shiki : shiki CONMA ID       
    """
    if len( p[1][0][0] ) > 1:
        p[0] = list( p[1] ) + [ ( "ID", p[3] ) ]
    else:
        p[0] =  ( p[1] ), ("ID", p[3])

def p_insert(p):
    """
    bun : RESERV ID LISL NUMBER LISR EQUALS STR SEMI
        | RESERV ID LISL ID LISR EQUALS STR SEMI
        | RESERV ID LISL NUMBER LISR EQUALS ID SEMI
        | RESERV ID LISL ID LISR EQUALS ID SEMI
    """
    p[0] = ( "RES", p[1], p[2], p[4], p[7] )

def p_reserv (p):
    '''
    bun : RESERV KAKKO shiki KOKKA SEMI
    '''
    p[0] = ( "RES",p[1],p[3] )

def p_shiki_func_ret(p):
    """
    shiki : ID KAKKO shiki KOKKA
    """
    p[0] = ("CALL", p[1], p[3])

def p_shiki_call_void(p):
    '''
    shiki : ID KAKKO KOKKA
    '''
    p[0] = ( "CALL", p[1], "void" )

def p_lets(p):
    """
    bun : TYPE TYPE LBRACE letlist RBRACE SEMI
    """
    p[0] = ( "LETS", p[2], p[4] )

def p_letsglobal(p):
    """
    bun : GLOBAL TYPE LBRACE letlist RBRACE SEMI
    """
    p[0] = ( "GLOBAL", p[2], p[4])

def p_letslis(p):
    """ 
    letlist : ID EQUALS STR SEMI 
            | ID EQUALS NUMBER SEMI 
            | letlist ID EQUALS STR SEMI
            | letlist ID EQUALS NUMBER SEMI
    """
    if type(p[1]) != tuple: 
        p[0] = ( p[1], p[3] )
    else:
        p[0] = [ p[1], (p[2], p[4])]

def p_str_add(p):
    """
    bun : ID EQUALS ID OPTASU STR SEMI
        | ID EQUALS STR OPTASU ID SEMI
    """
    p[0] = ( "STRADD", p[1], p[3], p[5] )

def p_add_add_num(p):
    """
    bun : ID OPTASU OPTASU SEMI
        | STR OPTASU OPTASU SEMI
    """
    p[0] = ('OPSTR',p[1],p[2],p[1])

# syntax error
def p_error(p):
    print ('SyntaxErr : すみません、 %sに当てはまる文法作るのやめてもらっていいすか？' % p)

parser = yacc.yacc()

class CodeGenartor:
    #file書き込みやそのための文字列作成など
    mList = []

    global icj, funclis

    def __init__( self ):
        self.ifcj = icj

    def append(self , line):
        self.mList.append(line)
    
    def out_put( self ):
        wfile =  open ( filename+"s", "a", encoding="utf_8")
        wfile.truncate(0) 
        for item in self.mList:
            print ("".join( item), file=wfile)
    
    def add_define( self , info ):
        self.append( ["\n"+info['funcname']+':'] )
    
    def add_return( self , info ):
        self.append( ['','end;\ncb;\n'] )
        #TODO : end;cb;
        for name in iflis:
            self.if_write( name, funcd )
        
        for name in funclis:
            self.f_write( name, funcd )

    def f_write( self, nameandarg, funcd ):
        name =  nameandarg.split( ":" )[0]
        arg =  nameandarg.split( ":" )[1]
        if arg != "void":
            args = ""
            self.append( [ '',"\n"+name+"("+arg.replace( " ", "" ).replace( "and", "" )+"):" ] )
            arg = arg.split( " and " )
            for item in arg:
                if item != "":
                    self.add_vall( item.split( " " )[0], item.split( " " )[1] )
                args += item
        else:
            self.append( [ '',"\n"+name+"():" ] )
        for item in funcd[name]:
            walker.step2( item )
        self.append( ['','end;\ncb;\n'] )

    def if_write( self, name, dic ):
        self.append( [ '',"\n"+name+"():" ] )
        for item in funcd[name][6:]:
            walker.step2( item )

    def add_num( self , info, arg, mode ):
        self.append( ['',"mode>"+mode+";\n"+"mov "+arg+" "+info[arg]+";" ])
    
    def add_deflis( self, arg, vall, mode, index ):
        self.append( ['',"mode>"+mode+";\n"+"mov "+arg+", "+vall+"["+index+"]"+";" ])

    def add_sym( self , arg, funcname ):
        self.append( ["ret "+funcname+", "+arg+";" ])
    
    def add_fode( self, fode ):
        self.append( [ '',"fode>"+fode+";" ] )

    def add_call ( self, name, vall ):
        self.append( [ "", "call "+name+"["+vall+"];" ] )

    def add_msg ( self, word ):
        self.append( [ "", "msg "+word+";" ])
    
    def add_input ( self, word ):
        self.append( [ "", "input "+word+";" ])

    def add_dainyu( self, ast ):
        if ast[3] == "+":
            self.append( ['','mode>int;\nadd ',ast[2],", ",ast[4],";\nmov ", ast[1], ", ", ast[2],";"] )
        
        if ast[3] == "-":
            self.append( ['','mode>int;\nsub ',ast[2],", ",ast[4],";\nmov ", ast[1], ", ", ast[2],";"] )
        
        if ast[3] == "*":
            self.append( ['','mode>int;\ndev ',ast[2],", ",ast[4],";\nmov ", ast[1], ", ", ast[2],";"] )
        
        if ast[3] == "/":
            self.append( ['','mode>int;\nmul ',ast[2],", ",ast[4],";\nmov ", ast[1], ", ", ast[2],";"] )
    
    def add_ifcall( self, word ):
        self.append( ['', word ] )
    
    def add_if ( self, name ):
        self.append( ['', name +"():\n"+funcd[name] ] )
    
    def add_while( self, loopn ):
        self.append( ['', "jmp "+str( loopn )+", L"+str( ifc )+";" ] )

    def add_vall( self, mode, data ):
        self.append( ['',"mode>"+mode+";\n"+"pop "+data+";" ] )

    def add_lis( self, ast ):
        self.append( [ '', "mode>lis;\nmov "+ast[1]+", "+ast[2]+";" ] )

    def add_insert( self, lisn, index, STR ):
        self.append( [ '', "mode>lisin;\nmov "+lisn+"["+index+"], "+STR+";" ] )

#codegenインスタンスを作成
codegen = CodeGenartor()

def if_j( x, y, mode, kata ):
    if kata == "int":
        if mode == "==":
            if x in intd and y in intd and intd[x] == intd[y]:
                return 0
            elif x in intd and intd[x] == int( y ):
                return 0
            elif y in intd and intd[ y ] == int( x ):
                return 0
        elif mode == ">":
            if x in intd and y in intd and intd[x] > intd[y]:
                return 0
            elif x in intd and intd[x] > int( y ):
                return 0
            elif y in intd and intd[ y ] > int( x ):
                return 0
        elif mode == "<":
            if x in intd and y in intd and intd[x] < intd[y]:
                return 0
            elif x in intd and intd[x] < int( y ):
                return 0
            elif y in intd and intd[ y ] < int( x ):
                return 0
    elif kata == "str":
        if x[0] == "ID":
            x = strd[x[1]].replace( "\"", "'" ).replace( "' ", "" ).replace("'", "")
            y = y.replace( "\"", "'" ).replace("' ", "").replace( "'", "" )
            if x == y:
                return 0
        if y in strd:
            x = x.replace( "\"", "'" ).replace( "'", "" )
            y = strd[y].replace( "\"", "'" ).replace( "'", "" )
            if x == y:
                return 0
        else:
            return 1

class Calc:
    #各種四則演算計算用
    def __init__( self, ast ):
        self.ast = ast
    
    def first( self ):

        if self.ast[2] == "+":
            ret = self.plus()
        elif self.ast[2] == "-":
            self.min()
        return ret
    
    def plus( self ):
        if self.ast[1][0] == "NUM" or self.ast[3][0] == "NUM":
            formula = int(self.ast[1][1]) + int(self.ast[3][1])
        return formula
    
    def min( self ):
        if self.ast[1][0] == "NUM" or self.ast[3][0] == "NUM":
            formula = int(self.ast[1][1]) - int(self.ast[3][1])
        return formula

class Walker:

    def walk(self,ast):
        #step2に移動用。
        self.step2( ast )

    def step2(self,ast):

        global  funcname, mode, funclis, kataw, ifc, iflisc, lisc, ast_2, funcd, classlist, clos
        
        if ast[0] == 'exp':
            self.step2(ast[1])
        
        elif ast[0] == 'LISTD':
            codegen.add_lis( ast )

        elif ast[0] == "PASS":
            pass

        elif ast[0] == 'DEF':

            funcname = ast[2]
            size = 0
            vallw = ""

            try:
                for item in ast[3]:
                    vallw += item[1]+item[2]
                    size+=1
            except IndexError:
                    pass
                
            funcd[ast[2]] = ast[2:]
            codegen.add_define({'funcname':ast[2]+"("+vallw+")", 'localvarsize':size })

            codegen.append( ["", "fode>"+ast[1]+";"] )
            for item in ast[3]:
                self.step2(item)
            for item in ast[4]:
                self.step2(item)

            codegen.add_return({'funcname':ast[2]})

        elif ast[0] == 'ID':
            pass
            #codegen.add_sym( ast[1], funcname)
        
        elif ast[0] == "WHILE":
            add = []
            codegen.add_while( ast[1][1] )
            for item in ast:
                add += item
            funcd["L"+str( ifc )] = (add)
            iflis.append( "L"+str( ifc ) )
            ifc+=1

        elif ast[0] == "HIKAKU1":
            if ast[2] == "==":
                jmode = "je"
            elif ast[2] == "<":
                jmode = "ja"
            elif ast[2] == ">":
                jmode = "jne"
            ifword = jmode+" "+ast[1][1][1]+", "+ast[3][1].replace( "\" ", "\"" )+", L"+str( ifc )+";"
            codegen.add_ifcall( ifword )

        elif ast[0] == 'IF':
            add = []
            self.step2(ast[0:2][1])#TODO : HIAKAKU
            for item in ast:
                add += item
            funcd["L"+str( ifc )] = (add)
            iflis.append( "L"+str( ifc ) )
            ifc+=1

        elif ast[0] == 'DAINYU':
            codegen.add_dainyu( ast )

        elif ast[0] == "LISTARG":
            codegen.add_deflis(ast[1], ast[2], "ind", ast[3] )
        
        elif ast[0] == 'PARAM':
            try:
                if ast[1] == "int":
                    codegen.add_vall(  ast[1], ast[2] )
                
                if ast[1] == "str":
                    codegen.add_vall(  ast[1], ast[2] )
            except IndexError:
                pass

        elif ast[0] == "CALL":
            size = 0
            vallw = ""

            self.step2(ast[2])
            if ast[2][0] == "OP":
                codegen.add_call( ast[1], ast[2][1][1] )
            else:
                if ast[2][0][0] == "ID":
                    codegen.add_call( ast[1], ast[2][0][1]+", "+ast[2][1] )
                else:
                    codegen.add_call( ast[1], ast[2][1] )
            
            try:
                try:
                    for item in funcd[ast[1]][1] :
                        if item[1] != "void":
                            vallw += item[1]+item[2]
                        else:
                            vallw += "void"
                except IndexError:
                    for item in funcd[ast[1]]:
                        if type(item) != tuple:
                            vallw = ""
                        else:
                            vallw = item[1]+item[2]
            except KeyError:
                print("DefineErr："+ast[1]+"？なんすか、"+ast[1]+"って")
            
            #codegen.add_define({'funcname':ast[1]+"("+vallw+")", 'localvarsize':size })

        elif ast[0] == "RES":
            if ast[1] == "put":
                if type(ast[2]) == tuple:
                    self.step2(ast[2])
                    codegen.add_msg( ast[2][1] )
                    codegen.add_msg( "\"\\n\"" )
                else:
                    codegen.add_msg( ast[2] )
                    codegen.add_msg( "\"\\n\"" )
            elif ast[1] == "msg":
                codegen.add_msg( ast[2] )
            elif ast[1] == "input":
                codegen.add_input( ast[2] )
            elif ast[1] == "insert":
                codegen.add_insert( ast[2], ast[3], ast[4] )

        elif ast[0] == "RESF":
            l = []
            l.append( "CALL" )
            l.append( ast[1] )
            l.append( ast[2] )
            self.step2( l )
            l = []
            l.append( "RES" )
            l.append( "put" )
            l.append( ast[1] )
            self.step2( l )

        elif ast[0] == 'SENGEN':
            mode = ast[1]
            if mode == "int":
                if ast[3][0] == "shiki":
                    intd[ast[2]] = Calc(ast[3]).first()
                    codegen.append( ['',"mode>int;\n"+"mov "+ast[2]+" "+str(Calc(ast[3]).first())+";" ])
                else:
                    intd[ast[2]] = int( ast[3][1] )
                    codegen.add_num({ast[2]:ast[3][1]}, ast[2], ast[1])
            if mode == "str":
                strd[ast[2]] = ast[3]
                if (ast[3][0] == "TYPEF"):
                    codegen.append( ["", "mode>type;\nmov "+ast[2]+" "+ast[3][1][1]+";"] )
                elif ast[3][0] == "CONVT":
                    codegen.append( ["", "mode>con"+ast[3][1]+";\nmov "+ast[2]+" "+ast[3][2][1]+";"] )
                elif ast[3][0] == "INPUT":
                    tu = ( "RES", "input", ast[3][1][1] )
                    self.step2(tu)
                    codegen.append( ["", "mode>str;\nmov "+ast[2]+" "+ast[3][1][1]+";"] )
                else:
                    codegen.append( ["", "mode>str;\nmov "+ast[2]+" "+ast[3][1]+";"] )

        elif ast[0] == 'RETURN':
            self.step2( ast[1] )
            if type( ast[1][1] ) == tuple:
                codegen.add_sym( ast[1][1][1], funcname )
            else:
                codegen.add_sym( ast[1][1], funcname )

        elif ast[0] == "LAM":
            add = []
            arg = ""
            for item in ast[2]:
                if item[1] == "void":
                    break
                else:
                    arg += item[1]+" "+item[2]+" "
            funcd[ast[1]] = ast[3]
            funclis.append( ast[1]+":"+arg )
        
        elif ast[0] == "OP":
            item = ast[1:]
            for item2 in item:
                self.step2(item2)
            if ast[2] == "+":
                op = "add "

            elif ast[2] == "-":
                op = "sub "
            
            elif ast[2] == "*":
                op = "dev "
            
            elif ast[2] == "/":
                op = "mull "
            codegen.append( [ op+ast[1][1]+", "+ast[3][1]+";" ] )

        elif ast[0] == "OPSTR":
            codegen.append( [ "add "+ast[1]+", 1;" ] )

        elif ast[0] == "NEWLIS":
            codegen.add_lis(["", ast[1], "\"\""])

        elif ast[0] == "LETS":
            for msd in ast[2]:
                item = ( "SENGEN", ast[1], msd[0], msd[1] )
                self.step2(item)

        elif ast[0] == "GLOBAL":

            if type( ast[2][0] ) != str:
                for msd in ast[2]:
                    item = ( "SEG", ast[1], msd[0], msd[1] )
                    self.step2(item)
            else:
                self.step2( ( "SEG", ast[2][0], ast[2][1] ) )
        
        elif ast[0] == "SEG":
            codegen.append( ["", "mode>global"+ast[1]+";\nmov "+ast[2], " "+ast[3]+";"] )

        elif ast[0] == "STRADD":
            codegen.append( [ "stradd "+ast[2]+", "+ast[3]+";\nmov "+ast[1]+", "+ast[2]+";" ] )

        elif ast[0] == "STRUCT":

            codegen.append( [ "", "mode>struct;\nname "+ast[1]+";" ] )
            for item in ast[2]:
                self.step2(item)
            codegen.append( [ "", "end;" ] )

        elif ast[0] == "CLINST":
            arg = ""
            for item in ast[3]:
                if item[0] == "ID":
                    arg += item[1]+", "
                else:
                    arg = item
            codegen.append( ["", "class>"+ast[1]+" "+ast[2]+"["+arg+"];"] )
        
        elif ast[0] == "CLASS":
            codegen.append( ["", ast[1]+"():"] )
            if type ( ast[2] ) != list:
                for item in ast[2]:
                    self.step2( item )
            else:
                self.step2( ast[2] )
            codegen.append("end;\ncd;")

        elif ast[0] == "INS":
            codegen.append( ["", "inst "+ast[1]+", "+ast[2]+";"] )
        
        elif ast[0] == "CLDEF":
            hikisu = ""
            for item in ast[2]:
                hikisu = hikisu + item[2] + " and "
            codegen.append( ["", "in>"+ast[1]+"["+hikisu+"];"] )

            funcname = ast[1]
            size = 0
            vallw = ""

            try:
                for item in ast[2]:
                    if item[1] == "void":
                        vallw = "void"
                    else:
                        vallw += item[1]+" "+item[2]+" and "
                        size+=1
            except IndexError:
                    pass
            
            funclis.append(ast[1]+":"+vallw)
            funcd[ast[1]] = ast[4]

        elif type(ast[0]) == tuple:
            for item in ast:
                self.step2(item)

walker = Walker()


if __name__ == '__main__':  
    file = open ( filename, "r", encoding="utf_8" )
    data = ""
    for item in file:
        if item.startswith("class "):
            item = item.replace( "class ", "fnclass " )
        elif item.startswith( "include " ):
            item = item.replace( "include ", "fninclude " )
        data += item
    file = data.replace( "\n", "" )
    for i in range ( len( file.split( "fn" ) ) ):
        if file.split("fn")[i] != "":
            result = parser.parse( "fn"+file.split("fn")[i] )
            if result != None:
                walker.walk(result)
                codegen.out_put()
