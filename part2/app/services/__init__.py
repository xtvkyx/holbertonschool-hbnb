"""Services package init.

Expose a single shared facade instance for the whole app.
"""

from app.services.hbnb_facade import HBnBFacade

_facade = HBnBFacade()


def get_facade() -> HBnBFacade:
    """Return the shared facade instance."""
    return _facade
