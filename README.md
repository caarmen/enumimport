# Attempt to reproduce a problem with different imports of an enum

The project structure is:

```
myapp
 \------ models
 |        \-------------- myenum.py
 |
 \------ calleepackage
 |        \-------------- callee.py
 |
 \------ callerpackage
          \-------------- caller.py
```

The `myenum` module defines an enum, `MyEnum`:

```python
class MyEnum(enum.Enum):
    DOG = 0
    CAT = 1
```


The `callee` module defines a function which returns a `CAT` instance of `MyEnum`:

```python
def get_my_enum():
    return MyEnum["CAT"]
```

The `caller` module defines a function which calls the callee to get the `CAT` instance:

```python
def entry_point():
    value = get_my_enum()
    if value == MyEnum.CAT:
        print("got a cat")
    else:
        print("didn't get a cat")
```

To run the project:
`python -m myapp.callerpackage.caller`

We expect to see "got a cat" printed.

The goal of this project is to see if we always get the expected behavior, regardless of how we import the `MyEnum` class, from `caller` and from `callee` :
* We can use an absolute import: `from myapp.models.myenum import MyEnum`.
* We can use a relative import: `from ..models.myenum import MyEnum`


