from flask import Flask, render_template, request, jsonify
import pickle

app = Flask(__name__)

# Load the trained ML model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

# Define a route to make predictions on new packets