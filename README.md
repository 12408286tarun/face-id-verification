# Face ID Verification & Digital Identity Verification System

An integrated identity verification system that combines **Face Recognition, Image Hashing, Reverse Image Search, and Blockchain Verification** into a single Flask-based application.

The system accepts an image either through **file upload or camera capture**, verifies the presence of a face, generates a 128-dimensional face encoding and SHA-256 image hash, uploads the image to ImgBB to obtain a publicly accessible image URL, performs reverse image search using SerpApi, and finally verifies/registers the image hash on the Ethereum Sepolia blockchain using a Solidity smart contract.

---

## 📌 Project Overview

The purpose of this project is to demonstrate how multiple technologies can be integrated into one end-to-end digital identity and image verification workflow.

The application combines:

- Face Detection
- Face Encoding
- Image Hashing
- Image Hosting
- Reverse Image Search
- Blockchain-based Verification
- Smart Contract Interaction
- Flask Web Application

The complete workflow is:

```text
Image Upload / Camera Capture
            ↓
      Image Validation
            ↓
       Face Detection
            ↓
      Face Encoding
            ↓
       SHA-256 Hash
            ↓
       ImgBB Upload
            ↓
     Public Image URL
            ↓
    SerpApi Reverse Search
            ↓
   Blockchain Hash Check
            ↓
   Register if not found
            ↓
       Final Result

🚀 Features

Face Verification
- Accepts uploaded images.
- Supports camera capture.
- Detects faces using the face-recognition library.
- Uses dlib internally for face detection and encoding.
- Generates a 128-dimensional face encoding.
- Rejects images containing multiple faces.
- Provides useful validation messages when:
  - No face is detected.
  - Multiple faces are detected.
  - Image is invalid.
  - Face encoding fails.
Image Hashing
Every successfully processed image generates a SHA-256 hash.
The hash acts as a unique fingerprint of the image file.
Example:
228b9cc047db079bdcb0a60bff8847bdb2d6b96e07d34bd00b7805a087ac77d1
The hash is later used for blockchain verification.
🔎 Reverse Image Search
After successful face processing, the application uploads the image to ImgBB.
The ImgBB API returns a publicly accessible image URL.
Example:
https://i.ibb.co/...
That URL is then passed to SerpApi.
The application uses the:
google_reverse_image
SerpApi engine to search for visually related or matching images on the web.
The search module returns information such as:
- Title
- Source
- URL
- Snippet
⛓️ Blockchain Verification
The generated SHA-256 image hash is checked against a Solidity smart contract deployed on the Ethereum Sepolia test network.
The application performs two operations:
1. Verify Hash
The application first checks whether the image hash already exists on the blockchain.
If the hash exists:
Verified = True
The smart contract can return:
- Verification status
- Timestamp
- Uploader address
2. Register Hash
If the hash is not already registered, the application sends a blockchain transaction to register it.
After successful registration, the transaction hash is returned.
🧠 Smart Contract

The project uses the Solidity contract:
PostVerifier.sol
The contract provides two main functions:
registerPost(bytes32 fingerprint)
and
verifyPost(bytes32 fingerprint)
registerPost()
Stores an image fingerprint on the blockchain.
verifyPost()
Checks whether a fingerprint has been registered and returns:
verified
timestamp
uploader

🌐 Ethereum Network
The blockchain component uses the Ethereum Sepolia test network.
Network:
Ethereum Sepolia
Chain ID:
11155111
The deployed contract address used by the Python application is:
0xc0d6300826d9da999f57fd55812846c027e9e05f
This is a testnet deployment. It should not be considered a production deployment.

🏗️ Technology Stack
Frontend
- HTML
- CSS
- JavaScript
Backend
- Python
- Flask
Face Recognition
- face-recognition
- dlib
- OpenCV
- NumPy
- Pillow
Reverse Image Search
- ImgBB API
- SerpApi
Blockchain
- Solidity
- Web3.py
- Hardhat
- Ethereum Sepolia

📁 Project Structure
face-id-verification
│
├── app1.py
├── facemodule1.py
├── search_module.py
├── search_module.ipynb
│
├── templates
│   └── index.html
│
├── sample.jpg
├── test_image.jpg
├── testfacemodule1.py
│
├── Blockchain
│   └── blockchain
│       ├── blockchain_module.py
│       ├── hardhat.config.ts
│       ├── package.json
│       ├── package-lock.json
│       ├── tsconfig.json
│       │
│       ├── contracts
│       │   └── PostVerifier.sol
│       │
│       └── scripts
│           └── deploy.ts
│
└── .gitignore

⚙️ Installation & Setup

1. Clone the Repository
git clone https://github.com/12408286tarun/face-id-verification.git
cd face-id-verification
🐍 Python Setup
This project uses Python 3.11.
Check the installed Python version:
py -3.11 --version
Expected:
Python 3.11.x
Create a virtual environment:
py -3.11 -m venv venv
Activate it:
venv\Scripts\activate
📦 Python Dependencies
Install the required packages:
pip install flask
pip install face-recognition
pip install dlib
pip install numpy==1.26.4
pip install opencv-python==4.10.0.84
pip install pillow
pip install requests
pip install python-dotenv
pip install google-search-results
pip install web3
Important NumPy Version
The project uses:
numpy==1.26.4
This version is important for compatibility with the installed dlib/face-recognition environment.

🔐 Environment Variables
The project requires API credentials for:
- ImgBB
- SerpApi
- Ethereum Sepolia RPC
- Ethereum wallet private key
These values must never be committed to GitHub.
Create a .env file in the project root:
SERPAPI_KEY=your_serpapi_key
IMGBB_API_KEY=your_imgbb_api_key
Create another .env inside:
Blockchain/blockchain/
with:
SEPOLIA_RPC_URL=your_sepolia_rpc_url
SEPOLIA_PRIVATE_KEY=your_wallet_private_key
Security Warning
Never upload the actual .env files.
The project .gitignore prevents environment files and sensitive credentials from being uploaded.
🖼️ How Image Processing Works
When an image is uploaded:
Uploaded Image
      ↓
Image File Validation
      ↓
RGB Conversion
      ↓
Face Detection
      ↓
Face Selection
      ↓
Face Encoding
      ↓
SHA-256 Hash
The face module is implemented in:
facemodule1.py
The main processing function is:
process_uploaded_image()

👤 Face Detection
The project uses:
face_recognition.face_locations()
with the hog detection model.
The application is configured to reject multiple faces:
MULTIPLE_FACES_MODE = "reject"
This prevents the system from accidentally selecting the wrong person when an image contains multiple faces.

🧬 Face Encoding
After detecting a valid face, the application generates a face encoding.
The encoding contains:
128 dimensions
These numerical values represent facial characteristics extracted by the face-recognition model.
The application also displays a small preview of the encoding for demonstration purposes.
#️⃣ SHA-256 Image Hash
The application calculates a SHA-256 hash from the original image bytes.
Conceptually:
Image File
    ↓
SHA-256
    ↓
64-character hexadecimal hash
Example:
228b9cc047db079bdcb0a60bff8847bdb2d6b96e07d34bd00b7805a087ac77d1
This hash is used as the blockchain fingerprint.

☁️ ImgBB Image Upload
The application cannot directly send a local computer file to a remote reverse image search service that requires a public image URL.
Therefore, the workflow first uploads the image to ImgBB.
The application sends:
POST https://api.imgbb.com/1/upload
with the ImgBB API key and image file.
ImgBB returns a public image URL.
That URL is then passed to the reverse image search module.

🔎 SerpApi Reverse Image Search
The reverse image search implementation is located in:
search_module.py
The application uses:
GoogleSearch
from the SerpApi Python package.
The request uses:
params = {
    "engine": "google_reverse_image",
    "image_url": image_url,
    "api_key": serpapi_key
}
The important part is:
image_url
The URL comes from the previous ImgBB upload step.
Therefore:
Local Image
     ↓
ImgBB API
     ↓
Public Image URL
     ↓
SerpApi
     ↓
Google Reverse Image Search
     ↓
Search Result
The module extracts:
title
url
source
snippet
from the first available image result.

⛓️ Blockchain Python Integration
The Python blockchain integration is implemented in:
Blockchain/blockchain/blockchain_module.py
It uses:
from web3 import Web3
The application connects to Ethereum Sepolia using an RPC URL.
The connection is created using:
Web3.HTTPProvider(RPC_URL)

🔍 Blockchain Verification Flow
After generating the image hash:
SHA-256 Image Hash
        ↓
verify_hash()
        ↓
Smart Contract
        ↓
Hash Found?
If the hash is already registered:
Verified = True
If it is not registered:
verify_hash()
      ↓
verified = False
      ↓
register_hash()
      ↓
Blockchain Transaction
      ↓
Transaction Receipt
      ↓
Hash Registered

🧾 Blockchain Transaction
The registration function:
register_hash()
performs the following operations:
1. Converts the hexadecimal fingerprint into bytes.
2. Loads the wallet account using the private key.
3. Gets the pending transaction nonce.
4. Builds the smart contract transaction.
5. Signs the transaction.
6. Sends the raw transaction to Sepolia.
7. Waits for the transaction receipt.
8. Returns the transaction hash.
The transaction uses the Sepolia chain ID:
11155111

🌐 Flask Application
The main application is:
app1.py
Run it using:
py -3.11 app1.py
The Flask server starts on:
http://127.0.0.1:5000
Open the address in a browser.

📤 Upload Flow
The application provides an image upload interface.
The upload request is handled by:
@app.route("/upload", methods=["POST"])
The uploaded image is temporarily saved inside:
uploads/
The image is then processed by:
process_and_render()
📷 Camera Capture Flow
The application also supports camera capture.
The captured image is converted from the browser's data URL into image bytes.
The image is temporarily stored as a JPG file.
The same processing pipeline is then used:
Camera Capture
      ↓
Image Bytes
      ↓
Temporary JPG
      ↓
Face Processing
      ↓
Hash
      ↓
Reverse Search
      ↓
Blockchain
🔗 Complete End-to-End Flow
The complete application works as follows:
                   USER
                    │
                    ▼
          Upload Image / Camera
                    │
                    ▼
             Flask Application
                    │
                    ▼
            Image Validation
                    │
                    ▼
             Face Detection
                    │
                    ▼
             Face Encoding
                    │
                    ▼
              SHA-256 Hash
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
       ImgBB              Blockchain
          │                   │
          ▼                   ▼
   Public Image URL      Verify Hash
          │                   │
          ▼                   │
      SerpApi                 │
          │                   │
          ▼                   │
 Reverse Image Search         │
          │                   │
          └─────────┬─────────┘
                    ▼
              Final Result
🧪 Testing
The project contains:
testfacemodule1.py
for testing the face-processing module.
Test images include:
sample.jpg
test_image.jpg
The application was tested with uploaded images and successfully demonstrated:
- Face detection
- 128-dimensional face encoding
- Image hashing
- ImgBB image upload
- Reverse image search
- Blockchain hash verification
- Blockchain hash registration
- Successful transaction confirmation
🛠️ Useful Development Commands
Check Python
py -3.11 --version
Activate Virtual Environment
venv\Scripts\activate
Run Flask Application
py -3.11 app1.py
Check Git Status
git status
Stage Changes
git add .
Commit Changes
git commit -m "Update project"
Push Changes
git push
⛓️ Hardhat / Blockchain Development
Move into the blockchain directory:
cd Blockchain\blockchain
Install Node.js dependencies:
npm install
Compile the Solidity contracts:
npx hardhat compile
The main contract for this project is:
contracts/PostVerifier.sol
Deployment scripts are located in:
scripts/
The deployed contract is configured in:
blockchain_module.py
🔧 Blockchain Configuration
The Hardhat project contains:
hardhat.config.ts
package.json
package-lock.json
tsconfig.json
contracts/
scripts/
Generated directories such as:
node_modules/
artifacts/
cache/
are excluded from Git using .gitignore.
🔒 Security
The project uses API keys and a blockchain wallet private key.
The following files must never be uploaded:
.env
*.env
The repository .gitignore also excludes generated and unnecessary directories:
venv/
__pycache__/
*.pyc
uploads/
node_modules/
artifacts/
cache/
Never hard-code API keys or private keys inside Python, Solidity, TypeScript, HTML, or JavaScript source files.
⚠️ Important Notes
1. Internet Connection
The application requires internet access for:
- ImgBB API
- SerpApi
- Ethereum Sepolia RPC
2. API Keys
Valid ImgBB and SerpApi credentials are required.
3. Blockchain Wallet
The Sepolia wallet must have test ETH to submit blockchain transactions.
4. Camera
Camera capture depends on browser permissions, webcam availability, lighting, and image quality.
5. Test Network
The blockchain implementation uses Ethereum Sepolia testnet and is intended for demonstration/testing purposes.
📊 Example Verification Result
A successful run can produce information such as:
Face Detected: Yes
Faces: 1

Encoding:
128 dimensions

Image Hash:
SHA-256 fingerprint

Reverse Image Search:
Search result returned

Blockchain:
VERIFIED ✓

Network:
Ethereum Sepolia

Transaction:
Successful

🎯 Project Objective
This project demonstrates the integration of multiple technologies into a single verification workflow.
Instead of relying on only one verification technique, the system combines:
Biometric Information
        +
Image Fingerprinting
        +
Web-Based Image Search
        +
Blockchain Verification
This provides a practical demonstration of how modern web, AI/computer-vision, API, and blockchain technologies can work together in an identity verification system.

📌 Future Improvements
Possible future enhancements include:
- Persistent user accounts
- Database integration
- Better face matching against registered identities
- Multiple image comparison
- Improved camera capture
- Authentication and authorization
- More detailed reverse-image-search results
- Blockchain event tracking
- Transaction explorer links
- Production-grade deployment
- Cloud hosting
- Improved UI/UX
- Automated testing
- Docker-based deployment

📄 License
This project is intended for educational and demonstration purposes.
