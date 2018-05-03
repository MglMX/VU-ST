from CarInsuranceRate import calculate_rate
import unittest

class StatementTest(unittest.TestCase):
    def test_unmarried_male_20(self):
        married = False
        gender = "male"
        age = 20

        self.assertEqual(calculate_rate(married,gender,age),2000) #Visits statement rate += 1500

    def test_married_female_55(self):
        married = True
        gender = "female"
        age = 55

        self.assertEqual(calculate_rate(married, gender, age), 200) #Visits statement rate -= 200 and rte -= 100


if __name__ == '__main__':
    unittest.main()
