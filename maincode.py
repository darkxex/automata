import sys
import os
import copy


while(1):
    
    print ("Leyendo Quintupla.")
    os.system("reader.py")
    print ("transformando a AFND a AFD.")
    os.system("execute.py afd data.txt final.txt")
    print ("Desea minimizar? Presione S para afirmar.")
    x = raw_input()
    if (x == "S" or x == "s" or x == "Si"):
        print ("Generando Automata reducido.")
        os.system("execute.py minimizar final.txt final.txt")
    else:
        print ("Ha escogido no reducir el automata.")

    f = open('final.txt')
    print "Estado Es final? Transicion"
    for line in f:                
        
            print line.replace(":", "->").replace("S","Si").replace("N","No")   
    f.close()
    print "Ingrese los caracteres a validar... (Ej 110, para epsilon no ingrese nada.)"
    
    y = raw_input()
    os.system("execute.py validar final.txt " + y)
    
    print "--------------------------------------------------"

