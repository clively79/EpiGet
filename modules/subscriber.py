class Subscriber:
    """An abstract class allowing Publisher classes a unified method for notifying subscribers of state changes 
    """
    def notify(self):
        """An abstract method to be implemented by the child class
        """
        pass
