import os,math,json
import sympy as sp
import logging

from .logic import SymPyGamma

g = SymPyGamma()

def solve_sympy_equation(equation):
    if "=" in equation:
        line = equation.split("=")
        line_1 = line[1]

        if line_1[0] != "+" and line_1[0] != "-":
            line_1 = f"+{line_1}"

        line_1 = list(line_1)

        for symbol_id,symbol in enumerate(line_1):
            if symbol == "-":
                line_1[symbol_id] = "+"

            if symbol == "+":
                line_1[symbol_id] = "-"

        line_1 = "".join(line_1)

        equation = line[0]+line_1

    try:        
        r = g.eval(equation)

        equ_plot = False

        for elem in r:
            if "card" in elem.keys():
                if elem['card'] == "roots":
                    equ = elem['input']

                if elem['card'] == "plot":
                    equ_plot = True
                
        if "variable" in r[0].keys():
            equ_res = sp.sympify(f"{equ}")
            equ_type = "equation"
            if type(equ_res) == list and len(equ_res) == 1:
                equ_res = equ_res[0]
        else:
            equ_res = r[0]["output"]
            equ_type = "digital"

        result = {"status_code":0,"message":str(equ_res),"type":equ_type}

        if equ_plot == True:
            equ_inp = r[0]['input']
            
            result['plot'] = equ_inp

        return result

    except Exception as exc:
        return {"status_code":1,"message":"invalid input","type":"None"}

def solve_equation(equation):
    try:
        equ_res = eval(equation)
        equ_type = "digital"
        return {"status_code":0,"message":str(equ_res),"type":equ_type}
    
    except:
        return solve_sympy_equation(equation)

def solve_equation_system(system):
    try:
        solution = g.eval(f"solve({system})")
        message = solution[1]["output"]
        status_code = 0

    except:
        message = "invalid input"
        status_code = 1

    return {"status_code":status_code,"message":message}