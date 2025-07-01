"""Test basic package imports with lazy loading"""

import pytest


def test_package_import():
    """Test that the main package can be imported"""
    import s3compat
    assert s3compat.__version__ == '1.0.0'


def test_lazy_loading_attributes():
    """Test that lazy loading attributes are available"""
    import s3compat
    
    # Check that both attributes are available
    assert hasattr(s3compat, 'osf_addon')
    assert hasattr(s3compat, 'waterbutler_provider')
    
    # Check that they are in __all__
    assert 'osf_addon' in s3compat.__all__
    assert 'waterbutler_provider' in s3compat.__all__


def test_osf_addon_lazy_import():
    """Test that OSF addon uses lazy loading and fails gracefully"""
    import s3compat
    
    # Try to access OSF addon - should fail gracefully in test environment
    with pytest.raises(ImportError, match="OSF framework dependencies"):
        _ = s3compat.osf_addon.S3CompatConfig


def test_waterbutler_provider_lazy_import():
    """Test that Waterbutler provider uses lazy loading and fails gracefully"""
    import s3compat
    
    # Try to access waterbutler provider - should fail gracefully in test environment
    with pytest.raises(ImportError, match="waterbutler dependencies"):
        _ = s3compat.waterbutler_provider.S3CompatProvider


@pytest.mark.skipif(
    True,  # Skip this test as it requires OSF dependencies
    reason="Requires OSF framework dependencies"
)
def test_osf_addon_import_with_dependencies():
    """Test that OSF addon can be imported when dependencies are available"""
    from s3compat.osf_addon import S3CompatConfig
    assert S3CompatConfig is not None


@pytest.mark.skipif(
    True,  # Skip this test as it requires waterbutler dependencies
    reason="Requires waterbutler dependencies"
)
def test_waterbutler_provider_import_with_dependencies():
    """Test that Waterbutler provider can be imported when dependencies are available"""
    from s3compat.waterbutler_provider import S3CompatProvider
    assert S3CompatProvider is not None


@pytest.mark.skipif(
    True,  # Skip this test as it requires OSF dependencies
    reason="Requires OSF framework dependencies"
)
def test_addon_config_entry_point_with_dependencies():
    """Test addon configuration entry point when dependencies are available"""
    from s3compat.osf_addon import get_addon_config
    config = get_addon_config()
    
    assert config['package'] == 's3compat.osf_addon'
    assert config['config_class'] == 'S3CompatConfig'
    assert config['name'] == 's3compat'


if __name__ == '__main__':
    pytest.main([__file__])