from fastapi import FastAPI, Depends

from preds import *
from funcs import *

import pandas as pd
import time
import classes


# Init the API
api = FastAPI(
	title='Projet 2',
	description="Datascientest Project 2 API",
	version='1.0.0')



@api.get('/')
def status():
	"""
	Returns the status
	"""
	return 1


@api.post('/predictions', name='PREDICTIONS')
def predictions(
	hour: classes.Hour,
	weekday: classes.Weekday,
	month: classes.Month,
	weather: classes.Weather,
	username: str = Depends(get_current_user)
	):

	"""
	Route for predictions
	"""
	# Check if hour is correct
	if 0 <= hour <= 24:
		# Get weekday integer from string (0 indexed)
		weekday_int = time.strptime(weekday.value, "%A").tm_wday + 1

		# Get month integer from string
		month_int = time.strptime(month.value, "%B").tm_mon

		# If weekday > 5, it's a weekend
		is_weekend = 0 if (int(weekday_int) >= 1) and (int(weekday_int) <= 5) else 1

		# Get weather index
		weather_index = get_weather(weather.value)

		# Build dataframe for prediction
		datas = pd.DataFrame(
			data = [[hour, month_int,
				weekday_int, is_weekend,
				weather_index]],
			columns = ['hr', 'month', 'weekday', 'is_weekend', 'weathersit']
			)

		# Call the prediction
		results = predict_results(datas)

		return {
			'user': username,
			'bikes': results['Prediction'][0]
		}

	else:
		raise HTTPException(
			status_code=422,
			detail="Must be between 0 and 24.")


@api.post('/scores/{Model}', name='SCORES')
def scores(
	model: classes.Model,
	username: str = Depends(get_current_user)
	):
	"""
	Route for model scores
	"""

	if model.value == 'Lasso':
		perfs = model_performances(all_models[0])
	elif model.value == 'SVR':
		perfs = model_performances(all_models[1])
	elif model.value == 'LinearRegression':
		perfs = model_performances(all_models[2])
	elif model.value == 'DecisionTreeRegressor':
		perfs = model_performances(all_models[3])

	return { 
		"user": username,
		"model": perfs 
	}


