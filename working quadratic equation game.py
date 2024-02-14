import cmath

def solve_quadratic(a, b, c):
    print("You entered the equation {}x^2 + {}x + {} = 0".format(a, b, c))

    # calculating the discriminant
    d = (b**2) - (4*a*c)
    print("First, we calculate the discriminant (b^2 - 4ac): {}".format(d))

    # find two solutions
    sol1 = (-b-cmath.sqrt(d))/(2*a)
    sol2 = (-b+cmath.sqrt(d))/(2*a)

    print("Then, we find the two solutions using the quadratic formula:")
    print("(-b ± sqrt(d)) / (2a)")
    print("Solution 1 is: {}".format(sol1))
    print("Solution 2 is: {}".format(sol2))

    return sol1, sol2

def main():
    print("Welcome to the quadratic equation solver!")
    print("Please enter the coefficients for ax^2 + bx + c = 0")

    a = float(input("Enter a: "))
    b = float(input("Enter b: "))
    c = float(input("Enter c: "))

    solve_quadratic(a, b, c)

if __name__ == "__main__":
    main()
