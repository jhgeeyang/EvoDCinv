import pickle

# loaded data is a "layered-model" object
a = pickle.load(open('test.pickle','rb'))
b = pickle.load(open('run1.pickle','rb'))
print(a.model)
print(b.model)

