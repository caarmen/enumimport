from myapp.models.myenum import MyEnum
from myapp.calleepackage.callee import get_my_enum


def entry_point():
    value = get_my_enum()
    if value == MyEnum.CAT:
        print("got a cat")
    else:
        print("didn't get a cat")


if __name__ == "__main__":
    entry_point()
