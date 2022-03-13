import re
from imp_lex import *


def get_type(token, txt=True, typ=False):
    text = ""
    type =""
    if re.match(r'[0-9]+', token):
        text ="целое число " + token
        type = 'dec'
    elif re.match(r'[0-9]+\.[0-9]+', token):
        text = "вещественное число " + token
        type = 'real'
    elif re.match(r'[A-Za-z][A-Za-z0-9_]*', token):
        text = "переменная " + token
        type ='var'
    elif re.match(r'[а-яА-ЯёЁ]', token):
        text = "переменная с русскими буквами. Можно использовать лишь буквы латинского алфавита!"
        type = 'ru'
    else:
        text=token
        type=''
    if txt and typ:
        return text, type
    elif txt and not typ:
        return text
    elif not txt and typ:
        return type

def highlighter(_curr, text):
    _curr+=1
    skippats = " \t"
    signs = ".,:;\'\"!?&|+-*/^%#()"
    is_word = False
    words = start = end = count = strnum = 0
    for iter, char in enumerate(text):
        if char == '\n':
            if words==_curr:
                    end = count
                    print("Word: ", words)
                    return strnum, start, end
            else:
                strnum+=1
                is_word = False
                count=0
                continue
        if char in skippats:
            if is_word:
                is_word=False
                if words==_curr:
                    end = count
                    print("Word: ", words)
                    return strnum, start, end
                else:
                    count+=1
                    continue
        else:
            if char in signs or iter>=len(text)-1:
                if is_word and words==_curr:
                    end = count
                    print("Word: ", words)
                    return strnum, start, end
                is_word = False
                words+=1
                if words==_curr:
                    end = count
                    print("Word: ", words)
                    return strnum, end, end+1
                
                count+=1
                continue
            if not is_word:
                words+=1
                is_word = True
                start = count
        count+=1
    print("Word: ", words)  
    return 0, 0, 0
