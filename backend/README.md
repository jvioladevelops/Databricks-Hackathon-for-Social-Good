## Documentation

### Table of contents
1. [Errors](#errors)
2. [Endpoints](#endpoints)
3. [Endpoint description](#endpoint-description)
4. [Tests](#tests)

### Errors
```
400 - Bad Request
404 - Not Found
422 - Unprocessabel Enityt 
```

### Endpoints
```
1. GET '/'
2. POST '/survey'
3. GET '/codes'
```

##### Endpoint description
```
1. GET '/'
DESCRIPTION: 
    Loads and renders HTML/CSS/JS/image files from the frontend.
RETURNS: 
    A rendered world map from world.html.
```
```
2. POST '/survey'
ASSUMPTIONS:
    The time series is sorted.
DESCRIPTION: 
    Uses a recurrent neural network to predict a number of new COVID-19 cases
    into the future. Then defines a direction of the trend line within the
    window.
REQUEST BODY: 
  {
      "country_region_code": "US",
      "look_forward_days": 3,
      "requested_date": "2020-06-06"
  }
RETURNS: 
    {
      "country_region_code": "US",
      "prediction_date": "2020-06-04",
      "prediction_new_cases": "26710",
      "starting_date": "2020-06-01",
      "success": true,
      "trend": "downward"
    }, 200
```
```
3. GET '/codes'
ASSUMPTIONS:
    A file names countryCodesNames.txt  exists and can be loaded as CSV.
DESCRIPTION: 
    Loads a file with a delimiter (as if it was CSV) and returns a list
    of dictionaries converted to JSON.
HEADERS:
  'Access-Control-Allow-Origin: *'
RETURNS: 
    {
      'results': [
                    {
                        "country_code": "US",
                        "map_name": "usa_en"
                    }, 
                    ...]
    }, 200
```

###### Trend line description
Since the data fluctuates it is not relevant for defining a direction of trend. 
<br>
It should be a directed line, thus a linear regression with polynomial features
was applied to available data appended with predicted data. 
<br>
Next the lookahead window (which is also a lookback distance) was considered
for defining the trend direction. 
<br>
Since the lookahead distance is relatively short, it make sense to compare only
the starting and ending dates of the prediction window.
<br> 
If the pandemic still there for a few more months or years, then it is necessary
to apply another technique for defining a direction of a trend line (expecting
a fluctuating curve for larger prediction windows).
![trend-US-polyreg-endpoint](https://gist.githubusercontent.com/eli-halych/908ca870a39bbbf0348f253ec7b0270e/raw/c835f0258ff1d1e76eeb48246bf8748d7c015b9b/trend-US-COVID-19_new-cases.png)

Region codes are described here:
[`./datasets/README.md`](./datasets/README.md)

### Tests
All endpoints are covered with unittests. To call tests, call the main test class
in [`./test.py`](./test.py)