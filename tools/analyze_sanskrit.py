import json
import os
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
data_json = os.path.join(root, "content", "data.json")

with open(data_json, 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"{'Round':<6} | {'Audio':<5} | {'Turns':<5} | {'Artifacts':<9} | {'Sample Corrupted Tokens'}")
print("-" * 75)

for p in data['pages']:
    pnum = p['pageNumber']
    txt = p.get('sanskritDevanagari', '')
    raw = p.get('sanskritRawVedicBrahma', '')
    audio_cnt = p.get('audioCount', 0)
    turns = [x.strip() for x in txt.split('\n\n') if x.strip()]
    
    # Find all words with non-Devanagari artifacts (except standard punctuation)
    # Valid: Devanagari 0900-097F, Vedic 1CD0-1CFF, digits, whitespace, । ॥ - , ? ! ( ) " ' *
    corrupted_tokens = []
    words = re.findall(r'\S+', txt)
    for w in words:
        # Check if word contains any forbidden chars
        if re.search(r'[;£ÐÏÎ\)`~\[\]\{\}\+\=\^a-zA-Z\x80-\xff]', w):
            # Exclude words that are pure numbers or known punctuation/bell annotations
            clean_w = re.sub(r'[\(\)\"\'\*\।\॥\,\-\?\!\d:🔔]', '', w)
            if clean_w:
                corrupted_tokens.append(w)
                
    sample = " ".join(corrupted_tokens[:4]) if corrupted_tokens else "None (Clean)"
    print(f"R{pnum:02d}    | {audio_cnt:<5} | {len(turns):<5} | {len(corrupted_tokens):<9} | {sample}")
