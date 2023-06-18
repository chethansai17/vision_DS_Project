import numpy as np
from numpy import *
import math
NL=int(input("Enter the number of links"))
print("θ=angle to z-axis along x-axis")
print("A=distance to z-axis along x-axis")
print("α=angle to x-axis along z-axis")
print("D=distance to x-axis along z-axis")
dals=[]
for i in range(1,NL+1):
    n=4
    print("link:",i)
    print("Format(θ A α D)")
    a1=list(map(int,input("Enter the values: ").strip().split()))[:4]
    dals.append(a1)
matrix2=[]
x0=0
y0=0
for j in range(0,NL):
    b1=dals[j]
    for z in b1:
        B=b1[0]
        A=b1[1]
        C=b1[2]
        D=b1[3]
        data1=[round(math.cos(math.radians(B)), ndigits=4), round(-(math.sin(math.radians(B))) * math.cos(math.radians(C)), ndigits=4), round(math.sin(math.radians(B))*math.sin(math.radians(C)), ndigits=4), round(A*math.cos(math.radians(B)), ndigits=4)]
        data2=[round(math.sin(math.radians(B)), ndigits=4), round(math.cos(math.radians(B)) * math.cos(math.radians(C)), ndigits=4), round(-(math.cos(math.radians(B))*math.sin(math.radians(C))), ndigits=4), round(A*math.sin(math.radians(B)), ndigits=4)]
        data3=[0, round(math.sin(math.radians(C)), ndigits=4), round(math.cos(math.radians(C)), ndigits=4), D]
        data4=[0,0,0,1]
    matrix2.append(data1)
    matrix2.append(data2)
    matrix2.append(data3)
    matrix2.append(data4)
print()
result=1
for k in range(0,len(matrix2),4):
    matrix3=np.array([matrix2[k],matrix2[k+1],matrix2[k+2],matrix2[k+3]])
    print(matrix3,"\n")
    matrix4=matrix(matrix3)
    result*=matrix4
print("The location of the end effector by us DH reperesnetation is:\n")
print(result)
