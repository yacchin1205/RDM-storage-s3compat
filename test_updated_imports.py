#!/usr/bin/env python
"""Simple test runner for updated import functionality"""

import sys
import traceback

def test_package_import():
    """Test that the main package can be imported"""
    print("Testing main package import...")
    try:
        import s3compat
        assert s3compat.__version__ == '1.0.0'
        print("✓ Package imported successfully")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_lazy_loading_attributes():
    """Test that lazy loading attributes are available"""
    print("Testing lazy loading attributes...")
    try:
        import s3compat
        
        # Check that both attributes are available
        assert hasattr(s3compat, 'osf_addon')
        assert hasattr(s3compat, 'waterbutler_provider')
        
        # Check that they are in __all__
        assert 'osf_addon' in s3compat.__all__
        assert 'waterbutler_provider' in s3compat.__all__
        
        print("✓ Lazy loading attributes are available")
        return True
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_osf_addon_lazy_import():
    """Test that OSF addon uses lazy loading and fails gracefully"""
    print("Testing OSF addon lazy import...")
    try:
        import s3compat
        
        # Try to access OSF addon - should fail gracefully in test environment
        try:
            _ = s3compat.osf_addon.S3CompatConfig
            print("✗ Should have failed with ImportError")
            return False
        except ImportError as e:
            if "OSF framework dependencies" in str(e):
                print("✓ Failed gracefully with correct error message")
                return True
            else:
                print(f"✗ Wrong error message: {e}")
                return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def test_waterbutler_provider_lazy_import():
    """Test that Waterbutler provider uses lazy loading and fails gracefully"""
    print("Testing waterbutler provider lazy import...")
    try:
        import s3compat
        
        # Try to access waterbutler provider - should fail gracefully in test environment
        try:
            _ = s3compat.waterbutler_provider.S3CompatProvider
            print("✗ Should have failed with ImportError")
            return False
        except ImportError as e:
            if "waterbutler dependencies" in str(e):
                print("✓ Failed gracefully with correct error message")
                return True
            else:
                print(f"✗ Wrong error message: {e}")
                return False
    except Exception as e:
        print(f"✗ Failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing updated import functionality")
    print("=" * 60)
    
    tests = [
        test_package_import,
        test_lazy_loading_attributes,
        test_osf_addon_lazy_import,
        test_waterbutler_provider_lazy_import,
    ]
    
    results = []
    for test in tests:
        result = test()
        results.append(result)
        print()
    
    print("=" * 60)
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