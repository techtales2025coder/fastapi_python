def full_name(first_name:str, second_name:str):
    full_name = first_name.title() + " " + second_name.title()

    return full_name

final_name: str = full_name("hello", "world")
print(final_name)