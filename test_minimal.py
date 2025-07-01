#!/usr/bin/env python
"""Minimal test script for s3compat template plugin system without OSF dependencies"""

import os
import sys

# Add s3compat to Python path
sys.path.insert(0, '/app/s3compat-package')

print("Testing s3compat template functions without OSF dependencies...")

try:
    # Test template path functionality directly
    template_dir = '/app/s3compat-package/s3compat/osf_addon/templates'
    print(f"Template directory: {template_dir}")
    
    if os.path.exists(template_dir):
        print("Template directory exists!")
        
        # List template files
        for root, dirs, files in os.walk(template_dir):
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    rel_path = os.path.relpath(file_path, template_dir)
                    print(f"  Found template: {rel_path}")
                    
                    # Check file size
                    size = os.path.getsize(file_path)
                    print(f"    Size: {size} bytes")
                    
                    # Read first few lines
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            first_lines = f.read()[:200]
                            print(f"    Preview: {first_lines}...")
                    except Exception as e:
                        print(f"    Error reading file: {e}")
    else:
        print("Template directory not found")

    # Test template functions without OSF dependencies
    print("\nTesting basic template functions...")
    
    # Create a simple template function test
    def get_template_path_simple(template_name):
        template_dir = '/app/s3compat-package/s3compat/osf_addon/templates'
        template_mapping = {
            's3compat_modal.html': 'rdm_custom_storage_location/providers/s3compat_modal.html'
        }
        
        if template_name in template_mapping:
            template_path = os.path.join(template_dir, template_mapping[template_name])
            if os.path.exists(template_path):
                return template_path
        return None

    def get_template_content_simple(template_name):
        template_path = get_template_path_simple(template_name)
        if template_path:
            try:
                with open(template_path, 'r', encoding='utf-8') as f:
                    return f.read()
            except IOError:
                return None
        return None

    # Test the functions
    template_path = get_template_path_simple('s3compat_modal.html')
    print(f"Template path: {template_path}")
    
    if template_path:
        content = get_template_content_simple('s3compat_modal.html')
        if content:
            print(f"Template content loaded: {len(content)} characters")
            print("Template content preview:")
            print(content[:300])
            print("...")
            
            # Check for Django template tags
            if '{% load i18n %}' in content:
                print("✓ Django i18n tags found")
            if '{% trans ' in content:
                print("✓ Translation tags found")
            if 'modal' in content:
                print("✓ Modal content found")
            if 's3compat' in content:
                print("✓ S3 compatible content found")
        else:
            print("Failed to load template content")
    else:
        print("Template file not found")

except Exception as e:
    print(f"Error during testing: {e}")
    import traceback
    traceback.print_exc()

print("\nTest completed!")