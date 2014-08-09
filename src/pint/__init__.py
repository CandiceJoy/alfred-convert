# -*- coding: utf-8 -*-
"""
    pint
    ~~~~

    Pint is Python module/package to define, operate and manipulate
    **physical quantities**: the product of a numerical value and a
    unit of measurement. It allows arithmetic operations between them
    and conversions from and to different units.

    :copyright: (c) 2012 by Hernan E. Grecco.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
import os
import pkg_resources
from .formatting import formatter
from .unit import UnitRegistry, DimensionalityError, UndefinedUnitError, LazyRegistry
from .util import pi_theorem, logger

from .context import Context


__version__ = "unknown"
# on any error just try to grab the version that is installed on the system
try:
    __version__ = pkg_resources.get_distribution('pint').version
except:             # pragma: no cover
    pass  # we seem to have a local copy without any repository control or installed without setuptools
          # so the reported version will be __unknown__


#: A Registry with the default units and constants.
_DEFAULT_REGISTRY = LazyRegistry()

#: Registry used for unpickling operations.
_APP_REGISTRY = _DEFAULT_REGISTRY


def _build_quantity(value, units):
    """Build Quantity using the Application registry.
    Used only for unpickling operations.
    """
    global _APP_REGISTRY
    return _APP_REGISTRY.Quantity(value, units)


def set_application_registry(registry):
    """Set the application registry which is used for unpickling operations.

    :param registry: a UnitRegistry instance.
    """
    assert isinstance(registry, UnitRegistry)
    global _APP_REGISTRY
    logger.debug('Changing app registry from %r to %r.', _APP_REGISTRY, registry)
    _APP_REGISTRY = registry


def _run_pyroma(data):   # pragma: no cover
    """Run pyroma (used to perform checks before releasing a new version).
    """
    import sys
    from zest.releaser.utils import ask
    if not ask("Run pyroma on the package before uploading?"):
        return
    try:
        from pyroma import run
        result = run(data['tagdir'])
        if result != 10:
            if not ask("Continue?"):
                sys.exit(1)
    except ImportError:
        if not ask("pyroma not available. Continue?"):
            sys.exit(1)


def test():
    """Run all tests.

    :return: a :class:`unittest.TestResult` object
    """
    from .testsuite import run
    return run()
