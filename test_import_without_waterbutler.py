#!/usr/bin/env python
"""Test script to verify s3compat can be imported without waterbutler dependencies"""

import sys
import traceback

def test_main_package_import():
    """Test that the main s3compat package can be imported"""
    print("Testing s3compat package import...")
    try:
        import s3compat
        print(f"✓ Successfully imported s3compat (version: {s3compat.__version__})")
        return True
    except Exception as e:
        print(f"✗ Failed to import s3compat: {e}")
        traceback.print_exc()
        return False

def test_osf_addon_lazy_loading():
    """Test that the OSF addon uses lazy loading"""
    print("\nTesting s3compat.osf_addon lazy loading...")
    try:
        import s3compat
        
        # Check that osf_addon is in __all__
        if 'osf_addon' in s3compat.__all__:
            print("✓ osf_addon is in s3compat.__all__")
        else:
            print("✗ osf_addon not in s3compat.__all__")
            return False
        
        # Check that osf_addon attribute exists but is lazy loader
        if hasattr(s3compat, 'osf_addon'):
            osf_addon = s3compat.osf_addon
            print(f"✓ osf_addon attribute exists (type: {type(osf_addon)})")
            
            # Check if it's our lazy loader
            if 'LazyModule' in str(type(osf_addon)):
                print("✓ osf_addon is using lazy loading")
            else:
                print(f"? osf_addon type: {type(osf_addon)}")
        else:
            print("✗ osf_addon attribute not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed osf_addon lazy loading test: {e}")
        traceback.print_exc()
        return False

def test_osf_addon_access_fails():
    """Test that accessing OSF addon components fails gracefully"""
    print("\nTesting osf_addon access without OSF dependencies...")
    try:
        import s3compat
        
        # Try to access something from osf_addon
        try:
            config_class = s3compat.osf_addon.S3CompatConfig
            print("✗ Unexpectedly succeeded in accessing S3CompatConfig without OSF")
            return False
        except ImportError as e:
            if "OSF framework dependencies" in str(e):
                print("✓ Got expected ImportError with helpful message")
                print(f"  Error message: {e}")
                return True
            else:
                print(f"✗ Got ImportError but with unexpected message: {e}")
                return False
        except Exception as e:
            print(f"✗ Got unexpected exception type: {type(e).__name__}: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Failed osf_addon access test: {e}")
        traceback.print_exc()
        return False

def test_waterbutler_provider_lazy_loading():
    """Test that waterbutler_provider is available but doesn't force imports"""
    print("\nTesting waterbutler_provider lazy loading...")
    try:
        import s3compat
        
        # Check that waterbutler_provider is in __all__
        if 'waterbutler_provider' in s3compat.__all__:
            print("✓ waterbutler_provider is in s3compat.__all__")
        else:
            print("✗ waterbutler_provider not in s3compat.__all__")
            return False
        
        # Check that waterbutler_provider attribute exists but is lazy loader
        if hasattr(s3compat, 'waterbutler_provider'):
            wb_provider = s3compat.waterbutler_provider
            print(f"✓ waterbutler_provider attribute exists (type: {type(wb_provider)})")
            
            # Check if it's our lazy loader
            if 'LazyModule' in str(type(wb_provider)):
                print("✓ waterbutler_provider is using lazy loading")
            else:
                print(f"? waterbutler_provider type: {type(wb_provider)}")
        else:
            print("✗ waterbutler_provider attribute not found")
            return False
        
        return True
    except Exception as e:
        print(f"✗ Failed waterbutler_provider lazy loading test: {e}")
        traceback.print_exc()
        return False

def test_waterbutler_provider_access_fails():
    """Test that accessing waterbutler_provider components fails gracefully"""
    print("\nTesting waterbutler_provider access without waterbutler...")
    try:
        import s3compat
        
        # Try to access something from waterbutler_provider
        try:
            provider_class = s3compat.waterbutler_provider.S3CompatProvider
            print("✗ Unexpectedly succeeded in accessing S3CompatProvider without waterbutler")
            return False
        except ImportError as e:
            if "waterbutler dependencies" in str(e):
                print("✓ Got expected ImportError with helpful message")
                print(f"  Error message: {e}")
                return True
            else:
                print(f"✗ Got ImportError but with unexpected message: {e}")
                return False
        except Exception as e:
            print(f"✗ Got unexpected exception type: {type(e).__name__}: {e}")
            return False
            
    except Exception as e:
        print(f"✗ Failed waterbutler_provider access test: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("Testing s3compat import without waterbutler dependencies")
    print("=" * 60)
    
    tests = [
        test_main_package_import,
        test_osf_addon_lazy_loading,
        test_osf_addon_access_fails,
        test_waterbutler_provider_lazy_loading,
        test_waterbutler_provider_access_fails,
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