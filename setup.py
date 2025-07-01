#!/usr/bin/env python
"""Setup script for S3 Compatible Storage package."""

from setuptools import setup, find_packages
import os

# Read long description from README
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), 'README.md')
    if os.path.exists(readme_path):
        with open(readme_path, 'r', encoding='utf-8') as f:
            return f.read()
    return 'S3 Compatible Storage for RDM'

# Read version from package
def read_version():
    version_file = os.path.join('s3compat', '__init__.py')
    with open(version_file, 'r', encoding='utf-8') as f:
        for line in f:
            if line.startswith('__version__'):
                return line.split('=')[1].strip().strip('"').strip("'")
    return '1.0.0'

setup(
    name='s3compat',
    version=read_version(),
    description='S3 Compatible Storage for RDM',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    author='NII RDM Team',
    author_email='nii-rdm@nii.ac.jp',
    url='https://github.com/nii-rdm/RDM-storage-s3compat',
    
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    
    install_requires=[
        'boto==2.38.0',
        'xmltodict>=0.12.0',
    ],
    
    extras_require={
        'osf': [
            # Note: Django and Flask are provided by RDM-osf.io environment
            'Babel>=2.5.1',  # For i18n support
            'Mako>=1.0',     # For template support
        ],
        'waterbutler': [
            'aiohttp>=3.8',
            'tornado>=6.0',
        ],
        'dev': [
            'pytest>=6.0',
            'pytest-asyncio>=0.18',
            'aiohttpretty>=0.1.1',  # For waterbutler integration tests
            'pytest-cov>=2.10',
            'flake8>=3.8',
            'black>=21.0',
            'Babel>=2.5.1',  # For i18n development
        ],
        'test': [
            'pytest>=6.0',
            'pytest-asyncio>=0.18',
            'pytest-cov>=2.10',
            'mock>=4.0',
        ],
    },
    
    python_requires='>=3.6',
    
    entry_points={
        'waterbutler.providers': [
            's3compat = s3compat.waterbutler_provider:S3CompatProvider',
        ],
        'rdm.admin_integrations': [
            's3compat = s3compat.osf_addon.admin_integration:get_admin_integration_info',
        ],
    },
    
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Scientific/Engineering',
        'Topic :: System :: Archiving',
    ],
    
    keywords='rdm osf waterbutler s3 storage research-data',
)