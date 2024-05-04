def funcion1():
    funcion3()
    print("funcion1")


def funcion2():
    def funcion3():
        print("funcion3")

    funcion1()