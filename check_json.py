import json

# Load and inspect the JSON structure
print("Loading classes.json...")
with open('classes.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Show the structure
print("\n=== JSON Structure ===")
print(f"Type: {type(data)}")

if isinstance(data, dict):
    print(f"Top-level keys: {list(data.keys())}")
    print("\n=== First few lines of JSON ===")
    print(json.dumps(data, indent=2)[:500])
elif isinstance(data, list):
    print(f"Number of items: {len(data)}")
    if len(data) > 0:
        print("\n=== First item structure ===")
        print(f"Keys in first item: {list(data[0].keys())}")
        print(json.dumps(data[0], indent=2))

print("\n=== Full first 1000 characters ===")
with open('classes.json', 'r', encoding='utf-8') as f:
    print(f.read()[:1000])