# read text file
with open('data.txt', 'r') as myfile:
# this will read the whole file / cf.) readlines()
    data=myfile.read()
# delete the blank line
text = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
print(text)
file2 = open("newfile.txt",'w')
file2.write(text)
file2.close()
    
