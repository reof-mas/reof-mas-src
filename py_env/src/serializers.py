"""
Artifact serializer for creamas.
"""

import pickle
from creamas import Artifact

def get_artifact_ser():
    return Artifact, pickle.dumps, pickle.loads