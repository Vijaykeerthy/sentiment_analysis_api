from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from textblob import TextBlob

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

def sentiment_analysis(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment
    polarity = sentiment.polarity

    # Calculate positive and negative percentages based on polarity (-1 to 1)
    positive_percentage = (polarity + 1) / 2 * 100  # Maps polarity (-1 to 1) to (0 to 100)
    negative_percentage = (1 - polarity) / 2 * 100  # Inverse mapping for negative polarity

    # Determine sentiment classification
    if polarity > 0:
        sentiment_classification = 'positive'
    elif polarity < 0:
        sentiment_classification = 'negative'
    else:
        sentiment_classification = 'neutral'

    return {
        'positive_percentage': f"{positive_percentage:.2f}%",
        'negative_percentage': f"{negative_percentage:.2f}%",
        'sentiment_classification': sentiment_classification
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
                            sentiment_classification:
                                type: string
                                description: The sentiment classification as neutral, positive, or negative
                            positive_percentage:
                                type: number
                                description: The percentage of positive sentiment
                            negative_percentage:
                                type: number
                                description: The percentage of negative sentiment
        """
        text = request.args.get('text')
        analysis_result = sentiment_analysis(text)

        blob = TextBlob(text)
        sentiment = blob.sentiment

        response = {
            'text': text,
            'polarity': sentiment.polarity,
            **analysis_result  # Add sentiment analysis results including positive/negative percentages
        }
        return jsonify(response)

# Adding the resource to the API
api.add_resource(SentimentAnalysis, "/sentimentanalysis")

if __name__ == "__main__":
    app.run(debug=True)
