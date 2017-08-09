"""
Helper for injection pattern
"""

from .service import provide, require, NoServiceError

__all__ = ['provide', 'require', 'NoServiceError']
