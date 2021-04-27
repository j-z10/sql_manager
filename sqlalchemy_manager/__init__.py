import os
import json

from sqlalchemy_manager.core.model import DynamicModel
from sqlalchemy_manager.core.manager import Manager


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
version_info = json.load(open(os.path.join(BASE_DIR, 'version', 'version.json')))
__version__ = version_info['version']
