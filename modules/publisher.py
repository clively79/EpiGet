class Publisher:
    def __init__(self):
        self.subscribers = set()

    def notifySubscribers(self, message):
        for member in self.subscribers:
            member.notify(message)

    def addSubscriber(self, member):
        self.subscribers.add(member)

    def removeSubscriber(self, member):
        self.subscribers.remove(member)
