import argparse
import math


POINTS = {
    0: (1, 5),
    1: (3, 5),
    2: (2, 14),
    3: (3, 4),
    4: (12, 4),
    5: (2, 6),
    6: (4, 1),
    7: (4, 14),
    8: (4, 7),
    9: (4, 6),
    10: (7, 1),
    11: (6, 5),
    12: (8, 1),
    13: (4, 8),
    14: (8, 3),
    15: (5, 5),
    16: (3, 12),
    17: (7, 13),
}

K = 3
MAX_ITERATIONS = 5


def round2(value):
    return round(value + 1e-12, 2)


def format_center(center):
    return f"({center[0]:.2f}, {center[1]:.2f})"


def euclidean_distance(point, center):
    return round2(math.sqrt((point[0] - center[0]) ** 2 + (point[1] - center[1]) ** 2))


def get_initial_node_ids(last_three_digits):
    if len(last_three_digits) != K or not last_three_digits.isdigit():
        raise ValueError("Nhap dung 3 so cuoi MSSV, vi du: 123")

    counts = {}
    node_ids = []

    for digit_char in last_three_digits:
        digit = int(digit_char)
        counts[digit] = counts.get(digit, 0) + 1

        if counts[digit] == 1:
            node_ids.append(digit)
        elif counts[digit] == 2:
            node_ids.append(10)
        else:
            node_ids.append(11)

    return node_ids


def assign_points_to_clusters(centers):
    clusters = {i: [] for i in range(K)}
    distance_table = {}

    for point_id in sorted(POINTS):
        point = POINTS[point_id]
        distances = [euclidean_distance(point, center) for center in centers]
        best_cluster = min(range(K), key=lambda i: (distances[i], i))

        clusters[best_cluster].append(point_id)
        distance_table[point_id] = distances

    return clusters, distance_table


def update_centers(clusters, old_centers):
    new_centers = []

    for cluster_id in range(K):
        point_ids = clusters[cluster_id]

        if not point_ids:
            new_centers.append(old_centers[cluster_id])
            continue

        avg_x = sum(POINTS[point_id][0] for point_id in point_ids) / len(point_ids)
        avg_y = sum(POINTS[point_id][1] for point_id in point_ids) / len(point_ids)
        new_centers.append((round2(avg_x), round2(avg_y)))

    return new_centers


def print_points():
    print("Du lieu:")
    for point_id, point in POINTS.items():
        print(f"  Node {point_id:2d}: X = {point}")
    print()


def print_iteration(iteration, centers, clusters, distance_table, new_centers):
    print(f"Lan lap {iteration}")
    print("Tam hien tai:")
    for i, center in enumerate(centers, start=1):
        print(f"  C{i} = {format_center(center)}")

    print("Khoang cach va cum duoc chon:")
    print("  STT    d(C1)   d(C2)   d(C3)   Cum")
    for point_id in sorted(POINTS):
        distances = distance_table[point_id]
        chosen_cluster = next(i for i in range(K) if point_id in clusters[i])
        print(
            f"  {point_id:2d}     "
            f"{distances[0]:5.2f}   {distances[1]:5.2f}   {distances[2]:5.2f}   "
            f"C{chosen_cluster + 1}"
        )

    print("Cac cum:")
    for i in range(K):
        print(f"  C{i + 1}: {clusters[i]}")

    print("Tam moi:")
    for i, center in enumerate(new_centers, start=1):
        print(f"  C{i} = {format_center(center)}")
    print("-" * 55)


def run_kmeans(last_three_digits):
    initial_node_ids = get_initial_node_ids(last_three_digits)
    centers = [POINTS[node_id] for node_id in initial_node_ids]
    previous_clusters = None
    final_clusters = None

    print_points()
    print(f"3 so cuoi MSSV: {last_three_digits}")
    print(f"Node tam ban dau: {initial_node_ids}")
    print()

    for iteration in range(1, MAX_ITERATIONS + 1):
        clusters, distance_table = assign_points_to_clusters(centers)
        new_centers = update_centers(clusters, centers)

        print_iteration(iteration, centers, clusters, distance_table, new_centers)

        if clusters == previous_clusters or new_centers == centers:
            centers = new_centers
            final_clusters = clusters
            print("Dung vi cum/tam khong thay doi.")
            break

        previous_clusters = clusters
        final_clusters = clusters
        centers = new_centers
    else:
        print(f"Dung vi da lap toi da {MAX_ITERATIONS} lan.")

    print("Ket qua cuoi cung:")
    for i in range(K):
        print(f"  Cum C{i + 1}: {final_clusters[i]}")
    print("  Tam cuoi:")
    for i, center in enumerate(centers, start=1):
        print(f"    C{i} = {format_center(center)}")


def parse_args():
    parser = argparse.ArgumentParser(description="Thuat toan K-means cho bai tap trong anh.")
    parser.add_argument(
        "mssv",
        nargs="?",
        help="3 so cuoi MSSV, vi du: 123. Neu bo trong, chuong trinh se hoi khi chay.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    last_three_digits = args.mssv

    if not last_three_digits:
        last_three_digits = input("Nhap 3 so cuoi MSSV: ").strip()

    run_kmeans(last_three_digits)


if __name__ == "__main__":
    main()
