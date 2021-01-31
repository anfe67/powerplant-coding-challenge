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


## To run it (tested on a Raspberry Pi 4 running Ubuntu 20.04 and Python 3.8.5): 
- Clone the github repository:
```
git clone https://github.com/anfe67/powerplant-coding-challenge.git
```
- Create and activate a virtual environment and install the requirements (make sure python3-venv is installed)
```
cd powerplant-coding-challenge/
python3 -m venv venv
```
- Install the requirements> 
```
pip install -r requirements.txt
```
- I had an issue with json2html, I had to run separately 
```
pip install json2html
```

- unit tests (4 example payloads are used, the three provided and 1 unfeasible) can be run : 
```
python3 -m unittest test/test_logic.py
```

- just run python challenge_server.py
```
python challenge_server.py
```
- Point your browser to the monitoring page: http://127.0.0.1:8888/monitor 


- stimulate the server by posting a json payload at address 127.0.0.1:888/productionplan, using either postman or RESTER
from Chrome or other tools, observe the solutions populate the web page.
This image is a screenshot obtained on the Raspberry Pi. 
Sometimes a picture is worth 1000 words! [example_usage_rpi4.png]
 







