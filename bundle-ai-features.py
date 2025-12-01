#!/usr/bin/env python3
"""
Bundle ai-features-schema.yaml into AI-Features-Viewer.html
Creates a standalone AI-Features-Viewer-bundled.html file ready for deployment.
"""

# Read ai-features-schema.yaml as plain text
with open('ai-features-schema.yaml', 'r', encoding='utf-8') as f:
    schema_text = f.read()

# Escape backticks in the schema
schema_text = schema_text.replace('`', '\\`')

# Read AI-Features-Viewer.html template
with open('AI-Features-Viewer.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Find and replace the EMBEDDED_SCHEMA placeholder
bundled_html = html_content.replace(
    '''const EMBEDDED_SCHEMA = `
# Paste ai-features-schema.yaml content here
# Or use bundle script to embed automatically
`;''',
    f'const EMBEDDED_SCHEMA = `{schema_text}`;'
)

# Write bundled file
with open('AI-Features-Viewer-bundled.html', 'w', encoding='utf-8') as f:
    f.write(bundled_html)

print("✓ Created AI-Features-Viewer-bundled.html")
print("✓ This file contains the embedded AI Features schema")
print("\nNext steps:")
print("1. Test locally: open AI-Features-Viewer-bundled.html in browser")
print("2. Deploy to your hosting (GitHub Pages, S3, etc.)")
print("3. Embed in Vanilla Forums with iframe:")
print('   <iframe src="https://your-domain.com/AI-Features-Viewer-bundled.html" ')
print('           width="100%" height="800px" frameborder="0"></iframe>')
