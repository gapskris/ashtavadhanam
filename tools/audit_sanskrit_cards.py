import json
import re
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

with open('content/data.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

for pidx, page in enumerate(d['pages'], 1):
    san = page.get('sanskritDevanagari', '')
    cards = [c.strip() for c in san.split('\n\n') if c.strip()]
    print(f'=== PAGE {pidx:02d} ({len(cards)} cards) ===')
    for cidx, card in enumerate(cards, 1):
        first_line = card.split('\n')[0]
        suspicious = []
        if re.search(r'[a-zA-Z]', card):
            suspicious.append('contains Latin')
        if re.search(r'[\x80-\xff]', card):
            suspicious.append('contains high-ascii')
        if ';' in card:
            suspicious.append('contains semicolon')
        if '?' in card:
            suspicious.append('contains question mark')
        
        words = re.findall(r'[\u0900-\u097F]+', card)
        for w in words:
            if re.search(r'^[ािीुूृॄेैोौ्ंँः]', w):
                suspicious.append(f'isolated matra on {w}')
            # Look for common KrutiDev / VedicBrahma decoding anomalies
            # e.g. dangling repha, broken conjuncts, unintended characters
            if '±' in w or 'Ø' in w or '×' in w or 'ß' in w:
                suspicious.append(f'unconverted glyph in {w}')
                
        alert_str = (' | ALERT: ' + ', '.join(suspicious)) if suspicious else ''
        print(f'  Card {cidx:02d}: {first_line[:65]}...{alert_str}')
