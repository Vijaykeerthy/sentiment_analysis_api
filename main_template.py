from flask import Flask, jsonify, request
from flask_restful import Api, Resource
from flasgger import Swagger
from textblob import TextBlob

app = Flask(__name__)
api = Api(app)
swagger = Swagger(app)

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

        response = {
            'text': text,
            'polarity': sentiment.polarity,
            'subjectivity': sentiment.subjectivity,
            **analysis_result  # Add sentiment analysis results including positive/negative percentages
        }
        return jsonify(response)

api.add_resource(SentimentAnalysis, "/sentimentanalysis")

if __name__ == "__main__":
    app.run(debug=True)
