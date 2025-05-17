import sys
from queue import PriorityQueue
import heapq

def dijkstra_by_priority_queue(adj_list: list[list[tuple]], start_index: int):
    vertex_count = len(adj_list)
    is_visited = [False] * vertex_count
    distance = [sys.maxsize] * vertex_count
    prev_index = [-1] * vertex_count

    priority_queue = PriorityQueue()

    distance[start_index] = 0
    priority_queue.put((0, start_index))

    while not priority_queue.empty():
        curr_distance, curr_index = priority_queue.get()

        if is_visited[curr_index]:  # distance[curr_index] < curr_distance:
            continue

        is_visited[curr_index] = True

        for next_index, edge_length in adj_list[curr_index]:
            next_distance = distance[curr_index] + edge_length

            if next_distance < distance[next_index]:
                distance[next_index] = next_distance
                prev_index[next_index] = curr_index
                priority_queue.put((distance[next_index], next_index))

    return distance, prev_index


def dijkstra_by_heapq(adj_list: list[list[tuple]], start_index: int):
    vertex_count = len(adj_list)
    is_visited = [False] * vertex_count
    distance = [sys.maxsize] * vertex_count
    prev_index = [-1] * vertex_count

    priority_queue = []

    distance[start_index] = 0
    heapq.heappush(priority_queue, (0, start_index))

    while priority_queue:
        curr_distance, curr_index = heapq.heappop(priority_queue)

        if is_visited[curr_index]:  # distance[curr_index] < curr_distance:
            continue

        is_visited[curr_index] = True

        for next_index, edge_length in adj_list[curr_index]:
            next_distance = distance[curr_index] + edge_length

            if next_distance < distance[next_index]:
                distance[next_index] = next_distance
                prev_index[next_index] = curr_index
                heapq.heappush(priority_queue, (distance[next_index], next_index))

    return distance, prev_index
