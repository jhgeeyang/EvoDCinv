## Remove Blank lines
# read text file
with open('merged.txt', 'r') as myfile:
# this will read the whole file / cf.) readlines()
    data=myfile.read()
# delete the blank line
text = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
print(text)
file2 = open("merg.txt",'w')
file2.write(text)
file2.close()
    
