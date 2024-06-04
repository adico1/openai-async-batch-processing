"""
Module: event_handler

Description:
This module defines the EventHandler class,
which provides a simple event handling mechanism.
The EventHandler allows for the registration of events
with associated callback functions and the triggering of
these events with specific data.
This facilitates communication between different parts
of an application by allowing functions to subscribe to
and react to specific events.

Classes:
  - EventHandler: Manages the registration and triggering of events.
"""


class EventHandler:
    """
    A class to handle event registration and triggering.

    The EventHandler class allows you to register events with specific callback
    functions and trigger these events with given data. This is useful for
    decoupling different parts of an application, enabling communication between
    components through events.

    Attributes:
        events (dict): A dictionary storing event names and
        their associated callback functions.
    """

    def __init__(self):
        """
        Initializes a new instance of the EventHandler class.
        """
        self.events = {}

    def register_event(self, event_name, callback):
        """
        Registers a callback function for a specific event.

        If the event does not already exist, it is created and the callback
        function is added to the list of callbacks for that event.

        Args:
            event_name (str): The name of the event to register.
            callback (function): The function to call when the event is triggered.
        """
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(callback)

    def trigger_event(self, event_name, data):
        """
        Triggers an event and calls all registered callback functions
        with the given data.

        If the event has registered callbacks, each callback function is called
        with the provided data.

        Args:
            event_name (str): The name of the event to trigger.
            data: The data to pass to the callback functions.
        """
        if event_name in self.events:
            for callback in self.events[event_name]:
                callback(data)
