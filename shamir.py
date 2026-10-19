from secrets import randbelow


def split_secret(p, secret, n, t):
    """Создаёт n долей; для восстановления нужны любые t из них."""
    # Создаём f(x) = secret + a1*x + a2*x**2 + ... .
    # Коэффициенты a1, a2, ... выбираем случайно от 0 до p - 1.
    coefficients = [secret]
    for _ in range(t - 1):
        coefficients.append(randbelow(p))

    # Для участника с номером x вычисляем его долю y = f(x) по модулю p.
    shares = []
    for x in range(1, n + 1):
        y = 0
        for degree, coefficient in enumerate(coefficients):
            power = pow(x, degree, p)  # x в степени degree по модулю p.
            y = (y + coefficient * power) % p
        shares.append((x, y))

    return shares


def restore_secret(p, shares):
    """Находит секрет по не менее чем t парам (номер участника, доля)."""
    # Секрет равен f(0). По формуле Лагранжа это сумма долей y_i,
    # умноженных на L_i(0) = произведение (-x_j) / (x_i - x_j), j != i.
    secret = 0
    for x_i, y_i in shares:
        numerator = 1    # Числитель множителя L_i(0).
        denominator = 1  # Знаменатель этого множителя.

        for x_j, _ in shares:
            if x_i == x_j:
                continue
            numerator = (numerator * (-x_j)) % p
            denominator = (denominator * (x_i - x_j)) % p

        # Чтобы разделить по модулю p, умножаем на обратное число.
        # pow(denominator, -1, p) находит число, обратное к знаменателю.
        inverse_denominator = pow(denominator, -1, p)
        lagrange_coefficient = (numerator * inverse_denominator) % p
        secret = (secret + y_i * lagrange_coefficient) % p

    return secret


if __name__ == "__main__":
    p = 127
    secret = 123
    n = 5
    t = 3

    shares = split_secret(p, secret, n, t)
    selected_shares = shares[:t]  # Берём любые t долей, здесь первые t.
    restored_secret = restore_secret(p, selected_shares)

    print("Исходный секрет:", secret)
    print("Все доли:", shares)
    print("Доли для восстановления:", selected_shares)
    print("Восстановленный секрет:", restored_secret)
