from datetime import datetime
from typing import Dict, Optional, List


class DirtyMap:
    """
    A simple store which manages keys and a corresponding dirty flag allowing to retrieve keys
    that have been dirty for a certain amount of time.
    """

    map: Dict[str, Optional[datetime]] = {}

    def dirty(self, key: str):
        self.map[key] = datetime.now()

    def clear(self, key: str):
        self.map[key] = None

    def get_dirtied(self) -> List[str]:
        return sorted([key for key, value in self.map.items() if value is not None])

    def get_clean(self) -> List[str]:
        return sorted([key for key, value in self.map.items() if value is None])

    @staticmethod
    def _is_outdated(maxdelay: int, now: datetime, value: Optional[datetime]) -> bool:
        if value is None:
            return False
        difference = now - value
        return difference.total_seconds() > maxdelay

    def get_outdated(self, maxdelay: int) -> List[str]:
        now = datetime.now()
        return sorted([key for key, value in self.map.items() if DirtyMap._is_outdated(maxdelay, now, value)])
