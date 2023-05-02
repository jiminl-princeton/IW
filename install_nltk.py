# Sources:
# Kosuri, M. (2017). NLTK SSL Errors loading…. GitHub. https://github.com/gunthercox/ChatterBot/issues/930

import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download()