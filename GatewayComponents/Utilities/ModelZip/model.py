import pickle

with open('model.pkl' , 'rb') as f:
	model = pickle.load(f)

def predict(arg1,arg2,arg3,arg4):
	print('getting prediction')
	return  str(model.predict([[arg1,arg2,arg3,arg4]])[0])

# print(predict(1,2,3,4))