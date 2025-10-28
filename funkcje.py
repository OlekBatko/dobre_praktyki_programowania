import string

def is_palindrome(text: str) -> bool:
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]

def fibonacci(n: int) -> int:
    if n < 0:
        raise ValueError("Błąd logiczny")

    if n == 0:
        return 0
    if n == 1:
        return 1

    a,b = 0,1
    for _ in range(2, n+1):
        a, b = b, a+b

    return b

def count_vowels(text: str) -> int:
    count = 0
    to_lower = text.lower()
    for letter in to_lower:
        if letter in ["a", "e", "i", "o", "u", "y", "ó", "ą", "ę"]:
            count+=1
    return count

def calculate_discount(price: float, discount: float) -> float:
    if discount < 0 or discount > 1:
        raise ValueError("Wartość spoza zakresu")
    return price - (price*discount)

def flatten_list(nested_list: list) -> list:
    flat = []

    for element in nested_list:
        if isinstance(element, list):
            flat.extend(flatten_list(element))
        else:
            flat.append(element)

    return flat

def word_frequencies(text: str) -> dict:
    text = text.lower()

    for char in string.punctuation:
        text = text.replace(char, "")

    words = text.split()
    frequencies = {}

    for word in words:
        frequencies[word] = frequencies.get(word, 0) + 1

    return frequencies

def is_prime(n: int) -> bool:
    if n < 2:
        return False

    if n in (2, 3):
        return True

    if n % 2 == 0:
        return False

    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False

    return True
