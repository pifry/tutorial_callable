from periodic_runner import PeriodicRunner


"""Your definitions here"""


def my_callback(name=None):
    print("Hello", name)


if __name__ == "__main__":
    """Your code here"""
    x = PeriodicRunner(callback=my_callback, name="Peter")
    x.start()
