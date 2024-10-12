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

    from myapp.models.myenum import MyEnum as AbsoluteEnum
    from ..models.myenum import MyEnum as RelativeToRootEnum
    from models.myenum import MyEnum as DifferentSysPathAbsoluteEnum

    print(AbsoluteEnum.__module__)  # myapp.models.enum
    print(RelativeToRootEnum.__module__)  # myapp.models.myenum
    print(DifferentSysPathAbsoluteEnum.__module__)  # models.myenum

    print(
        "AbsoluteEnum.__module__ == RelativeToRootEnum.__module__: {}".format(
            (AbsoluteEnum.__module__ == RelativeToRootEnum.__module__)
        )
    )

    print(
        "AbsoluteEnum.__module__ == DifferentSysPathAbsoluteEnum.__module__: {}".format(
            (AbsoluteEnum.__module__ == DifferentSysPathAbsoluteEnum.__module__)
        )
    )
