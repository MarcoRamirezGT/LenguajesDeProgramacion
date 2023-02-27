import sys
import os
from pythonds.basic.stack import Stack
from Transition import Transition


class Thompson(object):
    #Clase para automatas finitos no deterministas
    #Operadores
	op = ["(","*","+","|","."]

	def __init__(self, initialState,finalState,transitions):
        #estado inicial
		self.initialState = initialState 
        #estado final
		self.finalState = finalState 
        #lista de transiciones
		self.transitions = transitions 
	
    #Regresa el estado final
	def count_transition(self):
		return self.finalState
    #Imprime cada transicion con la sintaxis para grapghviz
	def printTransitions(self):
		f= open("Thompson.gv","w+")
		f.write("digraph AFN{\n")
		f.write("rankdir=LR; \n node[shape = circle];\n")
		f.write("nodeI [shape=point];\n")
		for i in range(self.finalState):
			f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\"];\n")
			if (i+1) == self.finalState:
				f.write("node"+str(i+1)+" [name=\""+str(i+1)+"\" shape = \"doublecircle\"];\n")
			i+=1
		f.write("nodeI -> node1 [label = \"I\"];\n")
		for t in self.transitions:
			f.write(str(t) + "\n")
		f.write("}\n")

	
	#Concatenacion de dos automatas
	def concatenate(self,s):
        #Numero de transiciones en el automata
		number_of_transitions = self.count_transition() 
        #inicializa nueva lista de transiciones
		new_transitions = []
		for t in self.transitions:
            #inserta transiciones de r a nueva lista de transiciones
			new_transitions.append(t)
		for t in s.transitions:
            #a cada estado de s le suma la cantidad de estados en r menos el estado final de r que se fusiona con el estado
			t.nodeFrom += number_of_transitions -1
			t.nodeTo += number_of_transitions -1
            #agrega a nueva lista de transiciones
			new_transitions.append(t) 
        
		new_Thompson = Thompson(self.initialState,s.finalState+number_of_transitions- 1,new_transitions) 
		return new_Thompson
    #Union de dos automatas
	def union(self,s):
        #iniciliza nueva lista de transiciones
		new_transitions = [] 
        #contamos cuantos estados tiene el automata r
		number_of_transitions = self.count_transition() 
        #le agregamos dos estados nuevos
		finalState = s.finalState + number_of_transitions + 2  
		for t in self.transitions:
            #A cada transicion se le suma 1 en from y al to del automata r
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t)
		for t in s.transitions:
            #A cada transicion se le suma la cantidad de estados en y mas un inicial nuevo
			t.nodeFrom += number_of_transitions+1
			t.nodeTo += number_of_transitions+1
            #agrega a nuevas transiciones
			new_transitions.append(t) 
        #transicion de estado inicial nuevo a viejo estado inicial de r
		new_transition1 = Transition(1,2,"epsilon") 
		new_transition2 = Transition(1,s.initialState+number_of_transitions+1,"epsilon") 
		#transicion de viejo estado final de r a nuevo estado final 
		new_transition3 = Transition(self.finalState+1,finalState,"epsilon") 
		#transicion de viejo estado final de s a nuevo estado final 
		new_transition4 = Transition(s.finalState+number_of_transitions+1,finalState,"epsilon") 
		#inserta nuevas transiciones
		new_transitions.append(new_transition1)
		new_transitions.append(new_transition2)
		new_transitions.append(new_transition3)
		new_transitions.append(new_transition4)
   		#nuevo automata

		new_Thompson = Thompson(1,finalState,new_transitions)
		return new_Thompson
	#aplica cerradura de kleene a automata
	def kleene(self):
		new_transitions = [] 
		for t in self.transitions:
			# a cada transicion le suma 1 en from y al to
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t) #inserta en la nueva lista de transiciones
		new_transition1 = Transition(1,2,"epsilon") #transicion epsilon desde estado inicial nuevo
		new_transition2 = Transition(1,self.finalState+2,"epsilon") #transicion epsilon de nuevo estado inicial al nuevo estado final
		new_transition3 = Transition(self.finalState+1,self.initialState+1, "epsilon") #transicion epsilon de regreso
		new_transition4 = Transition(self.finalState+1,self.finalState+2,"epsilon") #transicion epsilon al estado final nuevo
		new_transitions.append(new_transition1)
		new_transitions.append(new_transition2)
		new_transitions.append(new_transition3)
		new_transitions.append(new_transition4)
		new_Thompson = Thompson(1,self.finalState+2,new_transitions) #nuevo automata
		return new_Thompson

	def positive(self):
		#aplica cerradura positiva a automata
		new_transitions = [] #inicializa nueva lista de transiciones
		for t in self.transitions:
			t.nodeFrom += 1
			t.nodeTo += 1
			new_transitions.append(t) #inserta en la nueva lista de transiciones
		new_transition1 = Transition(1,2,"epsilon") #transicion epsilon desde estado inicial nuevo
		new_transition3 = Transition(self.finalState+1,self.initialState+1, "epsilon") #transicion epsilon de regreso
		new_transition4 = Transition(self.finalState+1,self.finalState+2,"epsilon") #transicion epsilon al estado final nuevo
		new_transitions.append(new_transition1) #inserta nueva transicion
		new_transitions.append(new_transition3) #inserta nueva transicion
		new_transitions.append(new_transition4) #inserta nueva transicion
		new_Thompson = Thompson(1,self.finalState+2,new_transitions) #nuevo automata
		return new_Thompson