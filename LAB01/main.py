import sys
import os
from pythonds.basic.stack import Stack
from Transition import Transition
from Thompson import Thompson

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
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" or token in "abcdefghijklmnopqrstuvwyz" or token in "0123456789" or token in "?<>":
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


if __name__ == '__main__':
	print("digraph AFN{")
	print("rankdir=LR; \n node[shape = circle];")
	regexp = "(a*|b*)c"
	re = RegularExpresion(regexp)
	
	thompson = re.re_to_Thompson()
	thompson.printTransitions()

	
	print("}")
	os.system("dot -Tpng Thompson.gv > Thompson.png")
	