from contextlib import AbstractContextManager
from typing import Callable

import pytest

from sqlalchemy.orm import Session
from app.services.growth_stage import GrowthStageService


def test_get_raises_lookup_error_when_id_does_not_exist(
    open_session: Callable[[], AbstractContextManager[Session]],
) -> None:
    # Arrange
    with open_session() as session:
        service = GrowthStageService(session)

        # Act + Assert: fehlende Id muss LookupError auslösen
        with pytest.raises(LookupError):
            service.get(999999)
