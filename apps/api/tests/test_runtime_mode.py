import os
from unittest.mock import patch
from app.runtime_mode import RuntimeMode
from app.services.environment_action_mode_service import EnvironmentActionModeService

def test_runtime_mode_detection():
    # Explicit env variable override
    with patch.dict(os.environ, {"RUNTIME_MODE": "LIVE_ASYNC"}):
        assert EnvironmentActionModeService.get_runtime_mode() == RuntimeMode.LIVE_ASYNC

    # Default fallback when empty
    with patch.dict(os.environ, {"RUNTIME_MODE": ""}):
        mode = EnvironmentActionModeService.get_runtime_mode()
        assert mode in (RuntimeMode.LOCAL_SYNC, RuntimeMode.LIVE_SYNC)
