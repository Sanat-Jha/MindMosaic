import requests
from web3 import Web3
from web3.exceptions import ContractLogicError, ABIFunctionNotFound
from datetime import datetime
import json

# Connect to Blockchain
INFURA_API_KEY = "989c9a51fc8e4cbb97dfa5d1cd5ab317"
rpc_url = f"https://sepolia.infura.io/v3/{INFURA_API_KEY}"
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Contract details
contract_address = "0x12162baB20326b2b3606bf7aCAED704457A6bfE6"
contract_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "dreamer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "ipfsHash",
                "type": "string"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "DreamLogged",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "user",
                "type": "address"
            }
        ],
        "name": "getDreamsByUser",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "dreamer",
                        "type": "address"
                    },
                    {
                        "internalType": "string",
                        "name": "ipfsHash",
                        "type": "string"
                    },
                    {
                        "internalType": "uint256",
                        "name": "timestamp",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct DreamChain.Dream[]",
                "name": "",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]

def get_dream_cids(user_address):
    """Get dreams for a specific user"""
    try:
        # Initialize contract
        contract = web3.eth.contract(
            address=web3.to_checksum_address(contract_address),
            abi=contract_abi
        )
        
        # Ensure proper address formatting
        user_address = web3.to_checksum_address(user_address)
        
        # Call the contract function
        dreams = contract.functions.getDreamsByUser(user_address).call()
        print(f"Raw dreams from contract: {dreams}")  # Debug print
        
        # Format the results
        formatted_dreams = []
        for dream in dreams:
            formatted_dream = {
                'dreamer': dream[0],
                'ipfsHash': dream[1],
                'timestamp': datetime.fromtimestamp(dream[2]).strftime('%Y-%m-%d %H:%M:%S')
            }
            formatted_dreams.append(formatted_dream)
        
        print(f"Formatted dreams: {formatted_dreams}")  # Debug print
        return formatted_dreams
    
    except Exception as e:
        print(f"Error fetching dreams: {str(e)}")
        return None

def fetch_dream_text(cid):
    """Fetch dream text from Lighthouse using CID"""
    try:
        # Try multiple IPFS gateways
        gateways = [
            f"https://gateway.lighthouse.storage/ipfs/{cid}",
            f"https://ipfs.io/ipfs/{cid}",
            f"https://cloudflare-ipfs.com/ipfs/{cid}"
        ]
        
        for gateway in gateways:
            print(f"Trying gateway: {gateway}")  # Debug print
            try:
                response = requests.get(gateway, timeout=10)
                print(f"Response status code: {response.status_code}")  # Debug print
                print(f"Response content: {response.text[:200]}")  # Debug print first 200 chars
                
                if response.status_code == 200:
                    try:
                        # Try to parse as JSON first
                        dream_data = json.loads(response.text)
                        if isinstance(dream_data, dict):
                            # Look for common content fields
                            for field in ['content', 'dream', 'text', 'description']:
                                if field in dream_data:
                                    return dream_data[field]
                            # If no known fields found, return the whole JSON as string
                            return json.dumps(dream_data)
                    except json.JSONDecodeError:
                        # If not JSON, return the raw text
                        return response.text.strip()
            except requests.exceptions.RequestException as e:
                print(f"Error with gateway {gateway}: {str(e)}")
                continue
        
        print("Failed to fetch dream text from all gateways")
        return None
    except Exception as e:
        print(f"Error in fetch_dream_text: {str(e)}")
        return None

def mainfetch():
    user_address = "0x37dC3933E0f9a1d624136A945905D08550eb9C58"
    print(f"Fetching dreams for address: {user_address}")
    
    # Get dream data from the blockchain
    dreams = get_dream_cids(user_address)
    if dreams:
        print(f"\nFound {len(dreams)} dreams")
        
        # Extract CIDs and fetch dream texts
        dream_texts = []
        for dream in dreams:
            cid = dream['ipfsHash']
            print(f"\nProcessing CID: {cid}")
            
            text = fetch_dream_text(cid)
            if text:
                dream_texts.append(text)
                print("\nDream Details:")
                print(f"Dreamer: {dream['dreamer']}")
                print(f"CID: {cid}")
                print(f"Timestamp: {dream['timestamp']}")
                print(f"Dream Text: {text}")
            else:
                print(f"Failed to fetch text for CID: {cid}")
                
        print("\nAll Dream Texts:")
        dreamsList = []
        for i, text in enumerate(dream_texts, 1):
            print(f"\nDream {i}:")
            print(text)
            dreamsList.append(text)
        return dreamsList
    else:
        print("No dreams found or error occurred")

