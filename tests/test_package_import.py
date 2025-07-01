"""Test basic package imports"""

import pytest


def test_package_import():
    """Test that the main package can be imported"""
    import s3compat
    assert s3compat.__version__ == '1.0.0'


def test_osf_addon_import():
    """Test that OSF addon can be imported"""
    from s3compat.osf_addon import S3CompatConfig
    assert S3CompatConfig is not None


def test_waterbutler_provider_import():
    """Test that Waterbutler provider can be imported"""
    from s3compat.waterbutler_provider import S3CompatProvider
    assert S3CompatProvider is not None


def test_addon_config_entry_point():
    """Test addon configuration entry point"""
    from s3compat.osf_addon import get_addon_config
    config = get_addon_config()
    
    assert config['package'] == 's3compat.osf_addon'
    assert config['config_class'] == 'S3CompatConfig'
    assert config['name'] == 's3compat'


if __name__ == '__main__':
    pytest.main([__file__])