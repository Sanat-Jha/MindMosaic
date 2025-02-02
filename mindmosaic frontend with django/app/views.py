import os
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json 
from lighthouseweb3 import Lighthouse
from .Web3Mohit import lighthousetochain
from .fetchCID import mainfetch
from textblob import TextBlob
import asyncio

class DreamCategorizer:
    def __init__(self):
        # Keywords for different dream categories
        self.categories = {
            'nightmare': ['scary', 'terrifying', 'horror', 'fear', 'afraid', 'chase', 'dark', 'monster', 'death', 'panic'],
            'funny': ['laugh', 'hilarious', 'funny', 'joke', 'amusing', 'silly', 'ridiculous', 'comedy'],
            'adventure': ['explore', 'journey', 'quest', 'travel', 'discover', 'adventure', 'exciting'],
            'romantic': ['love', 'kiss', 'romantic', 'date', 'partner', 'relationship'],
            'flying': ['fly', 'flying', 'float', 'soar', 'sky', 'wings'],
            'sad': ['sad', 'cry', 'tears', 'depressed', 'grief', 'loss', 'heartbroken'],
        }
    
    def analyze_sentiment(self, text):
        analysis = TextBlob(text)
        return analysis.sentiment.polarity
    
    def categorize_dream(self, dream_text):
        dream_text = dream_text.lower()
        categories = []
        
        # Check for each category's keywords
        for category, keywords in self.categories.items():
            if any(keyword in dream_text for keyword in keywords):
                categories.append(category)
        
        # If no specific categories found, categorize based on sentiment
        if not categories:
            sentiment = self.analyze_sentiment(dream_text)
            if sentiment > 0.3:
                categories.append('positive')
            elif sentiment < -0.3:
                categories.append('negative')
            else:
                categories.append('neutral')
        
        return categories

def home(request):
    return render(request, 'home.html')

# Modified views.py
@csrf_exempt
def newdream(request):
    data = json.loads(request.body)
    dream_text = data.get('dream_text')
    tags = data.get('tags')
    walletAddress = data.get('wallet_address')
    
    # Categorize the dream
    categorizer = DreamCategorizer()
    categories = categorizer.categorize_dream(dream_text)
    # Create JSON data with categories
    json_data = {
        "dream_text": dream_text,
        "tags": tags,
        "wallet_address": walletAddress,
        "categories": categories
    }
    json_filename = "dream_data.json"
    
    # Save and upload JSON data
    with open(json_filename, "w") as json_file:
        json.dump(json_data, json_file)
    
    lh = Lighthouse(token="fd756e56.99bc2280aa4a40bf80bdc9b295ccd31f")
    response = lh.upload(json_filename)
    
    if hasattr(response, 'data') and hasattr(response.data, 'Hash'):
        json_data['cid'] = response.data.Hash
    
    os.remove(json_filename)
    asyncio.run(lighthousetochain())
    return JsonResponse({'status': 'success', 'data': json_data})

@csrf_exempt
def get_dreams(request):
    dreams = mainfetch()  # Now returns list of dream text strings
    processed_dreams = []
    categorizer = DreamCategorizer()
    
    for dream_text in dreams:
        # Create a new dream data structure for each dream text
        dream_data = {
            "dream_text": json.loads(dream_text)["dream_text"],
            "categories": categorizer.categorize_dream(dream_text)
        }
        processed_dreams.append(dream_data)

    return JsonResponse({'status': 'success', 'data': processed_dreams})