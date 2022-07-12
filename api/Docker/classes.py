from enum import Enum


class Model(str, Enum):
	lasso = 	'Lasso'
	svr =		'SVR'
	linear = 	'LinearRegression'
	dt = 		'DecisionTreeRegressor'


class Hour(int):
	hour = 0


class Weekday(str, Enum):
	d1 = 'Monday'
	d2 = 'Tuesday'
	d3 = 'Wednesday'
	d4 = 'Thursday'
	d5 = 'Friday'
	d6 = 'Saturday'
	d7 = 'Sunday'


class Month(str, Enum):
	m1 = 	'January'
	m2 = 	'February'
	m3 = 	'March'
	m4 = 	'April'
	m5 = 	'May'
	m6 = 	'June'
	m7 = 	'July'
	m8 = 	'August'
	m9 = 	'September'
	m10 = 	'October'
	m11 = 	'November'
	m12 = 	'December'



class Weather(str, Enum):
	clear = 	'Clear'
	cloudy = 	'Cloudy'
	rainy = 	'Rainy'
	snowy = 	'Snowy'
