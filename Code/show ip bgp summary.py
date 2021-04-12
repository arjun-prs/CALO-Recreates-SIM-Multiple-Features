f=open('Input\\show ip bgp summary.txt', 'r')
content=f.readlines()
i=13
neighbor_list=[]
while(i<len(content)):
    word=content[i].split()
    neighbor_list.append(word[0])
    i+=1
with open('Output\\bgp neighbors.txt', 'w+') as fout:
    for j in neighbor_list:
        fout.write(j)
        fout.write("\n")
print(neighbor_list)
