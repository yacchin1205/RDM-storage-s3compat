"""Test admin integration functionality"""

import pytest
from unittest.mock import Mock, patch

from s3compat.osf_addon.admin_integration import (
    test_s3compat_connection,
    get_admin_integration_info
)


class TestAdminIntegration:
    """Test admin integration functions"""
    
    def test_get_admin_integration_info(self):
        """Test admin integration info retrieval"""
        info = get_admin_integration_info()
        
        assert info['provider_name'] == 's3compat'
        assert info['display_name'] == 'S3 Compatible Storage'
        assert 'test_connection_func' in info
        assert callable(info['test_connection_func'])
        assert 'test_connection' in info['supported_operations']
        assert 'endpoint_url' in info['required_credentials']
    
    @patch('s3compat.osf_addon.admin_integration.utils.get_user_info')
    @patch('s3compat.osf_addon.admin_integration.utils.can_list')
    @patch('s3compat.osf_addon.admin_integration.utils.bucket_exists')
    def test_test_s3compat_connection_success(self, mock_bucket_exists, mock_can_list, mock_get_user_info):
        """Test successful connection test"""
        # Mock successful responses
        mock_user = Mock()
        mock_user.id = 'test_user_id'
        mock_user.display_name = 'Test User'
        mock_get_user_info.return_value = mock_user
        mock_can_list.return_value = True
        mock_bucket_exists.return_value = True
        
        result = test_s3compat_connection(
            endpoint_url='https://s3.example.com',
            access_key='test_key',
            secret_key='test_secret',
            bucket_name='test_bucket'
        )
        
        assert result['success'] is True
        assert 'successful' in result['message'].lower()
        assert result['user_info']['id'] == 'test_user_id'
        assert result['user_info']['display_name'] == 'Test User'
        assert result['can_list'] is True
        assert result['bucket_exists'] is True
    
    @patch('s3compat.osf_addon.admin_integration.utils.get_user_info')
    def test_test_s3compat_connection_invalid_credentials(self, mock_get_user_info):
        """Test connection test with invalid credentials"""
        mock_get_user_info.return_value = None
        
        result = test_s3compat_connection(
            endpoint_url='https://s3.example.com',
            access_key='invalid_key',
            secret_key='invalid_secret'
        )
        
        assert result['success'] is False
        assert 'invalid credentials' in result['message'].lower()
        assert result['user_info'] is None
        assert result['can_list'] is False
    
    @patch('s3compat.osf_addon.admin_integration.utils.get_user_info')
    @patch('s3compat.osf_addon.admin_integration.utils.can_list')
    @patch('s3compat.osf_addon.admin_integration.utils.bucket_exists')
    def test_test_s3compat_connection_bucket_not_exists(self, mock_bucket_exists, mock_can_list, mock_get_user_info):
        """Test connection test with non-existent bucket"""
        mock_user = Mock()
        mock_user.id = 'test_user_id'
        mock_user.display_name = 'Test User'
        mock_get_user_info.return_value = mock_user
        mock_can_list.return_value = True
        mock_bucket_exists.return_value = False
        
        result = test_s3compat_connection(
            endpoint_url='https://s3.example.com',
            access_key='test_key',
            secret_key='test_secret',
            bucket_name='nonexistent_bucket'
        )
        
        assert result['success'] is False
        assert 'does not exist' in result['message']
        assert result['bucket_exists'] is False
    
    @patch('s3compat.osf_addon.admin_integration.utils.get_user_info')
    def test_test_s3compat_connection_exception(self, mock_get_user_info):
        """Test connection test with exception"""
        mock_get_user_info.side_effect = Exception('Connection error')
        
        result = test_s3compat_connection(
            endpoint_url='https://s3.example.com',
            access_key='test_key',
            secret_key='test_secret'
        )
        
        assert result['success'] is False
        assert 'failed' in result['message'].lower()


if __name__ == '__main__':
    pytest.main([__file__])