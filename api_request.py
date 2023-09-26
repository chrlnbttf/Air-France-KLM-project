'''
This document list the api request for each quiery.
'''

# @api.get("/check")
curl -X 'GET' \
  'http://127.0.0.1:8000/check' \
  -H 'accept: application/json'

# @api.get("/flights/{IATA: str}")

## Case 1 : success with IATA = "AMS"
curl -X 'GET' \
  'http://127.0.0.1:8000/flights/{IATA: str}?IATA=AMS' \
  -H 'accept: application/json'"

## Case 2 : error 400 with "AMD"
curl -X 'GET' \
  'http://127.0.0.1:8000/flights/{IATA: str}?IATA=AMD' \
  -H 'accept: application/json'success with IATA = "AMS"

# @api.get("/flights/{volume: int})
curl -X 'GET' \
  'http://127.0.0.1:8000/flights/{volume: int}?volume=1' \
  -H 'accept: application/json'

# @api.get("/flights/)
curl -X 'GET' \
  'http://127.0.0.1:8000/flights/\
  -H 'accept: application/json'

# @api.get("/status")
curl -X 'GET' \
  'http://127.0.0.1:8000/status' \
  -H 'accept: application/json'

# @api.get("/delays")
curl -X 'GET' \
  'http://127.0.0.1:8000/delays' \
  -H 'accept: application/json'

# @api.get("/delays/departure_airport")
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/departure_airport' \
  -H 'accept: application/json'

# @api.get("/delays/{flight_number: int})

## Case 1 : Flight with delayed departure with flight nnumber = 1855
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{flight_number: int}?flight_number=1855' \
  -H 'accept: application/json'

## Case 2 : Flight with departure on-time with flight number = 747
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{flight_number: int}?flight_number=747' \
  -H 'accept: application/json'

## Case 3 : Error 404 with error flight number = 0
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{flight_number: int}?flight_number=0' \
  -H 'accept: application/json'

# @api.get("/delays/{IATA: str}"

## Case 1 : Success, delayed flight with IATA = AMS
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{IATA: str}?IATA=AMS' \
  -H 'accept: application/json'

## Case 2 : Succes, On-time flight with IATA = PAR
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{IATA: str}?IATA=PAR' \
  -H 'accept: application/json'

## Case 3 : Error 400 with IATA code = AMR
curl -X 'GET' \
  'http://127.0.0.1:8000/delays/{IATA: str}?IATA=AMR' \
  -H 'accept: application/json'








