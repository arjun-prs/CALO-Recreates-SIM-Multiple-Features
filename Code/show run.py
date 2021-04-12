import re
user_input=input("Which running configuration do you need: (bgp/eigrp/ospf/mpls/multicast/interface) ")
filename='Input\\show run '+user_input+'.txt'
f=open(filename, 'r')
lines=f.readlines()
search_list=[]
search_list.append(user_input)
if(user_input == "mpls"):
    search_list.append("vrf")
    search_list.append("ospf")
    search_list.append("bgp")
if(user_input == "multicast"):
    search_list.append("interface")
count=0
result=""
for line in lines:
    count=count+1
    for search_word in search_list:
        if re.search(search_word, line):
            for lineno in range(count-1,len(lines)):
                if re.search("!", lines[lineno]):
                    break
                result+=lines[lineno]
print(result)
filename='Output\\show run (filtered) '+user_input+'.txt'
with open(filename, 'w+') as fout:
    for j in result:
        fout.write(j)
f.close()
fout.close()