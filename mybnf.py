import sys, re
from tkinter import Tk
from imp_lex import *
from window import BNFWindow
from utils import *

def error(_curr, text):
    text = "Ошибка. " + text
    window.set_con(text)
    strnum, startch, endch = highlighter(_curr, window.code.get(1.0, 'end'))
    strnum+=1
    print("Word on: ", f'{strnum}.{startch}', f'{strnum}.{endch}')
    window.code.tag_configure("highlight", background="red", foreground="white")
    window.code.tag_add("highlight", f'{strnum}.{startch}', f'{strnum}.{endch}')
    raise Exception(text)

global variables
variables={}

def block_3(tokens, _curr):
    global variables

    if get_type(tokens[_curr], False, True)=='var':
        if (get_type(tokens[_curr-1], False, True) or tokens[_curr-1] in ')') and tokens[_curr-1]!=TOKEN_EQ:
            error(_curr-1, text="Нет знака между членами выражения!")
        if tokens[_curr]!=TOKEN_END:
            if tokens[_curr-1] in '+-*/^=' and (tokens[_curr] in '=:' or tokens[_curr+1] in '=:' or tokens[_curr]==TOKEN_END):
                error(_curr-1, text="Строка не может оканчиваться на знак действия!")
        else:
            if tokens[_curr-1] in '+-*/^=':
                error(_curr-1, text="Строка не может оканчиваться на знак действия!")
        if tokens[_curr] not in variables:
            err_msg = "Ошибка. Переменная \'" + tokens[_curr] + "\' не определена"
            error(_curr, text=err_msg)
        b3 = int(variables[tokens[_curr]])
        return _curr+1, b3
    elif get_type(tokens[_curr], False, True)=='real':
        err_msg = "Ошибка. После \'" + tokens[_curr-1] + "\' не может идти вещественное число \'" + tokens[_curr] + "\'. "
        error(_curr, text=err_msg)
    elif tokens[_curr] == TOKEN_LPAREN:
        if tokens[_curr-1]==TOKEN_RPAREN:
            error(_curr-1, text="Нет знака между скобками!")
        _curr+=1
        _curr, rp = right_part(tokens, _curr)
        if tokens[_curr] != TOKEN_RPAREN:
            err_msg = "Ошибка. Отсутствует закрывающая круглая скобка \')\'"
            error(_curr, text=err_msg)
        return _curr+1, rp
    elif get_type(tokens[_curr], False, True)=='dec':
        if (get_type(tokens[_curr-1], False, True) or tokens[_curr-1] in ')') and tokens[_curr-1]!=TOKEN_EQ:
            error(_curr-1, text="Нет знака между членами выражения!")
        b3 = int(tokens[_curr])
        return _curr+1, b3
    else:
        err_msg = "Ошибка."
        if tokens[_curr] in ['-', '+', '/', '*', '^']:
            err_msg += " Два знака действия подряд."
        if tokens[_curr] == ')':
            err_msg += "Не найдено открывающей скобки!"
        else:
            err_msg += " После \'" + str(tokens[_curr-1]) + "\' не может идти \'" + tokens[_curr] + "\'. "
        error(_curr, text=err_msg)

def block_2(tokens, _curr):
    _curr, b3 = block_3(tokens, _curr)
    b2 = b3
    while True:
        if _curr < len(tokens)-1 or tokens[-1]=='End':
            pass
        else:    
            error(len(tokens)-1, text="Программа не может кончаться на " + tokens[-1])
        if tokens[_curr] != TOKEN_DEGREE:
            return _curr, b2
        _curr, b3 = block_3(tokens, _curr+1)
        b2 = b2 ** b3

def block_1(tokens, _curr):
    _curr, b2 = block_2(tokens, _curr)
    b1 = b2
    while True:
        if tokens[_curr] not in [TOKEN_MUL, TOKEN_DIV]:
            return _curr, b1
        sign = tokens[_curr]
        _curr, b2 = block_2(tokens, _curr+1)
        if sign == TOKEN_MUL:
            b1 *= b2
        elif sign == TOKEN_DIV:
            if b2 != 0.0:
                b1 /= b2
            else:
                current_token = str(b2)
                err_msg = "Ошибка. Деление на \'0\'"
                error(_curr-1, text=err_msg)

def right_part(tokens, _curr):
    is_minus = False
    if tokens[_curr] == TOKEN_MINUS:
        _curr += 1
        is_minus = True
    rp = 0
    if tokens[_curr] in '+-*/^=' and tokens[_curr - 1] in [TOKEN_LPAREN, TOKEN_RPAREN] and tokens[_curr + 1] in [TOKEN_LPAREN, TOKEN_RPAREN]:
        error(_curr, text="Между скобок не может стоять знак")
    prev_token = None
    while True:
        _curr, b1 = block_1(tokens, _curr)
        if is_minus:
            b1 = -b1
            is_minus = False

        if prev_token == TOKEN_PLUS:
            rp += b1
        elif prev_token == TOKEN_MINUS:
            rp -= b1
        else:
            rp += b1

        if tokens[_curr] == None:
           return
        if tokens[_curr] != TOKEN_PLUS and tokens[_curr] != TOKEN_MINUS:
            return _curr, rp
        prev_token = tokens[_curr]

        _curr += 1

def run():
    global variables
    variables = {}
    window.clear_con()
    window.update_code()
    tokens = imp_lex(window.get_code())
    print(tokens)
    _curr = 0
    if tokens[_curr] != TOKEN_BEGIN:
            error(_curr, text="Программа не может начинаться с " + tokens[_curr])
    else:
        _curr += 1
    if tokens[_curr] == TOKEN_REAL or tokens[_curr] == TOKEN_INTEGER:
        while tokens[_curr + 1] != TOKEN_EQ and tokens[_curr + 1] != ':' and tokens[_curr]:
            if tokens[_curr] == TOKEN_REAL:
                _curr += 1
                while tokens[_curr + 1] != TOKEN_EQ and tokens[_curr + 1] != ':' and tokens[_curr] != TOKEN_REAL and tokens[_curr] != TOKEN_INTEGER:
                    if not re.match(EX_VAR, tokens[_curr]):
                        error(_curr, text="В Real не может быть " + get_type(tokens[_curr]) + ". Допустимы лишь переменные.")
                    else:
                        _curr += 1
            if tokens[_curr] == TOKEN_INTEGER:
                _curr += 1
                while tokens[_curr + 1] != TOKEN_EQ and tokens[_curr + 1] != ':' and tokens[_curr] != TOKEN_REAL and tokens[_curr] != TOKEN_INTEGER:
                    if not re.match(EX_INT, tokens[_curr]):
                        error(_curr, text="В Integer не может быть " + get_type(tokens[_curr]) + ". Допустимы лишь целые числа.")
                    else:
                        _curr += 1
            if tokens[_curr + 1] == TOKEN_EQ:
                break
    else:
        error(_curr, text="В начале определения должен быть Real или Integer, а не " + get_type(tokens[_curr]))
    terms=[]
    while tokens[_curr]!= TOKEN_END:
        if re.match(r'^[0-9]+', tokens[_curr]) or tokens[_curr+1]==':':
            if re.match(r'^[0-9]+', tokens[_curr]):
                _curr += 1
                if tokens[_curr]==':':
                    _curr += 1
                else:
                    error(_curr, text="После метки должен идти знак \":\".")
            else:
                error(_curr, text="Метка может быть только целочисленной.")
        
        if get_type(tokens[_curr], False, True)=='var':
            name = tokens[_curr]
            _curr+=1
            if tokens[_curr] == TOKEN_EQ:
                _curr+=1
                while tokens[_curr] != TOKEN_END and tokens[_curr + 1] != TOKEN_EQ and tokens[_curr + 1] != ':':
                    _curr, rp = right_part(tokens, _curr)
                    print(name, " = ", rp)
                    variables[name] = rp
                    if _curr == len(tokens)-1 and tokens[_curr] != TOKEN_END:
                        error(_curr, text="Программа не может кончаться на " + tokens[_curr])
    if TOKEN_END in tokens and tokens[-1] != TOKEN_END:
        error(len(tokens)-1, text="После End может идти только конец файла.")
    res = ""
    for key in variables:
        res+=key+" = "+str(variables[key])+"\n"
    window.set_con(res)

if __name__ == '__main__':
    window = BNFWindow(func = run)
    with open('code.ebnf', 'r') as f:
            text = f.read()
    window.set_code(text)
    window.mainloop()