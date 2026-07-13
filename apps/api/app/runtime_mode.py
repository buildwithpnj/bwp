from enum import Enum

class RuntimeMode(str, Enum):
    LOCAL_SYNC = "LOCAL_SYNC"
    LIVE_SYNC = "LIVE_SYNC"
    LIVE_ASYNC = "LIVE_ASYNC"
    HYBRID_SAFE = "HYBRID_SAFE"
