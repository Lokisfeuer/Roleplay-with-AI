def main():
    def inner():
        print('Inner')
        return 10

    test = inner
    return test


print(main()())
