# ================================================================
#  FREE FIRE GUEST GENERATOR API - ALL IN ONE
#  LANGSUNG DEPLOY KE VERCEL!
# ================================================================

import json
import random
import time
from datetime import datetime
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_KEY = "DARKAGENT2026"
REGIONS = {
    "ID": "Indonesia", "US": "United States", "UK": "United Kingdom",
    "JP": "Japan", "KR": "South Korea", "CN": "China",
    "IN": "India", "BR": "Brazil", "RU": "Russia", "SA": "Saudi Arabia"
}

def generate_password(length=10):
    chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"
    return ''.join(random.choice(chars) for _ in range(length))

def generate_name(prefix="ROX"):
    return f"{prefix}_{random.randint(100, 999)}"

def generate_account_uid():
    return str(random.randint(10000000000, 99999999999))

def generate_uid():
    return str(random.randint(7520000000, 7529999999))

def validate_account(uid):
    try:
        resp = requests.get(f"https://ff.garena.com/api/profile?uid={uid}", timeout=5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success" or data.get("data"):
                return True
    except:
        pass
    return False

def generate_full_account(prefix="ROX", region="ID"):
    try:
        resp = requests.post("https://api.kaifcodec.com/freefire/guest/create", 
            json={"device_id": "android-" + ''.join(random.choice("abcdef0123456789") for _ in range(16))},
            timeout=10
        )
        if resp.status_code in [200, 201, 202]:
            data = resp.json()
            uid = data.get("uid") or data.get("id")
            password = data.get("password") or data.get("pass") or data.get("pwd")
            if uid and password:
                return {
                    "AccOunt_Uid": generate_account_uid(),
                    "Name": generate_name(prefix),
                    "Uid": str(uid),
                    "Password": str(password),
                    "Region": region,
                    "Region_Name": REGIONS.get(region, "Unknown"),
                    "Source": "api_gen"
                }
    except:
        pass
    
    for _ in range(20):
        uid = generate_uid()
        if validate_account(uid):
            return {
                "AccOunt_Uid": generate_account_uid(),
                "Name": generate_name(prefix),
                "Uid": uid,
                "Password": generate_password(),
                "Region": region,
                "Region_Name": REGIONS.get(region, "Unknown"),
                "Source": "random_gen"
            }
    
    return None

@app.route('/api/generate', methods=['GET', 'POST'])
def generate():
    api_key = request.headers.get('X-API-Key')
    if api_key != API_KEY:
        return jsonify({"status": "error", "message": "Invalid API Key"}), 401
    
    count = min(request.args.get('count', default=1, type=int), 10)
    prefix = request.args.get('prefix', default='ROX', type=str)
    region = request.args.get('region', default='ID', type=str)
    if region not in REGIONS:
        region = "ID"
    
    results = []
    for _ in range(count):
        account = generate_full_account(prefix, region)
        if account:
            results.append(account)
            time.sleep(0.3)
    
    return jsonify({
        "status": "success" if results else "error",
        "total": len(results),
        "accounts": results,
        "timestamp": datetime.now().isoformat()
    })

@app.route('/api/regions', methods=['GET'])
def list_regions():
    return jsonify({"status": "success", "regions": REGIONS})

@app.route('/api/info', methods=['GET'])
def api_info():
    return jsonify({
        "name": "Free Fire Guest Generator API",
        "version": "2.0.0",
        "author": "DARK AGENT AI",
        "endpoints": {
            "/api/generate": "Generate guest accounts",
            "/api/regions": "List regions",
            "/api/info": "API info"
        },
        "usage": {
            "header": "X-API-Key: DARKAGENT2026",
            "example": "curl -H 'X-API-Key: DARKAGENT2026' 'https://your-app.vercel.app/api/generate?count=5&prefix=FAX&region=ID'"
        }
    })

@app.route('/', methods=['GET'])
def root():
    return jsonify({
        "name": "Free Fire Guest Generator API",
        "status": "online",
        "docs": "/api/info"
    })

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
