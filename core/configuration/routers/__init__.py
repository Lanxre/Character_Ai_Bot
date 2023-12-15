from core.internal.routers import telegram
from .router import Routes

__routers__ = Routes(routers=(
	telegram.router,
))
