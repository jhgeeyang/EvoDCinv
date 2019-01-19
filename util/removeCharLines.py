import itertools
# read text file
with open('newfile.txt', 'r') as myfile:
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
with open('newfile2.txt','w') as f:
    for line in data:
        f.write("%s" %line)
    
