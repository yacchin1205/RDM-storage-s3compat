#!/usr/bin/env python
"""Test script for s3compat template plugin system"""

import os
import sys

# Add s3compat to Python path
sys.path.insert(0, '/app/s3compat-package')

# Mock addons module since we're testing outside OSF environment
class MockAddonsModule:
    pass

sys.modules['addons'] = MockAddonsModule()
sys.modules['addons.osfstorage'] = MockAddonsModule()
sys.modules['addons.osfstorage.models'] = MockAddonsModule()

# Mock osf module
class MockOSFModule:
    class models:
        class ExternalAccount:
            def __init__(self, **kwargs):
                for k, v in kwargs.items():
                    setattr(self, k, v)

sys.modules['osf'] = MockOSFModule()
sys.modules['osf.models'] = MockOSFModule.models

# Test admin integration discovery
print("Testing s3compat admin integration...")

try:
    # Test entry point discovery
    from importlib.metadata import entry_points
    
    eps = entry_points()
    if hasattr(eps, 'select'):
        # Python 3.10+ style
        admin_integrations = eps.select(group='rdm.admin_integrations')
    else:
        # Python 3.8-3.9 style
        admin_integrations = eps.get('rdm.admin_integrations', [])
    
    print(f"Found {len(admin_integrations)} admin integrations:")
    for ep in admin_integrations:
        print(f"  - {ep.name}: {ep.value}")
        
        # Test loading the integration
        try:
            integration_func = ep.load()
            integration_info = integration_func()
            print(f"    Successfully loaded: {integration_info.get('display_name', 'Unknown')}")
            
            # Test template functions
            if 'template_functions' in integration_info:
                template_funcs = integration_info['template_functions']
                print(f"    Template functions: {list(template_funcs.keys())}")
                
                # Test getting template content
                get_content = template_funcs.get('get_template_content')
                if get_content:
                    content = get_content('s3compat_modal.html')
                    if content:
                        print(f"    Template content length: {len(content)} characters")
                        print(f"    Template preview: {content[:100]}...")
                    else:
                        print("    No template content found")
                        
        except Exception as e:
            print(f"    Failed to load integration: {e}")
            
except Exception as e:
    print(f"Error discovering integrations: {e}")

print("\nTesting template path...")
try:
    from s3compat.osf_addon.admin_integration import get_template_path, get_template_content
    
    template_path = get_template_path('s3compat_modal.html')
    print(f"Template path: {template_path}")
    
    if template_path and os.path.exists(template_path):
        print("Template file exists!")
        
        content = get_template_content('s3compat_modal.html')
        if content:
            print(f"Template content loaded: {len(content)} characters")
            print("Template content preview:")
            print(content[:300])
        else:
            print("Failed to load template content")
    else:
        print("Template file not found")
        
except Exception as e:
    print(f"Error testing template: {e}")

print("\nTest completed!")