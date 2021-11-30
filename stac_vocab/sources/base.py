# encoding: utf-8
"""

"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'

from abc import ABC, ABCMeta, abstractmethod


class BaseWorkflow(metaclass=ABCMeta):
    """ Base class for an executor """

    def __init__(self, **kwargs):
        """ Constructor """
        pass

    @abstractmethod
    def run(self, command: str) -> (dict):
        """ Abstract method to run a command """
        pass
