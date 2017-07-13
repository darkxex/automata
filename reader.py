import sys
import os.path
import copy

class main:
    numerodeestados=0
    cantidadalfabeto=0
    alfabeto=["E","a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    estadosfinales=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    transiciones=["e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e","e"]
    matriz=[0]
    k=0
    j=0
    n=0
    l=0
    x=0
    i=0
    print "------------------------------------"
    print " El estado inicial sera considerado como el primer estado en la lista"
    print "------------------------------------"
    numerodeestados= input("ingrese la cantidad es estados: ")
    
    print "------------------------------------"
    print "indique con un 1 si es final y con un 0 si no lo es"
    for l in range(numerodeestados):
        
        estadosfinales[l]=input("El estado 'Q"+ str(l) + "' es final: ")

    print "------------------------------------"
    cantidadalfabeto= input("ingrese la cantidad de alfabeto : ")
    for x in range(cantidadalfabeto):
        alfabeto[x+1]=raw_input(" Ingrese el alfabeto "+str(x+1)+" : ")
    #############################  pregutnas sobre cada transicion##############################
    print "------------------------------------"
    print "ingrese las trancisiones 1 a 1, responda con Q0,Q1,Q2... si deja vacio no hay transiciones  "
    for k in range(numerodeestados):
        for j in range(cantidadalfabeto+1):
            transiciones[i]= raw_input(" De Q"+str(k)+ " leyendo '"+alfabeto[j]+"' llega a :")
            i=i+1
            
    print ""
    print "   Estado |  Final(1=si, 0=no) |  alfabeto | trancisiones "
    k=0
    j=0
    i=0
    ###########################  mostrar la tabla por consola #####################################
    for k in range(numerodeestados):
        for j in range(cantidadalfabeto+1):
            print "      Q"+ str(k) + "          " + str(estadosfinales[k])+"               con  "+ alfabeto[j] +"      -->  "+transiciones[i]
            i=i+1
    inueva=i
    i=0
    knueva=100
    #a anexa texto, w sobreescribe texto
    file = open("data.txt","w")
    for k in range(numerodeestados):
        
        for j in range(cantidadalfabeto+1):
            validador="N"
            if(estadosfinales[k]==1):
                validador="S"
            if (knueva==k and transiciones[i]!="" ):
                file.write (" "+alfabeto[j]+":"+transiciones[i])
                knueva=k
            if (knueva!=k):
                file.write("Q"+str(k)+" "+validador)
                if (transiciones[i]!=""):
                    file.write(" "+alfabeto[j]+":"+transiciones[i])
                knueva=k
            i=i+1
        file.write ("\n")
           

