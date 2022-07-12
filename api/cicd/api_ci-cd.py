import requests
import os
import json
import datetime
from requests.auth import HTTPBasicAuth

# Set up params for requests
address = '172.17.0.1'
port = 8000

params_cloudy_summer = { 'hour': 15, 'weekday': 'Friday', 'month': 'June', 'weather': 'Cloudy' }
params_rainy_autumn = { 'hour': 8, 'weekday': 'Monday', 'month': 'October', 'weather': 'Rainy' }

alice_auth = HTTPBasicAuth('alice', 'wonderland')
bob_auth = HTTPBasicAuth('bob', 'builder')
bad_auth = HTTPBasicAuth('wrong', 'one')

models = [{'model': 'Lasso'}, {'model': 'LinearRegression'}, {'model': 'DecisionTreeRegressor'}]

# End set up params

# Requests
alice = requests.post(
	url='http://{address}:{port}/predictions'.format(address=address, port=port),
	params=params_cloudy_summer, timeout=5, auth=alice_auth
)

bob = requests.post(
	url='http://{address}:{port}/predictions'.format(address=address, port=port),
	params=params_rainy_autumn, timeout=5, auth=bob_auth
)

bad = requests.post(
	url='http://{address}:{port}/predictions'.format(address=address, port=port),
	params=params_rainy_autumn, timeout=5, auth=bad_auth
)

lasso = requests.post(
	url='http://{address}:{port}/scores/{{Model}}/'.format(address=address, port=port),
	params=models[0], timeout=5, auth=alice_auth
)

dt = requests.post(
	url='http://{address}:{port}/scores/{{Model}}/'.format(address=address, port=port),
	params=models[2], timeout=5, auth=alice_auth
)
# End requests

# Retrieve jsons
alice_results = json.loads(alice.text)
bob_results = json.loads(bob.text)
bad_results = json.loads(bad.text)
lasso_results = json.loads(lasso.text)
dt_results = json.loads(dt.text)

# Output for tests
output = """
=============================================
LOGS FOR CI/CD TESTS
- DATE: {today}

=======================
=== TESTS FOR PREDS ===
=======================

Request done for Alice:
-- Params: 15, Friday, June, Cloudy
| Expected Code = 200 
	>> Result = {alice_code}
| Expected Bikes = 214.0
	>> Result = {alice_bikes}

Request done for Bob:
-- Params: 8, Monday, October, Rainy
| Expected Code = 200 
	>> Result = {bob_code}

| Expected Bikes = 173.0 
	>> Result = {bob_bikes}

=======================
==== TESTS  MODELS ====
=======================

| Request done for models scores on Tests Datasets
-- Params:	 Lasso()
| Expected Code = 200 
	>> Result = {lasso_code}

| 0 < Expected Score < 0.3 
	>> Result = {lasso_score}

-- Params:	 DecisionTreeRegressor()
| Expected Code = 200 
	>> Result = {dt_code}

| 0.79 < Expected Score < 1
	>> Result = {dt_score}

=======================
=== TESTS FOR AUTHS ===
=======================

| Request done for bad user:
-- 
| Expected Code = 401 
	>> Result =  {bad_user}

=============================================
"""

date = datetime.datetime.today()

# Display requests results
alice_code = 'SUCCESS' if alice.status_code == 200 else 'FAILURE'
alice_bikes = 'SUCCESS' if alice_results['bikes'] == 214 else 'FAILURE'

bob_code = 'SUCCESS' if bob.status_code == 200 else 'FAILURE'
bob_bikes = 'SUCCESS' if bob_results['bikes'] == 173 else 'FAILURE'

bad_code = 'SUCCESS' if bad.status_code == 401 else 'FAILURE' 

lasso_code = 'SUCCESS' if lasso.status_code == 200 else 'FAILURE' 
lasso_score = 'SUCCESS' if (lasso_results['model'] > 0 and lasso_results['model'] < 0.3) else 'FAILURE'

dt_code = 'SUCCESS' if dt.status_code == 200 else 'FAILURE' 
dt_score = 'SUCCESS' if (dt_results['model'] > 0.79 and dt_results['model'] < 1) else 'FAILURE'

# Print the output
print(	output.format(
		today=date,
		alice_code=alice_code, alice_bikes=alice_bikes,
		bob_code=bob_code, bob_bikes=bob_bikes,
		lasso_code=lasso_code, lasso_score=lasso_score,
		dt_code=dt_code, dt_score=dt_score,
		bad_user=bad_code
	))

# Print output in a file if env variable LOG = 1
if os.environ.get('LOG') == "1":
	with open('/home/api/logs/api.log', 'a') as filestream:
		filestream.write(output.format(
				today=date,
				alice_code=alice_code, alice_bikes=alice_bikes,
				bob_code=bob_code, bob_bikes=bob_bikes,
				lasso_code=lasso_code, lasso_score=lasso_score,
				dt_code=dt_code, dt_score=dt_score,
				bad_user=bad_code
			))