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


## Altering the `sys.path`.

See the documentation for [sys.path](https://docs.python.org/3/library/sys.html#sys.path).

By default, when running `python -m myapp.callerpackage.caller`, python looks in the current working directory when resolving absolute imports.

We add this line to the `myapp` (root package) `__init__.py`:
```python
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
```

This adds `myapp` to the module search path. This means that python will look for modules in absolute impots:
* In the current working directory from which we launch `python -m` (the `enumimport` folder -- the root folder of this project).
* In the `myapp` directory.

This means we have a few options when importing `myenum` from `callee` or `caller`:
```python
from myapp.models.myenum import MyEnum
from ..models.myenum import MyEnum
from models.myenum import MyEnum
```

The first two resolve to the same module object.
The third resolves to a different module object.

If we don't use consistent imports, we may end up printing "didn't get a cat".

If, for example:
* `callee` imports: `from myapp.models.myenum import MyEnum`
* `caller` imports: `from models.myenum import MyEnum`

We will see "didn't get a cat".

### What's being imported?

Here's what's actually imported, when `caller` or `callee` imports the `myenum` package, depending on the enum syntax used:

<table>
<tr><td>code</td><td>output</td></tr>
<tr>
<td>

```python
from myapp.models import myenum
print(myenum)
```

</td>
<td>

```
<module 'myapp.models.myenum' from '/path/to/enumimport/myapp/models/myenum.py'>
```

</td>
</tr>
<tr>
<td>

```python
from ..models import myenum
print(myenum)
```

</td>
<td>

```
<module 'myapp.models.myenum' from '/path/to/enumimport/myapp/models/myenum.py'>
```

</td>
</tr>
<tr>
<td>

```python
from models import myenum
print(myenum)
```

</td>
<td>

```
<module 'models.myenum' from '/path/to/enumimport/myapp/models/myenum.py'>
```

</td>
</tr>
</table>

### Compatible imports

Here are different variations of imports between the `caller` and `callee` modules, of the `MyEnum` class.

We see that if we take advantage of the modified `sys.path`, we must do it from both `caller` and `callee`, to import the same `myenum` module.

| caller import                            | callee import                            | output              |
| ---------------------------------------- | ---------------------------------------- | ------------------- |
| `from myapp.models.myenum import MyEnum` | `from myapp.models.myenum import MyEnum` | ✅ got a cat        |
| `from myapp.models.myenum import MyEnum` | `from ..models.myenum import MyEnum`     | ✅ got a cat        |
| `from models.myenum import MyEnum`       | `from models.myenum import MyEnum`       | ✅ got a cat        |
| `from myapp.models.myenum import MyEnum` | `from models.myenum import MyEnum`       | ❌ didn't get a cat |
| `from ..models.myenum import MyEnum`     | `from models.myenum import MyEnum`       | ❌ didn't get a cat |
