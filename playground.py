class Person():
    def __init__(self,name,salary) -> None:
        self.name = name
        self.salary = salary

    def get_salary(self):
        print(f"Salary of {self.name} is {self.salary}")


class Employee(Person):
    def __init__(self, name, salary) -> None:
        super().__init__(name, salary)

    def get_salary(self):
        print(f"Salary of employee {self.name} is {self.salary - 1000}")

class Manager(Person):
    def __init__(self, name, salary, employees) -> None:
        super().__init__(name, salary)
        self.employees = employees

    def get_salary(self):
        print(f"Salary of employee {self.name} is {self.salary + 1000}")

        
john = Employee("John", 2000)

mirko = Manager("Mirko", 3000, john)

for i in (john,mirko):
    i.get_salary()