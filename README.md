# ENGIE Powerplant Allocation Challenge

## Implementation technology 

All implemented in Python. Required libraries in requirements.txt. 

Based on Flask - For the API exposed on 0.0.0.0:8888/productionplan methods = ['POST'], receives a json payload and 
returns a json solution, as in instructions. 

Also exposes an 0.0.0.0:8888/monitor methods=['GET'], which connects to a Flask-Socketio socket and returns a flask 
template. Every request emitted by a client is then forwarded to all monitoring clients connecting to this page. 

The request connection and event reception are handled in javascript.  

## Details 

The cost of the co2 emissions is calculated into the price pere MW produced by the powerstation and the powerstations 
are ordered in order of price per MW, increasing. 

The algorithm is an attempt to a recursive backtracking algorithm. To avoid tricky floating point arithmetics, request 
and payloads have been multiplied by 10 and then converted back before returning the responses. 

As the steps represent 0.1 of a MW, it has been necessary to increase the depth of the recursion. The algorithm works on 
the payload submitted, it is capable of detecting when a payload is not feasible (too high) and when a solution was not 
found (in this case it may exist or not). It has also been tested on a number of other cases. 
If a solution is not found, {"name": "SOLUTION", "p": "NOT FOUND"} is added at the end of the response. 
If a solution is not feasible, then {"name": ""SOLUTION Unfeasible"", "reason": "Requested load LOAD too high for our 
powerstations"} is returned. 


## To run it: 
- Clone the github repository: 
- Create a virtual environment and install the requirements 
- just run python challenge_server.py
- unit tests can be run :   
- stimulate the server by posting a json payload at address 127.0.0.1:888/productionplan 