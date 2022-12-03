def main():
    def inner():
        print('Inner')
        return x

    x = 10
    test = inner
    return test


print(main()())
