"""Admin integration utilities for S3 Compatible Storage

This module provides utilities for integration with RDM admin functionality,
including connection testing and storage validation.
"""

import logging
from . import utils

logger = logging.getLogger(__name__)


def test_s3compat_connection(endpoint_url, access_key, secret_key, bucket_name=None):
    """
    Test S3 compatible storage connection for admin interface
    
    Args:
        endpoint_url (str): S3 compatible storage endpoint URL
        access_key (str): Access key for authentication
        secret_key (str): Secret key for authentication  
        bucket_name (str, optional): Bucket name to test access
        
    Returns:
        dict: Test result with status and message
            {
                'success': bool,
                'message': str,
                'user_info': dict or None,
                'can_list': bool,
                'bucket_exists': bool or None
            }
    """
    try:
        # Create temporary external account for testing
        from osf.models import ExternalAccount
        temp_account = ExternalAccount(
            oauth_key=access_key,
            oauth_secret=secret_key,
            provider_name='s3compat'
        )
        
        # Test user info retrieval
        user_info = utils.get_user_info(temp_account, endpoint_url)
        if not user_info:
            return {
                'success': False,
                'message': 'Invalid credentials or unable to connect to storage service',
                'user_info': None,
                'can_list': False,
                'bucket_exists': None
            }
        
        # Test bucket listing capability
        can_list = utils.can_list(temp_account, endpoint_url)
        
        # Test specific bucket if provided
        bucket_exists = None
        if bucket_name:
            try:
                bucket_exists = utils.bucket_exists(temp_account, endpoint_url, bucket_name)
            except Exception as e:
                logger.warning(f"Error checking bucket existence: {e}")
                bucket_exists = False
        
        # Determine overall success
        success = True
        message = 'Connection successful'
        
        if not can_list:
            message = 'Connection successful but unable to list buckets. Check permissions.'
            
        if bucket_name and not bucket_exists:
            success = False
            message = f'Bucket "{bucket_name}" does not exist or is not accessible'
        
        return {
            'success': success,
            'message': message,
            'user_info': {
                'id': getattr(user_info, 'id', None),
                'display_name': getattr(user_info, 'display_name', None)
            } if user_info else None,
            'can_list': can_list,
            'bucket_exists': bucket_exists
        }
        
    except Exception as e:
        logger.error(f"S3 compatible storage connection test failed: {e}")
        return {
            'success': False,
            'message': f'Connection failed: {str(e)}',
            'user_info': None,
            'can_list': False,
            'bucket_exists': None
        }


def get_template_path(template_name):
    """
    Get template path for s3compat admin templates
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: Absolute path to template file or None if not found
    """
    import os
    
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    template_mapping = {
        's3compat_modal.html': 'rdm_custom_storage_location/providers/s3compat_modal.html'
    }
    
    if template_name in template_mapping:
        template_path = os.path.join(template_dir, template_mapping[template_name])
        if os.path.exists(template_path):
            return template_path
    
    return None


def get_template_content(template_name):
    """
    Get template content as string
    
    Args:
        template_name (str): Name of the template
        
    Returns:
        str: Template content or None if not found
    """
    template_path = get_template_path(template_name)
    if template_path:
        try:
            with open(template_path, 'r', encoding='utf-8') as f:
                return f.read()
        except IOError:
            logger.error(f"Failed to read template: {template_path}")
    
    return None


def get_admin_integration_info():
    """
    Get information about admin integration capabilities
    
    Returns:
        dict: Integration capabilities and function mappings
    """
    import os
    
    # Get template directory path
    template_dir = os.path.join(os.path.dirname(__file__), 'templates')
    
    return {
        'provider_name': 's3compat',
        'display_name': 'S3 Compatible Storage',
        'test_connection_func': test_s3compat_connection,
        'supported_operations': [
            'test_connection',
            'validate_credentials', 
            'check_bucket_access',
            'list_buckets'
        ],
        'required_credentials': ['endpoint_url', 'access_key', 'secret_key'],
        'optional_parameters': ['bucket_name'],
        'templates': {
            'modal': {
                'name': 's3compat_modal.html',
                'path': 'rdm_custom_storage_location/providers/s3compat_modal.html',
                'get_content': lambda: get_template_content('s3compat_modal.html'),
                'get_path': lambda: get_template_path('s3compat_modal.html')
            }
        },
        'template_dir': template_dir,
        'template_functions': {
            'get_template_path': get_template_path,
            'get_template_content': get_template_content
        }
    }