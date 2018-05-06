def calculate_rate(married, gender, age):
    rate = 500

    if not married and gender=="male" and age < 25:
        rate += 1500
    if married or gender=="female":
        rate -= 200
    if age >= 50 and age <= 60:
        rate -= 100

    return rate


married = False
gender = "female"
age = 55

print(calculate_rate(married,gender,age))