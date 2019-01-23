import glob
list = (glob.glob("./DAS_pick_3km/*.txt"))
for text in list:
    print(text[15:-4])
