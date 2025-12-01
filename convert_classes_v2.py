#!/usr/bin/env python3
"""
Convert classes.json from Nearmap API to YAML schema format
Handles different JSON structures
"""
import json
import yaml

# Load the API response
print("Loading classes.json...")
with open('classes.json', 'r', encoding='utf-8') as f:
    api_data = json.load(f)

print(f"JSON type: {type(api_data)}")

# Handle different possible JSON structures
ai_classes = []

# Try to find the classes data
if isinstance(api_data, dict):
    if 'classes' in api_data:
        classes_list = api_data['classes']
    elif 'features' in api_data:
        classes_list = api_data['features']
    elif 'data' in api_data:
        classes_list = api_data['data']
    else:
        print("Available keys:", list(api_data.keys()))
        print("\nPlease tell me which key contains the classes")
        exit(1)
elif isinstance(api_data, list):
    classes_list = api_data
else:
    print("Error: Unexpected JSON format")
    exit(1)

print(f"Found {len(classes_list)} items")

# Process each class
for idx, cls in enumerate(classes_list):
    try:
        # Try different possible field names
        name = cls.get('name') or cls.get('className') or cls.get('class_name') or cls.get('label') or f"Unknown_{idx}"
        class_id = cls.get('id') or cls.get('classId') or cls.get('class_id') or str(idx)
        description = cls.get('description') or cls.get('desc') or f"AI-detected {name}"
        
        layer = {
            'id': name.lower().replace(' ', '_').replace('/', '_').replace('-', '_'),
            'class_id': str(class_id),
            'name': name,
            'description': description,
            'pack': cls.get('pack') or cls.get('packName') or 'unknown',
            'help_url': f"https://help.nearmap.com/kb/articles/{class_id}-{name.lower().replace(' ', '-').replace('/', '-')}",
            'attributes': cls.get('attributes') or ['area_sqm', 'confidence'],
            'available_in': ['ai_features_api'],
            'tags': cls.get('tags') or []
        }
        ai_classes.append(layer)
        print(f"  ✓ {idx+1}. {name} (ID: {class_id})")
        
    except Exception as e:
        print(f"  ✗ Error processing item {idx}: {e}")
        print(f"     Item data: {cls}")
        continue

print(f"\n✓ Successfully processed {len(ai_classes)} classes")

# Load existing schema
print("\nLoading existing ai-features-schema.yaml...")
try:
    with open('ai-features-schema.yaml', 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)
except FileNotFoundError:
    print("Warning: Creating new schema from scratch")
    schema = {
        'version': '1.0',
        'last_updated': '2024-12-01',
        'systems': {
            'ai_features_api': {
                'name': 'AI Features API',
                'description': 'Retrieve geospatial AI features',
                'endpoint_base': 'https://api.nearmap.com/ai/features/v4'
            }
        },
        'ai_packs': []
    }

# Update with new classes
schema['ai_classes'] = ai_classes

# Write updated schema
output_file = 'ai-features-schema-updated.yaml'
print(f"\nWriting to {output_file}...")
with open(output_file, 'w', encoding='utf-8') as f:
    yaml.dump(schema, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

print(f"\n✓ SUCCESS! Created {output_file}")
print(f"✓ Total classes: {len(ai_classes)}")
print("\nNext steps:")
print("1. Review ai-features-schema-updated.yaml")
print("2. If it looks good:")
print("   rename ai-features-schema.yaml ai-features-schema-backup.yaml")
print("   rename ai-features-schema-updated.yaml ai-features-schema.yaml")
print("3. Run: py bundle-ai-features.py")