from textblob import TextBlob

class APIIntegration:
    def analyze_sentiment(self, text: str) -> float:
        if not text:
            return 0.0
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity  
        return polarity