from django.conf import settings

CACHE_PREFIX = getattr(settings, 
                       'FLATBLOCKS_XTD_CACHE_PREFIX', 
                       'flatblocks_xtd')

AUTOCREATE_STATIC_BLOCKS = getattr(settings, 
                                   'FLATBLOCKS_XTD_AUTOCREATE_STATIC_BLOCKS', 
                                   False)
