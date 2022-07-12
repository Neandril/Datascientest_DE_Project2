import pandas as pd
from sklearn.model_selection import train_test_split


# Read pickles
df = pd.read_pickle('./pkl/DataForML.pkl')
scaler = pd.read_pickle('./pkl/MinMaxScaler.pkl')
model = pd.read_pickle('./pkl/Final_DT_Model.pkl')
all_models = pd.read_pickle('./pkl/All_Models.pkl')

# Variables and target
variables = ['hr', 'month', 'weekday', 'is_weekend', 'weathersit']
target = 'cnt'


def predict_results(datas):
	"""
	Return the predictions based on user inputs

	datas -- Dataframe
	"""

	# Get the shape of inputs
	nb = datas.shape[0]

	# Concat passed datas with dataframe
	datas = pd.concat([datas, df])

	# Create X based on the variables, and scale it
	X = datas[variables].values[0:nb]
	X = scaler.transform(X)

	# Make predictions
	predictions = model.predict(X)

	# Store predictions into a dataframe
	preds_result = pd.DataFrame(predictions, columns=['Prediction'])

	return(round(preds_result))



def model_performances(model):
	"""
	Return R2 Score of a model on the test set

	model -- Model to compute performances
	"""

	# Split dataframe
	X = df[variables].values
	y = df[target].values
	X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)

	# Return score of the model
	return model.score(X_test, y_test)

