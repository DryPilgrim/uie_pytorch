import re
f=open('dry/demo.txt')
a=list(f)
b=[]
i=0
for item in a:
    b.append(list(item.split(' ')))
    try:
        if int(b[i][2]):
            pass
    except:
        del b[i][2]
    print(b[i])
    i+=1
# print(b[-3])
with open('dry/demo2.txt','a') as f:
    for i in range(len(b)):
        for j in range(len(b[i])):
            f.write(str(b[i][j]))
            f.write(' ')
with open('dry/demo2.txt') as f:
    cont=f.read()
    cont=re.sub(r'\n\s', '\n', cont)
with open('dry/demo2.txt','w') as f:
    f.write(cont)