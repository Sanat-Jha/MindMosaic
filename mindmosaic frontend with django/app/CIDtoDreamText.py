import requests
from .fetchCID import get_dream_cids

def fetch_dream_text(cid):
    """Fetch dream text from Lighthouse using CID"""
    url = f"https://gateway.lighthouse.storage/ipfs/{cid}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text.strip()  # Extract dream text
    else:
        return None

def mainfetch():
    user_address = "0x37dC3933E0f9a1d624136A945905D08550eb9C58"
    
    # Get dream data from the blockchain
    dreams = get_dream_cids(user_address)

    if dreams:
        print("\nFetched Dreams:")
        
        # Extract CIDs from the retrieved dream data
        dream_cids = [dream['ipfsHash'] for dream in dreams]

        # Fetch dream texts from Lighthouse using the CIDs
        fetched_dreams = {cid: fetch_dream_text(cid) for cid in dream_cids}
        dreamstext = []
        # Print all fetched dream texts
        for cid, text in fetched_dreams.items():
            dreamstext.append(text)
            print(f"\nCID: {cid}")
            print(f"Dream Text: {text}\n")
        print(dreamstext)
    else:
        print("No dreams found or error occurred")
