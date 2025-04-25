import math

class Comp:
    def __init__(self, real, img):
        self.real = real
        self.img = img

    def __add__(self, other):
        return Comp(self.real + other.real, self.img + other.img)

    def __sub__(self, other):
        return Comp(self.real - other.real, self.img - other.img)

    def __mul__(self, other):
        real_part = self.real * other.real - self.img * other.img
        img_part = self.real * other.img + self.img * other.real
        return Comp(real_part, img_part)

    def __truediv__(self, other):
        denom= other.real**2 + other.img**2
        if denom== 0:
            raise ZeroDivisionError("Cannot divide by zero")
        real_part = (self.real * other.real + self.img * other.img) / denom
        img_part = (self.img * other.real - self.real * other.img) / denom
        return Comp(real_part, img_part)

    def mod(self):
        return Comp(math.sqrt(self.real**2 + self.img**2), 0)

    def __str__(self):
        if self.img == 0:
            return f"{self.real:.2f}+0.00i"
        elif self.real == 0:
            return f"0.00{('+' if self.img >= 0 else '-')}{abs(self.img):.2f}i"
        else:
            return f"{self.real:.2f}{('+' if self.img >= 0 else '-')}{abs(self.img):.2f}i"

a, b = map(int, input().split())
c, d = map(int, input().split())

c1 = Comp(a, b)
c2 = Comp(c, d)

print(c1 + c2)
print(c1 - c2)
print(c1 * c2)
print(c1 / c2)
print(c1.mod())
print(c2.mod())
