RIGHT = 0
LEFT = 1


class Vertex:
    name = None
    deadline = None
    relativeDeadline = None
    flightTime = {}
    numOfVisits = None
    firstVisits = {}
    lastVisits = {}
    pivot = False

    def __init__(self, name, deadline, flight_times):
        self.name = name
        self.deadline = deadline
        self.relativeDeadline = deadline
        self.flightTimes = flight_times
        self.numOfVisits = 0
        self.firstVisits = {RIGHT: None, LEFT: None}
        self.lastVisits = {RIGHT: None, LEFT: None}
        self.pivot = False

    def set_pivot(self):
        self.pivot = True
        self.numOfVisits = 1
        self.firstVisits = {RIGHT: 0, LEFT: 0}
        self.lastVisits = {RIGHT: 0, LEFT: 0}


class Cycle:
    pivot = None
    route = {}
    routeTimes = {}

    def __init__(self, pivot):
        self.pivot = pivot
        self.route = {RIGHT: [pivot], LEFT: [pivot]}
        self.routeTimes = {RIGHT: [0], LEFT: [0]}

    def get_route_str(self):
        route_str = '{' + str(self.pivot.name) + '}'

        for i in range(1, len(self.route[RIGHT])):
            route_str += ' -> ' + str(self.route[RIGHT][i].name)

        for i in range(1, len(self.route[LEFT])):
            route_str = str(self.route[LEFT][i].name) + ' -> ' + route_str

        return route_str
