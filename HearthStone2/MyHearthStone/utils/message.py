#! /usr/bin/python
# -*- coding: utf-8 -*-

"""Utilities for output message."""

import os as _os
import logging as _logging
from time import time as _time
from functools import partial as _partial, wraps as _wraps
from contextlib import contextmanager as _cm

from ..utils.constants import UserLogPath, C

__author__ = 'fyabc'

# Debug levels.
LEVEL_DEBUG = _logging.DEBUG
LEVEL_VERBOSE = 15
LEVEL_INFO = _logging.INFO
LEVEL_WARNING = _logging.WARNING
LEVEL_ERROR = _logging.ERROR
LEVEL_CRITICAL = _logging.CRITICAL


def _get_handler(level=_logging.INFO, file=None, fmt=None, datefmt=None):
    if file is None:
        handler = _logging.StreamHandler()
    else:
        handler = _logging.FileHandler(file, encoding='utf-8')
    handler.setFormatter(_logging.Formatter(fmt=fmt, datefmt=datefmt, style='{'))
    handler.setLevel(level)

    return handler


def setup_logging(file='log.txt', level=_logging.INFO, scr_log=False, scr_level=_logging.DEBUG):
    """Setup logging. This function will setup some loggers and print some initial message.

    :param file: (str or None) ['log.txt']
        Logging filename. If set to None, do not create file logger.
    :param level: [logging.INFO] Message level of file logger.
    :param scr_log: (bool) [False]
        Open screen logger.
    :param scr_level: [logging.DEBUG] Message level of screen logger.
    """
    _logging.addLevelName(15, 'VERBOSE')
    _logging.addLevelName(25, 'NOTE')
    _logging.addLevelName(25, 'COMMON')

    # Clear old handlers. Useful for multiprocessing (call this in a new process).
    for old_handler in _logging.root.handlers[:]:
        _logging.root.removeHandler(old_handler)

    handlers = []
    if file is not None:
        handlers.append(
            _get_handler(level=level, file=_os.path.join(UserLogPath, file),
                         fmt='[{levelname:<8}] {asctime}.{msecs:0>3.0f}: <{pathname}:{lineno}> {message}',
                         datefmt='%Y-%m-%d %H:%M:%S'))
    if scr_log:
        handlers.append(
            _get_handler(level=scr_level, file=None, fmt='[{levelname:<8}] <{filename}:{lineno}> {message}'))
    _logging.basicConfig(level=_logging.DEBUG, handlers=handlers)

    info('Start the app')
    info('Process ID: {}'.format(_os.getpid()))
    info('App config: {}'.format(C.to_dict()))


message = _logging.log
debug = _logging.debug
verbose = _partial(message, LEVEL_VERBOSE)
info = _logging.info
warning = _logging.warning
error = _logging.error
critical = _logging.critical


@_cm
def msg_block(msg, level=LEVEL_INFO, log_time=True):
    if log_time:
        start_time = _time()
    message(level, '{}... '.format(msg))
    yield
    # noinspection PyUnboundLocalVariable
    message(level, '{} done{}.'.format(msg, ', time: {:.4f}s'.format(_time() - start_time) if log_time else ''))


def msg_time(func, level=LEVEL_INFO):
    @_wraps(func)
    def wrapper(*args, **kwargs):
        start_time = _time()
        result = func(*args, **kwargs)
        message(level, 'Function "{}" time: {:.4f}s'.format(func.__name__, _time() - start_time))
        return result
    return wrapper


def entity_message(self, kwargs, prefix='', __show_cls=True):
    return '{}{}({})'.format(
        prefix,
        self.__class__.__name__ if __show_cls else '',
        ', '.join(
            '{}={}'.format(k, v)
            for k, v in kwargs.items()
        )
    )
