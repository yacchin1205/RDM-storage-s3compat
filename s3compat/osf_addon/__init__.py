"""OSF S3 Compatible Storage Addon

This module provides the OSF integration components for S3 compatible storage.
"""

from .apps import S3CompatConfig
from .admin_integration import get_admin_integration_info

__all__ = ['S3CompatConfig', 'get_admin_integration_info']

default_app_config = 's3compat.osf_addon.apps.S3CompatAddonAppConfig'