import sys
import os
from pythonds.basic.stack import Stack
from Transition import Transition
from Thompson import Thompson
from re import search	
#Clase para expresiones regulares
class RegularExpresion(object):
	
	def __init__(self, regexp):
		self.infix = ponPuntos(regexp)
		self.postfix = infixToPostfix(regexp)

	def re_to_Thompson(self):
		#Stack 
		stack = []
		postfix = infixToPostfix(self.infix)
		#Por cada elemento encontrado en la expresion regular hara lo siguiente
		for i in postfix:
			if i == '*':
				 #saca el ultimo dato de la lista y lo asigna a automat
				automat = stack.pop()
				#aplica cerradura de kleene e inserta al final de la lista
				stack.append(automat.kleene()) 
			elif i == '+':
       			#saca el ultimo dato de la lista
				automat = stack.pop()
    			#aplica cerradura positiva e inserta al final de la lista
				stack.append(automat.positive())
			elif i == '|':
				#saca ultimo dato de la lista
				right = stack.pop() 
				#saca penultimo dato de la lista
				left = stack.pop()
				#aplica union a right y left (left|right) e inserta al final de la lista ya que asi se establece la funcion de OR, siendo la concatenacion de dos expresiones regulares
				stack.append(left.union(right))
			elif i == '.':
				#saca ultimo dato de la lista
				right = stack.pop()
				#saca penultimo dato de la lista
				left = stack.pop() 
				#aplica concatenacion a right y left (left.right) e inserta al final de la lista
				stack.append(left.concatenate(right))
			else:
				initialTransitions = [] 
				#inserta transicion, sólo de 1 a 2
				initialTransitions.append(Transition(1,2,i)) 
				#crea automata básico 
				new_Thompson = Thompson(1,2,initialTransitions) 
				stack.append(new_Thompson) 
		return stack.pop() #regresa el ultimo valor de la lista, que es el automata final 
		


def infixToPostfix(infixexpr): 
    #precedencia de los operadores donde 
    prec = {}
    prec["*"] = 4
    prec["+"] = 4
    prec["."] = 3
    prec["|"] = 2
    prec["("] = 1
   
    opStack = Stack()
    postfixList = []
	#Definimos los tokens que se van a encontrar en la expresion regular obviamente separando los tokens de los operadores. 
    for token in infixexpr:
        
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvxwyz" or token in "0123456789" or token in "ε:;'" or token in '"':
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return "".join(postfixList)

def ponPuntos(re):
	op = ["(","|",".",")"]
	aux = ""
	i = 0
	n = 0
	while (i + 1) < len(re):
		
		if re[i] in op:
			if re[i] == ")" and re[i+1] == "+" or re[i+1] == "*":
				aux += re[i]
				aux += re[i+1]
			elif re[i] == ")" and re[i+1] not in op and re[i+1] != "+" and re[i+1] != "*":
				aux += re[i]
				aux+= "."
			else:
				aux += re[i]

		elif re[i] == "+" or re[i] == "*":
			if(re[i+1] not in op) or re[i+1] == "(":
				aux+= "."
			
			
		elif re[i] not in op and re[i + 1] not in op and re[i + 1] != "*" and re[i + 1] != "+":
			aux += re[i]
			aux += "."
					
		elif re[i] not in op and re[i + 1] == "*" or re[i + 1] == "+":
			aux += re[i]
			aux += re[i+1]
				
		elif (re[i] not in op and re[i+1] in op):
			aux += re[i]
	
		i+=1
		n = i
		if re[i] not in op and re[i] != "*" and re[i] != "+" and n + 1 == len(re):
			aux += re[i]
	return aux

def agregar_parentesis(expr):
    stack = []
    for char in expr:
        if char == '(':
            stack.append(char)
        elif char == ')':
            if len(stack) > 0 and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(char)
    while len(stack) > 0:
        if stack[-1] == '(':
            expr += ')'
        else:
            expr = '(' + expr
        stack.pop()
    return expr

   
if __name__ == '__main__':
	
	regexp = input("Ingrese la expresion regular: ")
	print(regexp)
	if "ε" in regexp:
		regexp = regexp.replace('ε','e')
		re = RegularExpresion(regexp)
		thompson = re.re_to_Thompson()
		thompson.printTransitions()
		os.system("dot -Tgif Thompson.gv > Thompson.gif")
	if "?" in regexp:
		print('La expresion regular contiene un simbolo de interrogacion, por lo que se reemplazo por |e')
		regexp = regexp.replace('?','|e)')
		regexp = agregar_parentesis(regexp)

		if "+" in regexp:
			print('La expresion regular contiene un simbolo de mas, por lo que se reemplazo por concatenacion')
			regexp= agregar_parentesis(regexp)
			print(regexp)
			re = RegularExpresion(regexp)
			thompson = re.re_to_Thompson()
			thompson.printTransitions()
   
   
		print(regexp)
		re = RegularExpresion(regexp)
		thompson = re.re_to_Thompson()
		thompson.printTransitions()

		
		
		os.system("dot -Tgif Thompson.gv > Thompson.gif")
	if "+" in regexp:
		print('La expresion regular contiene un simbolo de mas, por lo que se reemplazo por concatenacion')
		
		print(regexp)
		regexp = agregar_parentesis(regexp)
		re = RegularExpresion(regexp)
		thompson = re.re_to_Thompson()
		thompson.printTransitions()

		
		os.system("dot -Tgif Thompson.gv > Thompson.gif")
	else:
		regexp = ponPuntos(regexp)
		regexp = agregar_parentesis(regexp)
		print(regexp)	
		re = RegularExpresion(regexp)
	
		thompson = re.re_to_Thompson()
		thompson.printTransitions()

		
		os.system("dot -Tgif Thompson.gv > Thompson.gif")

   	
		
		