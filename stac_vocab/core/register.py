# encoding: utf-8
"""
Code snippet taken from: https://medium.com/@geoffreykoh/implementing-the-factory-pattern-via-dynamic-registry-and-python-decorators-479fc1537bbe
"""
__author__ = 'Richard Smith'
__date__ = '17 Nov 2021'
__copyright__ = 'Copyright 2018 United Kingdom Research and Innovation'
__license__ = 'BSD - see LICENSE file in top-level package directory'
__contact__ = 'richard.d.smith@stfc.ac.uk'


class WorkflowFactory:
    """ The factory class for creating workflows"""

    registry = {}
    """ Internal registry for available workflows """

    @classmethod
    def register(cls, name: str) -> Callable:
        """ Class method to register workflow class to the internal registry.
        Args:
            name (str): The name of the workflow.
        Returns:
            The workflow class itself.
        """

        def inner_wrapper(wrapped_class: workflowBase) -> Callable:
            if name in cls.registry:
                logger.warning('workflow %s already exists. Will replace it', name)
            cls.registry[name] = wrapped_class
            return wrapped_class

        return inner_wrapper

    # end register()

    @classmethod
    def create_workflow(cls, name: str, **kwargs) -> 'workflowBase':
        """ Factory command to create the workflow.
        This method gets the appropriate workflow class from the registry
        and creates an instance of it, while passing in the parameters
        given in ``kwargs``.
        Args:
            name (str): The name of the workflow to create.
        Returns:
            An instance of the workflow that is created.
        """

        if name not in cls.registry:
            logger.warning('workflow %s does not exist in the registry', name)
            return None

        exec_class = cls.registry[name]
        workflow = exec_class(**kwargs)
        return workflow
