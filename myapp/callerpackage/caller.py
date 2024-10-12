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

    from myapp.models import myenum as absolute_enum
    from ..models import myenum as relative_enum
    from models import myenum as modified_sys_path_enum

    print(absolute_enum)  # myapp.models.enum
    print(relative_enum)  # myapp.models.myenum
    print(modified_sys_path_enum)  # models.myenum

    print(
        "absolute_enum == relative_enum {}".format(
            (absolute_enum == relative_enum)
        )
    )

    print(
        "absolute_enum == modified_sys_path_enum: {}".format(
            (absolute_enum == modified_sys_path_enum)
        )
    )
