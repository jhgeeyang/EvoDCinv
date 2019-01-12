import pickle

# loaded data is a "layered-model" object
a = pickle.load(open('test.pickle','rb'))
a = pickle.load(open('test.pickle','rb'))
print(a.model)
