Callable explained
==================

1. Introduction

This tutorial will help you to understand the concept of using callable (or callback functions). Together we will
create a facility that will call our callable. Then we will play the role of user of our facility. User that has no any
knowledge about internals of our facility. User that want's to use it with minimal effort.
In files *.ready you'll find ready working example so treat it as a spoiler.

1. Let's say we have a dog

Let's say we have a python library called PeriodicRunner. The purpose of this library is to provide users with a way to
run something periodically. You'll find a scaffold of this library in [periodic_runner.py](src/periodic_runner.py).
PeriodicRunner needs to be implemented. In normal circumstances, user have no interest in PeriodicRunner internals. We
need to implement convenient interface for our user. User have to have a way to REGISTER his function and to START
process that will do the work (sometimes called worker). The PeriodicRunner needs to get function from user and call it
every period.

2. Let's code

In [user_code.py](src/user_code.py) we are user of PeriodicRunner library. First of all we have to define our callback
function:

```python
#user_code.py
"""Your definitions here"""
def my_callback():
    print("Hello world")
```

We can call this simple function and test if it works:

```python
#user_code.py
"""Your code here"""
my_callback()
```

The result should be, as expected, 'Hello world' in the console. We need some way to pass this function to
PeriodicRunner so it can run it periodically. User should be able to do this:

```python
#user_code.py
"""Your code here"""
runner = PeriodicRunner(callback=my_callback)
```

We're passing my_callback to PeriodicRunner se let's implement this on the PeriodicRunner side:

```python
#periodic_runner.py
class PeriodicRunner:

    def __init__(self, period=1.0, callback=None):
        self.period = period
        self.callback = callback
```

Now the PeriodicRunner can accept callback keyword argument and store it in self.callback variable. This is a function
hook. Besides storing hook, PeriodicRunner must call this hook periodically. Let's implement this:

```python
#periodic_runner.py
class PeriodicRunner:

    def __init__(self, period=1.0, callback=None):
        self.period = period
        self.callback = callback

    def start(self):
        while True:
            sleep(self.period)
            if self.callback:
                self.callback()
```

We defined a start method which runs an infinite loop. Inside this loop it's going to sleep for a period and then
calling function that is stored inside self.callback variable. The if statement ensures that no call will be done if
callback is not defined.
Now user have to start worker:

```python
#user_code.py
"""Your code here"""
runner = PeriodicRunner(callback=my_callback)
runner.start()
```

And you should see 'Hello world' in console every one second. We have basic functionality now. Our periodic runner
calls callback periodically. There is one problem however. Function my_callback is extremely simple. In real world user
will want to pass some argument to his callback. Let's define slightly more complicated callback:

```python
#user_code.py
"""Your definitions here"""
def my_callback(name):
    print("Hello" name)
```

Our user wants to pass name to his callback. It is clear that he must provide this variable during registration of the
hook.

```python
#user_code.py
"""Your code here"""
runner = PeriodicRunner("Peter", callback=my_callback)
runner.start()
```

We must modify PeriodicRunner to handle this:

```python
#periodic_runner.py
class PeriodicRunner:

    def __init__(self, arg, period=1.0, callback=None):
        self.period = period
        self.callback = callback
        self.arg = arg

    def start(self):
        while True:
            sleep(self.period)
            if self.callback:
                self.callback(self.arg)
```

Now our Periodic runner __init__ accept additional positional argument arg, store it inside self.arg variable. Then
worker calls callback and pass self.arg to it. Let's run this code. You should see 'Hello Peter' once every second.
Nice, but user may want to pass more arguments to his callback and we don't want to modify PeriodicRunner every time.
We can use keyword arguments for this. Let's start from modifying user callback:

```python
#user_code.py
"""Your definitions here"""
def my_callback(name=None):
    print("Hello" name)
```

Now user expects his callback to receive keyword argument name and uses it inside print function. He must pass this
keyword argument during registration of the callback:

```python
#user_code.py
"""Your code here"""
runner = PeriodicRunner(callback=my_callback, name="Peter")
runner.start()
```

Our PeriodicRunner must handle keywords arguments now:

```python
#periodic_runner.py
class PeriodicRunner:

    def __init__(self, period=1.0, callback=None, **kwargs):
        self.period = period
        self.callback = callback
        self.kwargs = kwargs

    def start(self):
        while True:
            sleep(self.period)
            if self.callback:
                self.callback(**self.kwargs)
```

PeriodicRunner __init__ now accept arbitrary number of keyword arguments (**kwargs). It doesn't know about specific
names of arguments just stores entire kwargs dictionary inside self.kwargs variable. Worker unpacks and pass every
argument from kwargs and pass it to callback.

4. Working example

```python
#user_code.py
from periodic_runner import PeriodicRunner


"""Your definitions here"""


def my_callback(name=None):
    print("Hello", name)


if __name__ == "__main__":
    """Your code here"""
    x = PeriodicRunner(callback=my_callback, name="Peter")
    x.start()
```

```python
#periodic_runner.py
from time import sleep


class PeriodicRunner:

    def __init__(self, period=1.0, callback=None, **kwargs):
        self.period = period
        self.callback = callback
        self.kwargs = kwargs

    def start(self):
        while True:
            sleep(self.period)
            if self.callback:
                self.callback(**self.kwargs)
```