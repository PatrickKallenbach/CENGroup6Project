from Shift import Shift

class Schedule:

  def __init__(self):
    self.days = {
        "Monday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Tuesday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Wednesday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Thursday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Friday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Saturday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
        "Sunday": {
            "Morning": Shift("Morning"),
            "Afternoon": Shift("Afternoon"),
            "Evening": Shift("Evening")
        },
    }
    self.shifts = {
        "Morning": "7:00 AM - 12:00 PM",
        "Afternoon": "12:00 PM - 5:00 PM",
        "Evening": "5:00 PM - 10:00 PM",
    }

  def add_employee_to_shift(self, day, shift_type, employee):
    if day in self.days and shift_type in self.days[day]:
      self.days[day][shift_type].add_employee(employee)

  def remove_employee_from_shift(self, day, shift_type, employee):
    if day in self.days and shift_type in self.days[day]:
      self.days[day][shift_type].remove_employee(employee)

  def print_schedule(self):
    for day, shifts in self.days.items():
      print(f"{day}:")
      for shift_type, shift in shifts.items():
        time = self.shifts[shift_type]
        print(
            f"  {shift_type} ({time}): {shift if shift.employees else 'No employees'}"
        )
