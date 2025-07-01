#!/usr/bin/env python
"""Test script to verify entry points work correctly"""

import sys
import traceback

def test_entry_point_path():
    """Test that the entry point path is correct"""
    print("Testing entry point path...")
    try:
        # Test that the lazy loading works through the main package
        import s3compat
        
        # Try to access the provider class through lazy loading - this should fail gracefully
        try:
            provider_class = s3compat.waterbutler_provider.S3CompatProvider
            print("✗ Unexpectedly succeeded in accessing S3CompatProvider without waterbutler")
            return False
        except ImportError as e:
            if "waterbutler dependencies" in str(e):
                print("✓ Got expected ImportError when accessing provider class through lazy loading")
                print(f"  Error message: {e}")
                return True
            else:
                print(f"✗ Got ImportError but with unexpected message: {e}")
                return False
        except Exception as e:
            print(f"✗ Got unexpected exception: {type(e).__name__}: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test entry point path: {e}")
        traceback.print_exc()
        return False

def test_osf_admin_integration_entry_point():
    """Test that OSF admin integration entry point works"""
    print("\nTesting OSF admin integration entry point...")
    try:
        # Test that the lazy loading works through the main package
        import s3compat
        
        try:
            integration_info = s3compat.osf_addon.get_admin_integration_info()
            print("✗ Unexpectedly succeeded in accessing admin integration without OSF")
            return False
        except ImportError as e:
            if "OSF framework dependencies" in str(e):
                print("✓ Got expected ImportError when accessing admin integration through lazy loading")
                print(f"  Error message: {e}")
                return True
            else:
                print(f"✗ Got ImportError but with unexpected message: {e}")
                return False
        except Exception as e:
            print(f"✗ Got unexpected exception: {type(e).__name__}: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Failed to test admin integration: {e}")
        traceback.print_exc()
        return False

def test_setup_py_entry_points():
    """Test that setup.py entry points are still correct"""
    print("\nTesting setup.py entry points configuration...")
    try:
        # Read and check setup.py entry points
        setup_py_path = 'setup.py'
        
        with open(setup_py_path, 'r') as f:
            setup_content = f.read()
        
        # Check waterbutler provider entry point
        if "'s3compat = s3compat.waterbutler_provider:S3CompatProvider'" in setup_content:
            print("✓ Waterbutler provider entry point is correctly configured")
        else:
            print("✗ Waterbutler provider entry point not found or incorrect")
            return False
        
        # Check admin integration entry point
        if "'s3compat = s3compat.osf_addon.admin_integration:get_admin_integration_info'" in setup_content:
            print("✓ Admin integration entry point is correctly configured")
        else:
            print("✗ Admin integration entry point not found or incorrect")
            return False
        
        return True
        
    except Exception as e:
        print(f"✗ Failed to check setup.py entry points: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all entry point tests"""
    print("=" * 60)
    print("Testing entry points functionality")
    print("=" * 60)
    
    tests = [
        test_entry_point_path,
        test_osf_admin_integration_entry_point,
        test_setup_py_entry_points,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✓ All {total} tests passed!")
        return 0
    else:
        print(f"✗ {total - passed} out of {total} tests failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())