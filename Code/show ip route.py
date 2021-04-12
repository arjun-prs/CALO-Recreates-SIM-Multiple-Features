import re
import json
user_input=input("Which routes do you want to display: (eigrp/ospf/bgp/mpls) ")
filename='Input\\show ip route '+user_input+'.txt'
f=open(filename, 'r')
content=f.readlines()
i=10
dictionary=[]
temp={}
while(i<len(content)):
    line=content[i].split()
    if(line[0] == "O" or line[0] == "D") :
        temp={}
        temp["dest"]=line[1]
        temp["exit"]=line[-1]
        dictionary.append(temp)
    elif(line[0] == "B"):
        temp={}
        temp["dest"]=line[1]
        temp["exit"]=line[-2]
        dictionary.append(temp)
    elif(line[0] == "*>"):
        temp={}
        temp["dest"]=line[1]
        temp["exit"]=line[2]
        dictionary.append(temp)
    i+=1
filename='Output\\show ip route '+user_input+'.json'
with open(filename, 'w+') as fout:
    json.dump(dictionary, fout)
print(dictionary)
f.close()
fout.close()