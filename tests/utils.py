"""Test utilities for s3compat package

Utilities moved from waterbutler tests to support independent testing.
"""
import asyncio


class MockCoroutine:
    """Mock coroutine for testing async functions"""
    
    def __init__(self, return_value=None, side_effect=None):
        self.return_value = return_value
        self.side_effect = side_effect
        self.call_count = 0
        self.call_args_list = []
    
    def __call__(self, *args, **kwargs):
        self.call_count += 1
        self.call_args_list.append((args, kwargs))
        
        if self.side_effect:
            if isinstance(self.side_effect, Exception):
                raise self.side_effect
            elif callable(self.side_effect):
                return self.side_effect(*args, **kwargs)
            else:
                return self.side_effect
        
        async def mock_coro():
            return self.return_value
        
        return mock_coro()