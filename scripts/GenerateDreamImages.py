import requests

# Replace with your free DeepAI API key
API_KEY = "c9473c4e-1c85-4ae0-ad40-c0a2776c5c8a"

def generate_ai_image(dream_category):
    """Generate an AI image for a dream category using DeepAI API"""
    url = "https://api.deepai.org/api/text2img"

    headers = {
        "api-key": API_KEY
    }

    data = {
        "text": f"A surreal dreamscape representing {dream_category} dreams, with vibrant colors and ethereal lighting."
    }

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        image_url = response.json()["output_url"]
        print(f"Generated AI Image for {dream_category}: {image_url}")
        return image_url
    else:
        print("Error:", response.json())
        return None

# Example Usage
image_url = generate_ai_image("Flying Dreams")
print(f"Generated AI Image URL: {image_url}")