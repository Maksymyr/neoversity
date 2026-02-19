def caching_fibonacci():
    cache = {}

    def fibonacci(n):
        try:
            n = int(n)
        except (TypeError, ValueError):
            raise TypeError("n must be a number or convertible to int")

        if n <= 0:
            return 0

        if n == 1:
            return 1

        if n in cache:
            return cache[n]

        cache[n] = fibonacci(n - 1) + fibonacci(n - 2)
        return cache[n]

    return fibonacci
