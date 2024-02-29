from Schedule import Schedule

class Calendar:
    def __init__(self):
        self.employees = dict(zip([]))
        self.schedule = []

    def addEmployee(self, employeeID, employeeName):
        self.employees[employeeID] = employeeName

    def addSchedule(self, scheduleItem):
        if scheduleItem.employeeID not in self.employees:
            print("idiot")
            return None

        self.schedule.append(scheduleItem)
        self.schedule.sort()        

    def print(self):
        for scheduleItem in self.schedule:
            print(self.employees[scheduleItem.employeeID])

if __name__ == "__main__":
    calendar = Calendar()
    calendar.addEmployee(12, "John")
    calendar.addEmployee(5, "James")

    john = Schedule(3, 2, 6, False)
    john.setEmployee(12)
    
    james = Schedule(5, 3, 9, False)
    
    john2 = Schedule(12, 7, 9, False)

    calendar.addSchedule(john)
    calendar.addSchedule(james)
    calendar.addSchedule(john2)

    calendar.print()