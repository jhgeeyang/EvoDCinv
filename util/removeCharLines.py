import itertools

## Remove Blank lines
# read text file
#filename ='data_60_4km_D_002.txt'
#filename='procD_n604km_002.txt' 
#filename ='D_merg2.txt'
#filename ='5lay_3.0_.txt'
#filename ='invResult_0315_DAS.txt'
filename ='invResult_0318_DAS.txt'
#filename = 'merge_3km_3lay_4.txt'
with open(filename, 'r') as myfile:
# this will read the whole file / cf.) readlines()
    data=myfile.read()
# delete the blank line
text = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
print(text)
file2 = open(filename,'w')
file2.write(text)
file2.close()

with open(filename, 'r') as myfile:
# this will read the whole file / cf.) readlines()
    data=myfile.read()
# delete the blank line
text = "\n".join([ll.rstrip() for ll in data.splitlines() if ll.strip()])
print(text)
file2 = open("synth_char.txt",'w')
file2.write(text)
file2.close()

## Remove lines with unwanted Letters

# read text file
with open('synth_char.txt', 'r') as myfile:
# this will read the whole file / cf.) readlines()
    data=myfile.readlines()
bag_of_words = ["curves","Inverting","Elapsed","Inverting","model","n_iter:","n_eval:"]
# only worked for first letter..
# BAD CODE
'''
for count, line in enumerate(data):
    print(line)
    for word in bag_of_words:
        if word in line:
            data.remove(line)
            for _ in itertools.islice(data,0):
                pass
            continue
'''
## USE list comprehension :)
for word in bag_of_words:
    data = [line for line in data if not word in line]
# Write the lines.
with open('edit'+filename,'w') as f:
    for line in data:
        f.write("%s" %line)
    
