"""S3 Compatible Storage for RDM

This package provides S3 compatible storage integration for RDM systems,
including both OSF addon and Waterbutler provider components.
"""

__version__ = '1.0.0'
__author__ = 'NII RDM Team'

# Lazy loading for both osf_addon and waterbutler_provider to avoid ImportError
# when their respective dependencies are not available
import sys
import importlib


def _import_osf_addon():
    """Lazy import function for osf_addon"""
    try:
        return importlib.import_module('s3compat.osf_addon')
    except ImportError as e:
        raise ImportError(
            f"osf_addon module requires OSF framework dependencies. "
            f"This module should only be imported within an OSF environment. "
            f"Original error: {e}"
        ) from e


def _import_waterbutler_provider():
    """Lazy import function for waterbutler_provider"""
    try:
        return importlib.import_module('s3compat.waterbutler_provider')
    except ImportError as e:
        raise ImportError(
            f"waterbutler_provider module requires waterbutler dependencies. "
            f"Install with: pip install s3compat[waterbutler]. "
            f"Original error: {e}"
        ) from e


class LazyModule:
    """Generic lazy module loader"""
    
    def __init__(self, import_func):
        self._import_func = import_func
        self._module = None
        self._loaded = False
    
    def __getattr__(self, name):
        if not self._loaded:
            self._module = self._import_func()
            self._loaded = True
        return getattr(self._module, name)


# Install the lazy loaders
osf_addon = LazyModule(_import_osf_addon)
waterbutler_provider = LazyModule(_import_waterbutler_provider)

__all__ = ['osf_addon', 'waterbutler_provider']