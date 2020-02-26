# Dominick Licciardi Parser_Project_LA
# worked with Xiasong/Simon on the assignment.
# CS3210 - Principles of Programming Languages - Spring 2020
# A Lexical Analyzer for the Parser Project

from enum import Enum
import sys


# all char classes
class CharClass(Enum):
    EOF = 1
    LETTER = 2
    DIGIT = 3
    OPERATOR = 4
    PUNCTUATOR = 5
    QUOTE = 6
    BLANK = 7
    OTHER = 8
    DOLLAR = 9


# reads the next char from input and returns its class
def getChar(input):
    if len(input) == 0:
        return None, CharClass.EOF
    c = input[0].lower()
    if c.isalpha():
        return c, CharClass.LETTER
    if c.isdigit():
        return c, CharClass.DIGIT
    if c == '"':
        return c, CharClass.QUOTE
    if c in ['+', '-', '*', '/', '>', '=', '<']:
        return c, CharClass.OPERATOR
    if c in ['.', ':', ',', ';']:
        return c, CharClass.PUNCTUATOR
    if c in [' ', '\n', '\t']:
        return c, CharClass.BLANK
    if c == '$':
        return c, CharClass.DOLLAR
    return c, CharClass.OTHER


# calls getChar and getChar until it returns a non-blank
def getNonBlank(input):
    ignore = ""
    while True:
        c, charClass = getChar(input)
        if charClass == CharClass.BLANK:
            input, ignore = addChar(input, ignore)
        else:
            return input


# adds the next char from input to lexeme, advancing the input by one char
def addChar(input, lexeme):
    if len(input) > 0:
        lexeme += input[0]
        input = input[1:]
    return input, lexeme


# all tokens
class Token(Enum):
    EOF = 0
    INT_TYPE = 1
    MAIN = 2
    OPEN_PAR = 3
    CLOSE_PAR = 4
    OPEN_CURLY = 5
    CLOSE_CURLY = 6
    OPEN_BRACKET = 7
    CLOSE_BRACKET = 8
    COMMA = 9
    ASSIGNMENT = 10
    SEMICOLON = 11
    IF = 12
    ELSE = 13
    WHILE = 14
    OR = 15
    AND = 16
    EQUALITY = 17
    INEQUALITY = 18
    LESS = 19
    LESS_EQUAL = 20
    GREATER = 21
    GREATER_EQUAL = 22
    ADD = 23
    SUBTRACT = 24
    MULTIPLY = 25
    DIVIDE = 26
    BOOL_TYPE = 27
    FLOAT_TYPE = 28
    CHAR_TYPE = 29
    IDENTIFIER = 30
    INT_LITERAL = 31
    TRUE = 32
    FALSE = 33
    FLOAT_LITERAL = 34
    CHAR_LITERAL = 35



# lexeme to token conversion, eliminated the dollar sign token
# because there is no need for it at this point.
lookup = {
    "eof": Token.EOF,
    "$": Token.INT_TYPE,
    # " "      : Token.MAIN,
    "main": Token.MAIN,
    "complex": Token.CLOSE_PAR,
    "fixed": Token.OPEN_CURLY,
    "floating": Token.CLOSE_CURLY,
    "single": Token.SINGLE,
    "double": Token.DOUBLE,
    "binary": Token.BINARY,
    "decimal": Token.DECIMAL
}


# returns the next (lexeme, token) pair or None if EOF is reached
def lex(input):
    input = getNonBlank(input)

    c, charClass = getChar(input)
    lexeme = ""

    # check EOF first
    if charClass == CharClass.EOF:
        return input, None, None

    # TODOd: read a letter followed by letters or digits
    # If lexeme not in the lookup, throw exception.
    if charClass == CharClass.LETTER:
        input, lexeme = addChar(input, lexeme)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.LETTER or charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                if lexeme not in lookup:
                    raise Exception("Lexical Analyzer Error: unrecognized lexeme found!")
                else:
                    return input, lexeme, lookup[lexeme]

    # TODOd: read digits
    if charClass == CharClass.DIGIT:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        while True:
            c, charClass = getChar(input)
            if charClass == CharClass.DIGIT:
                input, lexeme = addChar(input, lexeme)
            else:
                return input, lexeme, Token.LITERAL

    # TODOd: read an operator
    if charClass == CharClass.DOLLAR:
        input, lexeme = addChar(input, lexeme)
        c, charClass = getChar(input)
        if charClass == CharClass.LETTER:
            input, lexeme = addChar(input, lexeme)
            while True:
                c, charClass = getChar(input)
                if charClass == CharClass.LETTER or charClass == CharClass.DIGIT:
                    input, lexeme = addChar(input, lexeme)
                else:
                    return input, lexeme, Token.IDENTIFIER
    raise Exception("Lexical Analyzer Error: unrecognized symbol found!")


# main
if __name__ == "__main__":

    # checks if source file was passed and if it exists
    if len(sys.argv) != 2:
        raise ValueError("Missing source file")
    source = open(sys.argv[1], "rt")
    if not source:
        raise IOError("Couldn't open source file")
    input = source.read()
    source.close()
    output = []

    # main loop
    while True:
        input, lexeme, token = lex(input)
        if lexeme is None:
            break
        output.append((lexeme, token))

    # prints the output
    for (lexeme, token) in output:
        print(lexeme, token)


# input(source5.exp): declare $altitude double binary floating
# output:
# declare Token.DECLARE
# $altitude Token.IDENTIFIER
# double Token.DOUBLE
# binary Token.BINARY
# floating Token.FLOATING
