from aiogram import Router, types

from . import start
from . import help
from . import auth
from . import profile
from . import query
from . import support

router = Router()

router.include_router(start.router)
router.include_router(help.router)
router.include_router(auth.router)
router.include_router(profile.router)
router.include_router(support.router)
router.include_router(query.router)
