"""S3 Compatible Storage for RDM

This package provides S3 compatible storage integration for RDM systems,
including both OSF addon and Waterbutler provider components.
"""

__version__ = '1.0.0'
__author__ = 'NII RDM Team'

from . import osf_addon
from . import waterbutler_provider

__all__ = ['osf_addon', 'waterbutler_provider']