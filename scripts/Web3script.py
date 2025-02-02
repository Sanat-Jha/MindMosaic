from web3 import Web3
import json
from datetime import datetime
import requests
from fastapi import FastAPI, HTTPException
from eth_account.signers.local import LocalAccount
from eth_typing import Address

class DreamChainAutomation:
    def _init_(self):
        # Initialize Web3 with proper Infura URL
        self.w3 = Web3(Web3.HTTPProvider('https://sepolia.infura.io/v3/989c9a51fc8e4cbb97dfa5d1cd5ab317'))
        
        # Contract details
        self.contract_address = Address(bytes.fromhex('0xb2dB6D79B65cb788d8d57749367D4D6F76b22dd4'.replace('0x', '')))
        
        # Load contract ABI
        try:
            with open('contract_abi.json', 'r') as f:
                contract_abi = json.load(f)
                # Verify ABI contains the required function
                function_names = [item['name'] for item in contract_abi if item.get('type') == 'function']
                print("Available contract functions:", function_names)
        except FileNotFoundError:
            raise Exception("contract_abi.json file not found")
        except json.JSONDecodeError:
            raise Exception("Invalid JSON in contract_abi.json")
        
        # Initialize contract
        self.contract = self.w3.eth.contract(
            address=self.contract_address,
            abi=contract_abi
        )
        
        # Set up account
        private_key = 'b66033e7d30edc308c3571e1ad6de91040f5f5a86e0d7212d88519cdeaf0eb12'
        self.account: LocalAccount = self.w3.eth.account.from_key(private_key)
        
    async def upload_to_lighthouse(self, dream_content):
        """Upload dream content to Lighthouse and get CID"""
        try:
            # Prepare dream data
            dream_data = {
                "content": dream_content,
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "source": "web_interface"
                }
            }
            
            # Convert to JSON string
            json_str = json.dumps(dream_data)
            
            # Upload to Lighthouse using the direct API approach
            upload_url = "https://node.lighthouse.storage/api/v0/add"
            headers = {
                "Authorization": f"Bearer 4b1c4a53.c8dacd55a95d4f27a6219407b8f5c677"
            }
            
            # Create temporary file to upload
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_file:
                temp_file.write(json_str)
                temp_file.flush()
                
                with open(temp_file.name, 'rb') as file:
                    files = {'file': file}
                    response = requests.post(upload_url, headers=headers, files=files)
            
            if response.status_code == 200:
                return response.json()['Hash']
            else:
                raise Exception(f"Lighthouse upload failed: {response.text}")
            
        except Exception as e:
            print(f"Lighthouse upload failed: {e}")
            raise

    def store_dream_in_contract(self, cid):
        """Store CID in smart contract using submitDream function"""
        try:
            # Get nonce
            nonce = self.w3.eth.get_transaction_count(self.account.address)
            
            # Estimate gas
            gas_estimate = self.contract.functions.submitDream(cid).estimate_gas({
                'from': self.account.address,
                'nonce': nonce
            })
            
            # Get gas price
            gas_price = self.w3.eth.gas_price
            
            # Build transaction
            transaction = {
                'nonce': nonce,
                'gas': gas_estimate,
                'gasPrice': gas_price,
                'to': self.contract_address,
                'data': self.contract.functions.submitDream(cid).build_transaction()['data'],
                'chainId': 11155111  # Sepolia chain ID
            }
            
            # Sign transaction
            signed = self.account.sign_transaction(transaction)
            
            # Send transaction
            tx_hash = self.w3.eth.send_raw_transaction(signed.raw_transaction)
            
            # Wait for transaction receipt
            receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)
            
            return receipt
            
        except Exception as e:
            print(f"Contract storage failed: {e}")
            raise

    async def process_dream(self, dream_content):
        """Main function to handle dream processing"""
        try:
            # Upload to Lighthouse
            print("Uploading to Lighthouse...")
            cid = await self.upload_to_lighthouse(dream_content)
            print(f"Uploaded to Lighthouse with CID: {cid}")
            
            # Store in contract
            print("Storing in smart contract...")
            receipt = self.store_dream_in_contract(cid)
            print(f"Stored in contract. Transaction hash: {receipt['transactionHash'].hex()}")
            
            return {
                "status": "success",
                "cid": cid,
                "transaction_hash": receipt['transactionHash'].hex()
            }
            
        except Exception as e:
            print(f"Dream processing failed: {e}")
            return {
                "status": "error",
                "error": str(e)
            }

# FastAPI app
app = FastAPI()
dream_chain = DreamChainAutomation()

@app.post("/submit-dream")
async def submit_dream(dream_content: str):
    result = await dream_chain.process_dream(dream_content)
    
    if result["status"] == "error":
        raise HTTPException(status_code=500, detail=result["error"])
        
    return result


    
async def lighthousetochain():
    dream_content = "I was flying over a crystal city..."
    dream_chain = DreamChainAutomation()
    result = await dream_chain.process_dream(dream_content)
    
    if result["status"] == "success":
        print("\nDream successfully processed!")
        print(f"IPFS CID: {result['cid']}")
        print(f"Transaction Hash: {result['transaction_hash']}")
    else:
        print(f"\nError: {result['error']}")

