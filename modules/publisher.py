class Publisher:
    """ An abstract class designed to be inherited by ojects who wish to maintain a set of subscribers
        to transmit state change information 
    """
    def __init__(self):
        """ctor
        """
        self.subscribers = set()

    def notifySubscribers(self, message):
        """notifies all subscribed objects inheriting the subscriber class

        Args:
            message (json): A JSON object containing instructions for subscribed objects
        """
        for member in self.subscribers:
            member.notify(message)

    def addSubscriber(self, member):
        """Instance method to allow a subscriber object to subscribe to the publisher object

        Args:
            member (Subscriber): an Object wishing to subscribe to a publisher object must inherit the Subscriber class
        """
        self.subscribers.add(member)

    def removeSubscriber(self, member):
        """Instance method to allow a subscriber object to unsubscribe from the publisher object

        Args:
            member (Subscriber): Member argument must be a subscriber class
        """
        self.subscribers.remove(member)