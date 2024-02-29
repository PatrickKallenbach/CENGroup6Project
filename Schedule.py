class Schedule:
    def __init__(self, employeeID, startDate, endDate, repeat):
        # NOTE: schedule item assumes proper start and end dates. Might screw things up if start and end dates are sent in incorrectly
        self.employeeID = employeeID
        self.startDate = startDate
        self.endDate = endDate
        self.repeat = repeat

    def setEmployee(self, newEmployeeID):
        self.employeeID = newEmployeeID

    def __lt__(self, other):
        return self.startDate < other.startDate

    def print(self):
        print(self.employeeID)

if __name__ == "__main__":
    john = Schedule(3, 2, 6, False)
    john.print()
    john.setEmployee(12)
    john.print()