import json, sys

transcript_path = r"C:\Users\gkpan\.gemini\antigravity\brain\455879ea-5c59-4ef5-8181-2a16441a2101\.system_generated\logs\transcript_full.jsonl"
with open(transcript_path, 'r', encoding='utf-8') as f:
    for line_idx, line in enumerate(f):
        if line_idx == 152:
            data = json.loads(line)
            tool_calls = data.get('tool_calls', [])
            for tc in tool_calls:
                content = tc.get('args', {}).get('CodeContent', '')
                if content.startswith('"') and content.endswith('"'):
                    content = json.loads(content)
                with open("VERY_FIRST_MODERNIZATION_PLAN.md", "w", encoding="utf-8") as out:
                    out.write(content)
                print(f"Extracted Line 152 successfully: {len(content)} characters, {len(content.splitlines())} lines.")
