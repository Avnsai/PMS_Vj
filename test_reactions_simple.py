#!/usr/bin/env python3
"""
Simple test for reactions on existing comments
"""

import requests
import json

def test_reactions():
    # Login first
    login_response = requests.post(
        "https://typescript-fix-8.preview.emergentagent.com/api/auth/login",
        json={"email": "demo@company.com", "password": "demo123456"}
    )
    
    if login_response.status_code != 200:
        print("❌ Login failed")
        return False
        
    token = login_response.json()['tokens']['access_token']
    headers = {'Authorization': f'Bearer {token}', 'Content-Type': 'application/json'}
    
    # Test reaction on existing comment
    comment_id = "d9a56972-845a-43da-a439-3b7932b99779"  # Root comment from threading test
    
    reaction_response = requests.post(
        f"https://typescript-fix-8.preview.emergentagent.com/api/comments/{comment_id}/reactions?emoji=👍",
        headers=headers
    )
    
    print(f"Reaction response status: {reaction_response.status_code}")
    if reaction_response.status_code == 200:
        print("✅ Reaction added successfully")
        response_data = reaction_response.json()
        print(f"   Reaction count: {response_data.get('reaction_count', 0)}")
        print(f"   Reactions: {len(response_data.get('reactions', []))}")
        return True
    else:
        print(f"❌ Reaction failed: {reaction_response.text}")
        return False

if __name__ == "__main__":
    test_reactions()