# Assumptions:
# 1. The cycle is always in clockwise direction.
#    Although in reality it does not matter, as
#    flight times are symmetrical; undirected graph.
#
# 2. Constraints for all vertices only need to be
#    checked once after the next vertex has been
#    computed; subsequently, check on violated
#    vertices only.

from classes import Vertex, Cycle

RIGHT = 0
LEFT = 1
file_name = '3.1'
iterations = 0
cycle = None
totalVertices = 0
vertices = None
pivot = None


def main():
    initialisation()
    simple_decision_check()
    violated = []
    is_solution_found = False
    global iterations

    print_legend()
    print('<< Procedure >>')

    while not is_solution_found:
        for direction in range(2):
            iterations += 1

            route_str = cycle.get_route_str()

            # Compute the next vertex to visit.
            if direction == RIGHT:
                nxt_vertex = get_nxt_right_vertex()
            else:
                nxt_vertex = get_nxt_left_vertex()

            # Check constraints for each vertex.
            for vertex in vertices:
                violated_vertex = check_constraints(vertex, nxt_vertex, direction)

                if violated_vertex is not None:
                    violated.append(violated_vertex)

            # Print procedure.
            violated_str = ''

            if violated:
                violated_str = ', '.join([str(vertex.name) for vertex in violated])

                if direction == RIGHT:
                    violated_str = ' | ' + violated_str
                else:
                    violated_str += ' | '

            if direction == RIGHT:
                print(route_str + ' ~> ' + str(nxt_vertex.name) + violated_str)
            else:
                print(violated_str + str(nxt_vertex.name) + ' ~> ' + route_str)

            while violated:
                # At least one violation occurs.

                nxt_vertex = handle_violations(violated, nxt_vertex, direction)
                temp_list = list(violated)
                del violated[:]  # reset list

                # Check constraints for each violated vertex.
                for vertex in temp_list:
                    violated_vertex = check_constraints(vertex, nxt_vertex, direction)

                    if violated_vertex is not None:
                        violated.append(violated_vertex)

                del temp_list  # remove list

            if nxt_vertex is not None:
                # Tree grows according to the current direction.

                cur_time_slot = len(cycle.route[direction]) - 1
                end_vertex = cycle.route[direction][cur_time_slot]
                flight_time = end_vertex.flightTimes[nxt_vertex.name]
                old_travel_time = cycle.routeTimes[direction][cur_time_slot]
                new_travel_time = old_travel_time + flight_time

                # Update cycle.route and routeTimes
                cycle.route[direction].append(nxt_vertex)
                cycle.routeTimes[direction].append(new_travel_time)

                # Update attributes of nxt_vertex.
                if nxt_vertex.firstVisits[direction] is not None:
                    nxt_vertex.lastVisits[direction] = new_travel_time
                else:
                    nxt_vertex.firstVisits[direction] = \
                        nxt_vertex.lastVisits[direction] = new_travel_time

                    nxt_vertex.numOfVisits += 1

            # Update relative deadlines of all vertices.
            update_relative_deadlines(nxt_vertex, direction)

            # Base case:
            if cycle.route[LEFT][len(cycle.route[LEFT]) - 1] == cycle.route[RIGHT][len(cycle.route[RIGHT]) - 1]:
                # A loop is formed.

                # Check if all vertices have been visited at least once.
                for vertex in vertices:
                    if vertex.numOfVisits < 1:
                        is_solution_found = False
                        break
                    else:
                        is_solution_found = True

                if is_solution_found:
                    print(cycle.get_route_str())
                    break

    print_solution()


def initialisation():
    global cycle, totalVertices, \
        vertices, pivot

    deadlines, flight_times = extract_data()
    totalVertices = len(deadlines)
    vertices = []

    for i in range(totalVertices):
        vertices.append(Vertex(i, deadlines[i], flight_times[i]))

    pivot = get_pivot()
    cycle = Cycle(pivot)  # construct Cycle object
    pivot.set_pivot()


def extract_data():
    ft = []

    with open(file_name, 'r') as file:
        data = [line.split() for line in file]

        # First line contains relative deadline of each vertex.
        rd = [int(i) for i in data[0]]

        total_vertices = len(data) - 1

        # Skip the first line in text file.
        for i in range(total_vertices):
            temp = {j: int(data[i + 1][j]) for j in range(total_vertices)}
            ft.append(temp)

        return rd, ft


def get_pivot():
    max_rd = -1

    for vertex in vertices:
        if vertex.deadline >= max_rd:
            max_rd = vertex.deadline
            __pivot = vertex

    return __pivot


def simple_decision_check():
    for vertex in vertices:
        for j in vertex.flightTimes.values():
            if j > 0.5 * vertex.deadline:
                return False  # no solution can be found

    return True  # possible solution can be found, but not guaranteed


def get_nxt_right_vertex():
    # 1. Least visited vertices.
    least_visited = []
    min_value = vertices[0].numOfVisits
    end_vertex = cycle.route[RIGHT][len(cycle.route[RIGHT]) - 1]

    for vertex in vertices:
        if vertex.numOfVisits < min_value:
            min_value = vertex.numOfVisits

    for vertex in vertices:
        if vertex != end_vertex and vertex.numOfVisits == min_value:
            least_visited.append(vertex)

    # 2. Shortest relative deadline.
    if len(least_visited) > 1:
        shortest_rd = []
        min_value = least_visited[0].relativeDeadline

        for i in range(1, len(least_visited)):
            nxt_vertex = least_visited[i]

            if nxt_vertex.relativeDeadline < min_value:
                min_value = nxt_vertex.relativeDeadline

        for vertex in least_visited:
            if vertex.relativeDeadline == min_value:
                shortest_rd.append(vertex)
    else:
        return least_visited[0]

    # 3. Shortest flight time.
    shortest_ft = shortest_rd[0]

    if len(shortest_rd) > 1:
        cur_vertex = cycle.route[RIGHT][len(cycle.route[RIGHT]) - 1]
        min_value = cur_vertex.flightTimes[shortest_rd[0].name]

        for i in range(1, len(shortest_rd)):
            nxt_vertex = shortest_rd[i]

            if cur_vertex.flightTimes[nxt_vertex.name] <= min_value:
                min_value = cur_vertex.flightTimes[nxt_vertex.name]
                shortest_ft = nxt_vertex

    return shortest_ft


def get_nxt_left_vertex():
    # 1. Unvisited vertices.
    unvisited = []

    for vertex in vertices:
        if vertex.numOfVisits == 0:
            unvisited.append(vertex)

    if unvisited:
        # 2a. Shortest flight time.
        shortest_ft = []
        cur_vertex = cycle.route[LEFT][len(cycle.route[LEFT]) - 1]
        min_value = cur_vertex.flightTimes[unvisited[0].name]

        for i in range(1, len(unvisited)):
            nxt_vertex = unvisited[i]

            if cur_vertex.flightTimes[nxt_vertex] <= min_value:
                min_value = cur_vertex.flightTimes[nxt_vertex.name]

        for vertex in unvisited:
            if cur_vertex.flightTimes[vertex.name] == min_value:
                shortest_ft.append(vertex)

        # 3a. Shortest deadline.
        shortest_d = shortest_ft[0]

        if len(shortest_ft) > 1:
            min_value = shortest_ft[0].deadlines

            for i in range(1, len(shortest_ft)):
                nxt_vertex = shortest_ft[i]

                if nxt_vertex.deadlines <= min_value:
                    min_value = nxt_vertex.deadlines
                    shortest_d = nxt_vertex

        return shortest_d

    # 2b. Right end vertex.
    return cycle.route[RIGHT][len(cycle.route[RIGHT]) - 1]


def check_constraints(vertex, nxt_vertex, direction):
    opp_direction = 1 - direction
    cur_time_slot = len(cycle.route[direction]) - 1
    cur_opp_time_slot = len(cycle.route[opp_direction]) - 1
    end_vertex = cycle.route[direction][cur_time_slot]  # on the side the tree is growing

    if nxt_vertex is None:
        nxt_vertex = end_vertex

    travel_time = end_vertex.flightTimes[nxt_vertex.name] + \
                  cycle.routeTimes[direction][cur_time_slot]  # on one side
    opp_travel_time = cycle.routeTimes[opp_direction][cur_opp_time_slot]  # the other side

    if cycle.route[opp_direction][cur_opp_time_slot] != nxt_vertex:
        # Constraint No. 1
        if vertex.numOfVisits > 0 or vertex != nxt_vertex:
            if vertex.firstVisits[direction] is not None:
                travel_time -= vertex.lastVisits[direction]
            elif vertex.firstVisits[opp_direction] is not None:
                opp_travel_time = vertex.firstVisits[opp_direction]
                travel_time += opp_travel_time
        else:
            travel_time += opp_travel_time
    else:
        # Constraint No. 2
        if vertex == nxt_vertex:
            if vertex.numOfVisits > 0:
                if vertex.firstVisits[direction] is None:
                    opp_travel_time = vertex.firstVisits[opp_direction]
                    travel_time += opp_travel_time
                else:
                    travel_time -= vertex.lastVisits[direction]
        elif vertex.numOfVisits > 1:
            if vertex.firstVisits[direction] is None:
                travel_time = (travel_time + vertex.firstVisits[opp_direction]) + \
                              (opp_travel_time - vertex.lastVisits[opp_direction])
            elif vertex.firstVisits[opp_direction] is None:
                travel_time = (travel_time - vertex.lastVisits[direction]) + \
                              (opp_travel_time + vertex.firstVisits[direction])
            else:
                travel_time = (travel_time - vertex.lastVisits[direction]) + \
                              (opp_travel_time - vertex.lastVisits[opp_direction])
        else:
            travel_time += opp_travel_time

    if travel_time > vertex.deadline:
        # print("Constraint violated! Vertex: " + str(vertex))
        return vertex
    else:
        return


def handle_violations(violated, nxt_vertex, direction):
    opp_direction = 1 - direction
    cur_time_slot = len(cycle.route[direction]) - 1
    cur_opp_time_slot = len(cycle.route[opp_direction]) - 1
    end_vertex = cycle.route[direction][cur_time_slot]
    opp_end_vertex = cycle.route[opp_direction][cur_opp_time_slot]

    if len(violated) == 1:
        if end_vertex != violated[0] or end_vertex == opp_end_vertex:
            nxt_vertex = violated[0]
        else:
            removed_vertex = cycle.route[opp_direction][cur_opp_time_slot]

            # Replace the opposite end vertex with the violated vertex.
            cycle.route[opp_direction][cur_opp_time_slot] = violated[0]

            # Update routeTimes.
            opp_second_end_vertex = cycle.route[opp_direction][cur_opp_time_slot - 1]
            flight_time = violated[0].flightTimes[opp_second_end_vertex.name]
            travel_time = cycle.routeTimes[opp_direction][cur_opp_time_slot - 1]
            cycle.routeTimes[opp_direction][cur_opp_time_slot] = travel_time + flight_time

            # Update the opposite end vertex.
            opp_second_end_vertex = violated[0]

            if opp_second_end_vertex.firstVisits[opp_direction] is None:
                opp_second_end_vertex.firstVisits[opp_direction] = \
                    cycle.routeTimes[opp_direction][cur_opp_time_slot]

            opp_second_end_vertex.lastVisits[opp_direction] = \
                cycle.routeTimes[opp_direction][cur_opp_time_slot]
            opp_second_end_vertex.numOfVisits += 1

            # Update firstVisits or/and lastVisits of removed_vertex.
            update_removed_vertex(removed_vertex, opp_direction)

            return None

    # Remove end_vertex from route and routeTimes.
    del cycle.route[direction][cur_time_slot]
    del cycle.routeTimes[direction][cur_time_slot]

    # Update end_vertex.
    update_removed_vertex(end_vertex, direction)
    return nxt_vertex


def update_removed_vertex(vertex, direction):
    vertex.numOfVisits -= 1

    if vertex.firstVisits[direction] is not None:
        cur_time_slot = len(cycle.route[direction]) - 1

        # Last occurrence of vertex.
        for i in range(cur_time_slot, -1):
            if cycle.route[direction][i] == vertex:
                vertex.lastVisits[direction] = cycle.routeTimes[direction][i]
                return

    vertex.firstVisits[direction] = vertex.lastVisits[direction] = None


def update_relative_deadlines(nxt_vertex, direction):
    for vertex in vertices:
        if vertex == nxt_vertex and direction == RIGHT:
            travel_time = 0
        else:
            travel_time = cycle.routeTimes[RIGHT][len(cycle.route[RIGHT]) - 1]

            if vertex.numOfVisits > 0:
                if vertex.firstVisits[RIGHT] is not None:
                    travel_time -= vertex.lastVisits[RIGHT]
                else:
                    travel_time += vertex.firstVisits[LEFT]
            else:
                travel_time += cycle.routeTimes[LEFT][len(cycle.route[LEFT]) - 1]

        vertex.relativeDeadline = vertex.deadline - travel_time


def print_legend():
    print('[ Legend ]')
    print('{x} - the pivot, where x is the vertex')
    print('->  - the next vertex to visit (already included in the route)')
    print('~>  - the next vertex to visit (not yet included in the route)')
    print('|   - the vertex/vertices which violate(s) the constraint')
    print()


def print_solution():
    print('\n' + '[ Case ' + file_name + ' ]')
    print('\n<< Results >>')

    if len(cycle.route[RIGHT]) > len(cycle.route[LEFT]):
        print('Cyclic route: ' + cycle.get_route_str()[:-4])
    else:
        print('Cyclic route: ' + cycle.get_route_str()[5:])

    print('Cyclic time: ' + str(cycle.routeTimes[RIGHT][len(cycle.route[RIGHT]) - 1] +
                                cycle.routeTimes[LEFT][len(cycle.route[LEFT]) - 1]))
    print('Time slots: ' + str(len(cycle.route[RIGHT]) + len(cycle.route[LEFT]) - 2))
    print('Iterations: ' + str(iterations))


main()
