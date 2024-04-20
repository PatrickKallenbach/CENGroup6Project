class Shift:

  def __init__(self, shift_type):
    self.shift_type = shift_type
    self.employees = []

  def add_employee(self, employee):
    if employee not in self.employees:
      self.employees.append(employee)

  def remove_employee(self, employee):
    if employee in self.employees:
      self.employees.remove(employee)

  def __repr__(self):
    employee_names = ', '.join([emp.name for emp in self.employees])
    return f"{self.shift_type} Shift: [{employee_names}]"
