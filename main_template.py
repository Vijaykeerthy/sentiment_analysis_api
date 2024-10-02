from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from textblob import TextBlob
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

# Load the Tfidf and model for toxicity prediction
tfidf = pickle.load(open("tf_idf.pkt", "rb"))
nb_model = pickle.load(open("toxicity_model.pkt", "rb"))

# Define a function for toxicity prediction
def predict_toxicity(text: str):
    text_tfidf = tfidf.transform([text]).toarray()
    prediction = nb_model.predict(text_tfidf)
    class_name = "Toxic" if prediction == 1 else "Non-Toxic"
    return {
        "text": text,
        "class": class_name
    }

class SentimentAnalysis(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the sentiment analysis.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to analyze sentiment
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The original text
                            polarity:
                                type: number
                                description: The polarity of the sentiment
                            subjectivity:
                                type: number
                                description: The subjectivity of the sentiment
                            sentiment_classification:
                                type: string
                                description: The sentiment classification as neutral, positive, or negative
        """
        text = request.args.get('text')
        blob = TextBlob(text)
        sentiment = blob.sentiment

        sentiment_classification = 'positive' if sentiment.polarity > 0 else 'negative' if sentiment.polarity < 0 else 'neutral'

        response = {
            'text': text,
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            'sentiment_classification': sentiment_classification
        }
        return jsonify(response)

class ToxicityPrediction(Resource):
    def get(self):
        """
        This method responds to the GET request for this endpoint and returns the toxicity prediction.
        ---
        tags:
        - Text Processing
        parameters:
            - name: text
              in: query
              type: string
              required: true
              description: The text to predict toxicity
        responses:
            200:
                description: A successful GET request
                content:
                    application/json:
                      schema:
                        type: object
                        properties:
                            text:
                                type: string
                                description: The original text
                            class:
                                type: string
                                description: The toxicity classification as Toxic or Non-Toxic
        """
        text = request.args.get('text')
        result = predict_toxicity(text)
        return jsonify(result)

api.add_resource(SentimentAnalysis, "/sentimentanalysis")
api.add_resource(ToxicityPrediction, "/toxicity")

if __name__ == "__main__":
    app.run(debug=True)
