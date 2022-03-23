# Dependencies
from flask import Flask

# Create a new flask app 'instance'
app = Flask(__name__)

# define 'starting point' a.k.a the 'root'
@app.route('/')  ## the '/' denotes that we want to put our data at the root of our routes
# create a function that i want in this specific route
def hello_world():
    return 'Hello World'

# Create another route
@app.route('/hi') 
def cards():
    nums = ['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    suits = ['C','D','H','S']
    cards = [num+suit for suit in suits for num in nums]
    return cards