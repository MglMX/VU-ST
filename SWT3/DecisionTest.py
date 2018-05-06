from CarInsuranceRate import calculate_rate
import unittest

class DecisionTest(unittest.TestCase):
    def test_unmarried_male_20(self):
        married = False
        gender = "male"
        age = 20

        self.assertEqual(calculate_rate(married,gender,age),2000)
        '''
        if not married and gender=="male" and age < 25 TRUE
        if married or gender=="female": FALSE
        if age >= 50 and age <= 60: FALSE
        '''

    def test_married_female_55(self):
        married = True
        gender = "female"
        age = 55

        self.assertEqual(calculate_rate(married, gender, age), 200) #Visits statement rate -= 200 and rte -= 100
        '''
        if not married and gender=="male" and age < 25 FALSE
        if married or gender=="female": TRUE
        if age >= 50 and age <= 60: TRUE
        '''

if __name__ == '__main__':
    unittest.main()