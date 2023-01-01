# Question 7 #########################################################
EOI    = 0      #End of input
TRUE   = 1      #Constant True - True
FALSE  = 2      #Constant False - False
VAR    = 3      #a multi-character identifier of uppercase, lowercase or number combination -- $[0-9a-zA-Z]*
EQ     = 4      #character \=
AND    = 5      #Binary Operator "and"
OR     = 6      #Binary Operator "or"
NOT    = 7      #Unary Operator "not"
LP     = 8      #character \(
RP     = 9      #character \)
ERR    = 10     #Showing Error
# End of Question 7 #########################################################

# Question 8 #########################################################
# prog    -> VAR tail1 | {TRUE FALSE} tail2 | NOT term tail2 | LP expr RP
# tail1   -> EQ expr | {AND OR} term tail2 | epsilon
# expr    -> term tail2
# tail2   -> {AND OR} term tail2 | epsilon
# term    -> LP expr RP | NOT term | TRUE | FALSE | VAR
# End of Question 8 #########################################################


import sys
debug = False

def show(indent,name,s,spp):
    if debug:
        print(indent+name+'("',end='')
        j = len(s)
        for i in range(spp,j):
            print(s[i],sep="",end="")
        print('")',end='\n')
        return
    else:
        return
#end show

def x(indent,name1,name2):
    if debug:
        print(indent+"returned to "+name1+" from "+name2)
    else:
        return
#end x

def EatWhiteSpace(s,spp):
    j = len(s)
    if spp >= j:
        return spp

    while s[spp] == ' ' or s[spp] == '\n':
        spp=spp+1
        if spp >= j:
            break
        
    return spp
#end EatWhiteSpace


# prog -> VAR tail1 | {TRUE FALSE} tail2 | NOT {VAR TRUE FALSE} tail2 | LP expr RP 
# function prog ------------------------------------------------------------
def prog(s,spp,indent):
    show(indent,'prog',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == VAR:
        spp = ConsumeToken(s,spp)
        res,spp = tail1(s,spp,indent1)
        x(indent1,"prog","tail1")
        return res,spp
    elif token == TRUE or token == FALSE:
        spp = ConsumeToken(s,spp)
        res,spp = tail2(s,spp,indent1)
        x(indent1,"prog","tail2")
        return res,spp
    elif token == NOT:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"prog","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"prog","tail2")
        return res,spp
    elif token == LP:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"prog","expr")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp)
        return (token == RP),spp
    else:
        return True,spp
#end prog

# tail1 -> EQ expr | {AND OR} term tail2 | epsilon
# function tail1 --------------------------------------------------------
def tail1(s,spp,indent):
    show(indent,'tail1',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == EQ:
        spp = ConsumeToken(s,spp)
        res,spp = expr(s,spp,indent1)
        x(indent1,"tail1","expr")
        return res,spp
    elif token == AND or token == OR:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"tail1","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"tail1","tail2")
        return res,spp
    else:
        return True,spp  #epsilon
#end tail1

# expr -> term tail2
# function expr --------------------------------------------- 
def expr(s,spp,indent):
    show(indent,'expr',s,spp)
    indent1 = indent+' '

    res,spp = term(s,spp,indent1)
    x(indent1,"expr","term")
    if not res:
        return False,spp
    res,spp = tail2(s,spp,indent1)
    x(indent1,"expr","tail2")
    return res,spp
#end expr

# tail2 -> {AND OR} term tail2 | epsilon
# function tail2 --------------------------------------------- 
def tail2(s,spp,indent):
    show(indent,'tail2',s,spp)
    indent1 = indent+' '

    token = LookAhead(s,spp)
    if token == AND or token == OR:
        spp = ConsumeToken(s,spp)
        res,spp = term(s,spp,indent1)
        x(indent1,"tail2","term")
        if not res:
            return False,spp
        res,spp = tail2(s,spp,indent1)
        x(indent1,"tail2","tail2")
        return res,spp
    else:
        return True,spp  #epsilon
#end tail2

# term -> LP expr RP | NOT term | TRUE | FALSE | VAR
# function term --------------------------------------------- 
def term(s,spp,indent):
    show(indent,'term',s,spp)
    indent1 = indent+' '

    token,spp = NextToken(s,spp)
    if token == LP:
        res,spp = expr(s,spp,indent1)
        x(indent1,"term","expr")
        if not res:
            return False,spp
        token,spp = NextToken(s,spp)
        return (token == RP),spp
    elif token == NOT:
        res,spp = term(s,spp,indent1)
        x(indent1,"term","expr")
        return res,spp
    elif token == TRUE or token == FALSE or token == VAR:
        return True,spp
    else:
        return False,spp
#end term

# function LookAhead ------------------------------------------- 
def LookAhead(s,spp):
    j = len(s)
    i = spp
    
    if i >= j:
        return EOI
    while s[i]==" " or s[i]=="\n":
        i = i + 1
        if i >= j:
            return EOI

    if s[i: i + 3] == 'and':
        return AND
    elif s[i: i + 2] == "or":
        return OR
    elif s[i: i + 3] == "not":
        return NOT
    elif s[i] == "(":
        return LP
    elif s[i] == ")":
        return RP
    elif s[i: i + 4] == "True":
        return TRUE
    elif s[i: i + 5] == "False":
        return FALSE
    elif s[i] == "=":
        return EQ
    elif s[i] == "$":
        return VAR
    else:
        return ERR

# function NextToken --------------------------------------------- 
def NextToken(s,spp):
    spp1 = spp
    spp = EatWhiteSpace(s,spp)
    j = len(s)
    l = 1
    if spp >= j:
        return ERR,spp1
    
    if spp >= j:
        return EOI, spp
    elif s[spp: spp + 3] == 'and':
        return AND, spp + 3
    elif s[spp: spp + 2] == "or":
        return OR, spp + 2
    elif s[spp: spp + 3] == "not":
        return NOT, spp + 3
    elif s[spp] == "(":
        return LP, spp + 1
    elif s[spp] == ")":
        return RP, spp + 1
    elif s[spp:spp + 4] == "True":
        return TRUE, spp + 4
    elif s[spp:spp + 5] == "False":
        return FALSE, spp + 5
    elif s[spp] == "=":
        return EQ, spp + 1
    elif s[spp] == "$":
        res,spp = Lvar(s,spp+1)
        if not res:
            return ERR,spp1
        if spp >= j:
            return True,spp
        return VAR,spp
    else:
        return ERR, spp1
#end NextToken

# function lvar -------------------------------------------- 
def Lvar(s,spp):
    
    j = len(s)
    i = 0
    
    while i<100 :
        if spp < j and ((ord(s[spp]) >= ord('0') and ord(s[spp]) <= ord('9')) or 
                        (ord(s[spp])>=ord('A') and ord(s[spp])<=ord('Z'))     or 
                        (ord(s[spp])>=ord('a') and ord(s[spp])<=ord('z'))):
            spp = spp+1
            if spp >= j:
                break
            i = i+1
        else:
            break

    return True,spp


#end lvar

def ConsumeToken(s,spp):
    token,spp = NextToken(s,spp)
    return spp
#end ConsumeToken

s = "$A or $B = True"
res,spp = prog(s,0,"")

if spp < len(s)-1:
    print("parse Error")
else:
    if res:
        print("parsing OK")
    else:
        print("parse Error")