# Assumptions:
# 1. The cycle is always in clockwise direction.
#    Although in reality it does not matter,
#    flight times are symmetrical; undirected graph.

RIGHT = 0
LEFT = 1
file_name = '1.2'
iterations = 0


def main():
    initialisation()
    simple_decision_check()
    violated = []
    is_solution_found = False
    global iterations

    print('<< Procedure >>')

    while not is_solution_found:
        for direction in range(2):
            iterations += 1

            route_str = get_route_str()

            # Compute the next vertex to visit.
            if direction == RIGHT:
                nxt_vertex = get_nxt_right_vertex()
            else:
                nxt_vertex = get_nxt_left_vertex()

            # Check constraints for each vertex.
            for vertex in range(totalVertices):
                violated_vertex = check_constraints(vertex, nxt_vertex, direction)

                if violated_vertex is not None:
                    violated.append(violated_vertex)

            # Print procedure.
            violated_str = ''

            if violated:
                violated_str = ', '.join([str(vertex) for vertex in violated])

                if direction == RIGHT:
                    violated_str = ' | ' + violated_str
                else:
                    violated_str += ' | '

            if direction == RIGHT:
                print(route_str + ' ~> ' + str(nxt_vertex) + violated_str)
            else:
                print(violated_str + str(nxt_vertex) + ' ~> ' + route_str)

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

                cur_time_slot = len(route[direction]) - 1
                end_vertex = route[direction][cur_time_slot]
                flight_time = flightTimes[end_vertex][nxt_vertex]
                old_travel_time = routeTimes[direction][cur_time_slot]
                new_travel_time = old_travel_time + flight_time

                # Update route and routeTimes
                route[direction].append(nxt_vertex)
                routeTimes[direction].append(new_travel_time)

                # Update nxt_vertex.
                if firstVisits[direction][nxt_vertex] is not None:
                    lastVisits[direction][nxt_vertex] = new_travel_time
                else:
                    firstVisits[direction][nxt_vertex] = \
                        lastVisits[direction][nxt_vertex] = new_travel_time

                numOfVisits[nxt_vertex] += 1

            # Update relative deadlines of all vertices.
            update_relative_deadlines(nxt_vertex, direction)

            # Base case:
            if route[LEFT][len(route[LEFT]) - 1] == route[RIGHT][len(route[RIGHT]) - 1]:
                # A loop is formed.

                # Check if all vertices have been visited at least once.
                for vertex in range(totalVertices):
                    if numOfVisits[vertex] < 1:
                        is_solution_found = False
                        break
                    else:
                        is_solution_found = True

                if is_solution_found:
                    break

    print_solution()


def initialisation():
    global pivot, totalVertices, numOfVisits, \
        deadlines, relativeDeadlines, flightTimes, \
        route, routeTimes, \
        firstVisits, lastVisits

    route = [RIGHT, LEFT]
    routeTimes = [RIGHT, LEFT]
    firstVisits = [RIGHT, LEFT]
    lastVisits = [RIGHT, LEFT]
    deadlines, flightTimes = extract_data()
    relativeDeadlines = []
    totalVertices = len(deadlines)
    pivot = get_pivot()
    numOfVisits = []

    for direction in range(2):
        route[direction] = []
        route[direction].append(pivot)
        routeTimes[direction] = []
        routeTimes[direction].append(0)
        firstVisits[direction] = []
        lastVisits[direction] = []

    for i in range(totalVertices):
        for direction in range(2):
            firstVisits[direction].append(None)
            lastVisits[direction].append(None)

        relativeDeadlines.append(deadlines[i])
        numOfVisits.append(0)

    for i in range(direction):
        firstVisits[i][pivot] = lastVisits[i][pivot] = 0

    numOfVisits[pivot] = 1


def extract_data():
    ft = []

    with open(file_name, 'r') as file:
        data = [line.split() for line in file]

        # First line contains relative deadline of each vertex.
        rd = [int(i) for i in data[0]]

        # Skip the first line in text file.
        for i in range(len(data) - 1):
            temp = [int(j) for j in data[i + 1]]
            ft.append(temp)

        return rd, ft


def get_pivot():
    max_rd = -1

    for i in range(totalVertices):
        if deadlines[i] >= max_rd:
            max_rd = deadlines[i]
            vertex = i

    return vertex


def simple_decision_check():
    for i in range(totalVertices):
        for j in range(totalVertices):
            if flightTimes[i][j] > 0.5 * relativeDeadlines[i]:
                return False  # no solution can be found

    return True  # possible solution can be found, but not guaranteed


def get_nxt_right_vertex():
    # 1. Least visited vertices.
    least_visited = []
    min_value = numOfVisits[0]
    end_vertex = route[RIGHT][len(route[RIGHT]) - 1]

    for num in numOfVisits:
        if num < min_value:
            min_value = num

    for vertex in range(totalVertices):
        if vertex != end_vertex and numOfVisits[vertex] == min_value:
            least_visited.append(vertex)

    # 2. Shortest relative deadline.
    if len(least_visited) > 1:
        shortest_rd = []
        min_value = relativeDeadlines[least_visited[0]]
        print(str(least_visited[0]) + ': ' + str(min_value))

        for i in range(1, len(least_visited)):
            nxt_vertex = least_visited[i]
            # print(str(nxt_vertex) + ': ' + str(relativeDeadlines[nxt_vertex]))

            if relativeDeadlines[nxt_vertex] < min_value:
                min_value = relativeDeadlines[nxt_vertex]

        for vertex in least_visited:
            if relativeDeadlines[vertex] == min_value:
                shortest_rd.append(vertex)
    else:
        return least_visited[0]

    # 3. Shortest flight time.
    shortest_ft = shortest_rd[0]

    if len(shortest_rd) > 1:
        cur_vertex = route[RIGHT][len(route[RIGHT]) - 1]
        min_value = flightTimes[cur_vertex][shortest_rd[0]]

        for i in range(1, len(shortest_rd)):
            nxt_vertex = shortest_rd[i]

            if flightTimes[cur_vertex][nxt_vertex] <= min_value:
                min_value = flightTimes[cur_vertex][nxt_vertex]
                shortest_ft = nxt_vertex

    return shortest_ft


def get_nxt_left_vertex():
    # 1. Unvisited vertices.
    unvisited = []

    for vertex in range(totalVertices):
        if numOfVisits[vertex] == 0:
            unvisited.append(vertex)

    if unvisited:
        # 2a. Shortest flight time.
        shortest_ft = []
        cur_vertex = route[LEFT][len(route[LEFT]) - 1]
        min_value = flightTimes[cur_vertex][unvisited[0]]

        for i in range(1, len(unvisited)):
            nxt_vertex = unvisited[i]

            if flightTimes[cur_vertex][nxt_vertex] <= min_value:
                min_value = flightTimes[cur_vertex][nxt_vertex]

        for vertex in unvisited:
            if flightTimes[cur_vertex][vertex] == min_value:
                shortest_ft.append(vertex)

        # 3a. Shortest deadline.
        shortest_d = shortest_ft[0]

        if len(shortest_ft) > 1:
            min_value = deadlines[shortest_ft[0]]

            for i in range(1, len(shortest_ft)):
                nxt_vertex = shortest_ft[i]

                if deadlines[nxt_vertex] <= min_value:
                    min_value = deadlines[nxt_vertex]
                    shortest_d = nxt_vertex

        return shortest_d

    # 2b. Right end vertex.
    return route[RIGHT][len(route[RIGHT]) - 1]


def check_constraints(vertex, nxt_vertex, direction):
    opp_direction = 1 - direction
    cur_time_slot = len(route[direction]) - 1
    cur_opp_time_slot = len(route[opp_direction]) - 1
    end_vertex = route[direction][cur_time_slot]  # on the side the tree is growing

    if nxt_vertex is None:
        nxt_vertex = end_vertex

    travel_time = flightTimes[end_vertex][nxt_vertex] + \
                  routeTimes[direction][cur_time_slot]  # on one side
    opp_travel_time = routeTimes[opp_direction][cur_opp_time_slot]  # the other side

    if route[opp_direction][cur_opp_time_slot] != nxt_vertex:
        # Constraint No. 1
        if numOfVisits[vertex] > 0 or vertex != nxt_vertex:
            if firstVisits[direction][vertex] is not None:
                travel_time -= lastVisits[direction][vertex]
            elif firstVisits[opp_direction][vertex] is not None:
                opp_travel_time = firstVisits[opp_direction][vertex]
                travel_time += opp_travel_time
        else:
            travel_time += opp_travel_time
    else:
        # Constraint No. 2
        if vertex == nxt_vertex:
            if numOfVisits[vertex] > 0:
                if firstVisits[direction][vertex] is None:
                    opp_travel_time = firstVisits[opp_direction][vertex]
                    travel_time += opp_travel_time
                else:
                    travel_time -= lastVisits[direction][vertex]
        elif numOfVisits[vertex] > 1:
            if firstVisits[direction][vertex] is None:
                travel_time = (travel_time + firstVisits[opp_direction][vertex]) + \
                              (opp_travel_time - lastVisits[opp_direction][vertex])
            elif firstVisits[opp_direction][vertex] is None:
                travel_time = (travel_time - lastVisits[direction][vertex]) + \
                              (opp_travel_time + firstVisits[direction][vertex])
            else:
                travel_time = (travel_time - lastVisits[direction][vertex]) + \
                              (opp_travel_time - lastVisits[opp_direction][vertex])
        else:
            travel_time += opp_travel_time

    if travel_time > deadlines[vertex]:
        # print("Constraint violated! Vertex: " + str(vertex))
        return vertex
    else:
        return


def handle_violations(violated, nxt_vertex, direction):
    opp_direction = 1 - direction
    cur_time_slot = len(route[direction]) - 1
    cur_opp_time_slot = len(route[opp_direction]) - 1
    end_vertex = route[direction][cur_time_slot]
    opp_end_vertex = route[opp_direction][cur_opp_time_slot]

    if len(violated) == 1:
        if end_vertex != violated[0] or end_vertex == opp_end_vertex:
            nxt_vertex = violated[0]
        else:
            removed_vertex = route[opp_direction][cur_opp_time_slot]

            # Replace the opposite end vertex with the violated vertex.
            route[opp_direction][cur_opp_time_slot] = violated[0]

            # Update routeTimes.
            opp_second_end_vertex = route[opp_direction][cur_opp_time_slot - 1]
            flight_time = flightTimes[opp_second_end_vertex][violated[0]]
            travel_time = routeTimes[opp_direction][cur_opp_time_slot - 1]
            routeTimes[opp_direction][cur_opp_time_slot] = travel_time + flight_time

            # Update the opposite end vertex.
            opp_second_end_vertex = violated[0]

            if firstVisits[opp_direction][opp_second_end_vertex] is None:
                firstVisits[opp_direction][opp_second_end_vertex] = routeTimes[opp_direction][cur_opp_time_slot]

            lastVisits[opp_direction][opp_second_end_vertex] = routeTimes[opp_direction][cur_opp_time_slot]
            numOfVisits[opp_second_end_vertex] += 1

            # Update firstVisits or/and lastVisits of removed_vertex.
            update_removed_vertex(removed_vertex, opp_direction)

            return None

    # Remove end_vertex from route and routeTimes.
    del route[direction][cur_time_slot]
    del routeTimes[direction][cur_time_slot]

    # Update end_vertex.
    update_removed_vertex(end_vertex, direction)
    return nxt_vertex


def update_removed_vertex(vertex, direction):
    numOfVisits[vertex] -= 1

    if firstVisits[direction][vertex] is not None:
        cur_time_slot = len(route[direction]) - 1

        # Last occurrence of replaced_vertex.
        for i in range(cur_time_slot, -1):
            if route[direction][i] == vertex:
                lastVisits[vertex] = routeTimes[direction][i]
                return

    firstVisits[direction][vertex] = lastVisits[direction][vertex] = None

    
def update_relative_deadlines(nxt_vertex, direction):
    for vertex in range(totalVertices):
        if vertex == nxt_vertex and direction == RIGHT:
            travel_time = 0
        else:
            travel_time = routeTimes[RIGHT][len(route[RIGHT]) - 1]

            if numOfVisits[vertex] > 0:
                if firstVisits[RIGHT][vertex] is not None:
                    travel_time -= lastVisits[RIGHT][vertex]
                else:
                    travel_time += firstVisits[LEFT][vertex]
            else:
                travel_time += routeTimes[LEFT][len(route[LEFT]) - 1]

        relativeDeadlines[vertex] = deadlines[vertex] - travel_time


def get_route_str():
    route_str = '{' + str(pivot) + '}'

    for i in range(1, len(route[RIGHT])):
        route_str += ' -> ' + str(route[RIGHT][i])

    for i in range(1, len(route[LEFT])):
        route_str = str(route[LEFT][i]) + ' -> ' + route_str

    return route_str


def print_solution():
    print('\n' + '[ Case ' + file_name + ' ]')
    print('\n<< Results >>')

    if len(route[RIGHT]) > len(route[LEFT]):
        print('Cyclic route: ' + get_route_str()[:-4])
    else:
        print('Cyclic route: ' + get_route_str()[5:])

    print('Cyclic time: ' + str(routeTimes[RIGHT][len(route[RIGHT]) - 1] +
                                routeTimes[LEFT][len(route[LEFT]) - 1]))
    print('Time slots: ' + str(len(route[RIGHT]) + len(route[LEFT]) - 2))
    print('Iterations: ' + str(iterations))


main()
