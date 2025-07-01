# S3 Compatible Storage for RDM

This package provides S3 compatible storage integration for Research Data Management (RDM) systems, including both OSF addon and Waterbutler provider components.

## Features

- Support for 16+ S3 compatible storage services
- Integration with OSF (Open Science Framework)
- Integration with Waterbutler file handling service  
- Server-side encryption support
- Multi-part upload for large files
- Japanese research institution support

## Installation

```bash
pip install s3compat
```

### For OSF Integration

```bash
pip install s3compat[osf]
```

### For Waterbutler Integration

```bash
pip install s3compat[waterbutler]
```

### For Development

```bash
pip install s3compat[dev]
```

## Supported S3 Compatible Services

- AWS S3
- MinIO
- Japanese research institutions:
  - Kanazawa University
  - Osaka University  
  - Tohoku University
  - Kyoto University
  - And many more...

## Configuration

### OSF Configuration

Add to your OSF settings:

```python
# settings/local.py or production configuration
INSTALLED_APPS += [
    's3compat.osf_addon',
]

# Ensure addons.json includes s3compat in available addons list
```

### Waterbutler Configuration

Waterbutler automatically discovers the provider through entry points. No additional configuration required - simply install the package.

## Development

### Running Tests

```bash
pytest tests/
```

### Code Style

```bash
black s3compat/
flake8 s3compat/
```

## License

Apache License 2.0

## Contributing

Please read the contributing guidelines before submitting pull requests.

## Support

For issues and questions, please use the GitHub issue tracker.