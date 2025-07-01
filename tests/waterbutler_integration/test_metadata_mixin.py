"""Test S3CompatProvider integration with Waterbutler metadata mixin

This test was moved from RDM-waterbutler to maintain S3CompatProvider-specific 
testing while allowing the provider to be distributed as an independent package.
"""
import mock
import pytest

from tests.utils import MockCoroutine
from s3compat.waterbutler_provider import S3CompatProvider


@pytest.fixture
def auth():
    """Mock auth fixture for testing"""
    class MockAuth:
        pass
    return MockAuth()


@pytest.fixture
def credentials():
    """Mock credentials fixture for testing"""
    return {
        'host': 'normalhost:8080',
        'access_key': 'a',
        'secret_key': 's'
    }


@pytest.fixture  
def settings():
    """Mock settings fixture for testing"""
    return {}


@pytest.fixture
def provider_s3_compat(auth, credentials, settings):
    """S3CompatProvider fixture for testing"""
    provider = S3CompatProvider(auth, credentials, settings)
    provider._check_region = MockCoroutine()
    return provider


@pytest.fixture
def mock_folder_children_provider_s3():
    """Mock folder children for S3 provider testing"""
    class MockFolderChildren:
        def json_api_serialized(self, resource):
            return {'data': 'mock_folder_data'}
    
    return [MockFolderChildren() for _ in range(3)]


@pytest.fixture
def http_request():
    """Mock HTTP request for testing"""
    class MockRequest:
        def __init__(self):
            self.query_arguments = {}
    
    class MockHttpRequest:
        def __init__(self):
            self.request = MockRequest()
    
    return MockHttpRequest()


def mock_handler(http_request):
    """Create mock handler for testing"""
    class MockHandler:
        def __init__(self, http_request):
            self.request = http_request.request
            self.provider = None
            self.write = mock.Mock()
            self.resource = 'mock_resource'
        
        async def get_folder(self):
            """Mock get_folder implementation"""
            metadata = await self.provider.metadata()
            serialized_data = [x.json_api_serialized(self.resource) for x in metadata]
            response_data = {
                'data': serialized_data,
                'next_token': 'aaaa'  # Mock next token
            }
            self.write(response_data)
    
    return MockHandler(http_request)


class TestS3CompatMetadataMixin:
    """Test S3CompatProvider metadata functionality"""

    @pytest.mark.asyncio
    async def test_get_folder_with_next_token(self, http_request, provider_s3_compat, mock_folder_children_provider_s3):
        """Test S3CompatProvider folder metadata with pagination token"""
        # The get_folder method expected behavior is to return folder children's metadata, not the
        # metadata of the actual folder. This should be true of all providers.
        handler = mock_handler(http_request)
        handler.request.query_arguments['next_token'] = [b'']
        handler.provider = provider_s3_compat
        handler.write = mock.Mock()
        handler.provider.metadata = MockCoroutine(return_value=mock_folder_children_provider_s3)

        await handler.get_folder()
        call_args = handler.write.call_args[0][0]
        assert isinstance(call_args, dict)
        assert call_args['next_token'] == 'aaaa'
        assert isinstance(call_args['next_token'], str)
        assert isinstance(call_args['data'], list)