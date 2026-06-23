import math


# Du lieu ban dau: ma node va toa do (x, y).
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

# Chọn tâm trong các điểm dữ liệu ban đầu. Ở đây, tôi chọn bằng cách lấy thứ tự là số nguyên tố là nhỏ nhất.

# def is_prime(n):
#     """Kiểm tra số nguyên n có phải là số nguyên tố không."""
#     if n <= 1:
#         return False
#     for i in range(2, int(math.sqrt(n)) + 1):
#         if n % i == 0:
#             return False
#     return True

# prime_indices = [i for i in range(len(POINTS)) if is_prime(i)]
# centers = [POINTS[i] for i in prime_indices[:3]]  
centers = [POINTS[1], POINTS[2], POINTS[3]]
print("Tâm ban đầu:", centers)

def distance(point, center):
    """Tinh khoang cach Euclid tu mot diem den mot tam."""
    return math.sqrt(
        (point[0] - center[0]) ** 2
        + (point[1] - center[1]) ** 2
    )


def assign_clusters(points, centers):
    """Gan moi diem vao tam GAN THU NHI (nho thu nhi)."""
    clusters = [[] for _ in centers]

    for point_id, point in points.items():
        # 1. Tính khoảng cách từ điểm hiện tại tới cả 3 tâm
        # Kết quả trả về dạng danh sách các tuple: [(khoảng_cách, vị_trí_tâm), ...]
        distances_with_index = [
            (distance(point, center), idx)
            for idx, center in enumerate(centers)
        ]

        # 2. Sắp xếp danh sách theo thứ tự khoảng cách tăng dần
        distances_with_index.sort(key=lambda x: x[0])

        # 3. Lấy phần tử ở vị trí index 1 (chính là nhỏ thứ nhì)
        # distances_with_index[0] là nhỏ nhất, distances_with_index[1] là nhỏ thứ nhì
        second_nearest_center = distances_with_index[0][1]

        # 4. Gán ID của điểm vào cụm nhỏ thứ nhì đó
        clusters[second_nearest_center].append(point_id)

    return clusters

def calculate_centers(points, clusters, old_centers):
    """Tinh tam moi bang trung binh toa do cac diem trong cum."""
    new_centers = []

    for cluster_id, point_ids in enumerate(clusters):
        if not point_ids:
            new_centers.append(old_centers[cluster_id])
            continue

        average_x = sum(points[i][0] for i in point_ids) / len(point_ids)
        average_y = sum(points[i][1] for i in point_ids) / len(point_ids)
        new_centers.append((average_x, average_y))

    return new_centers


def kmeans(points, centers, max_iterations=100):
    """Lap hai buoc: gan cum va tinh lai tam."""
    for iteration in range(1, max_iterations + 1):
        clusters = assign_clusters(points, centers)
        new_centers = calculate_centers(points, clusters, centers)

        print(f"\nLan lap {iteration}:")
        for i in range(len(centers)):
            print(
                f"  Cum C{i + 1}: {clusters[i]} "
                f"-> tam ({new_centers[i][0]:.2f}, {new_centers[i][1]:.2f})"
            )

        if new_centers == centers:
            print("\nThuat toan da hoi tu.")
            return clusters, new_centers

        centers = new_centers

    return clusters, centers


final_clusters, final_centers = kmeans(POINTS, centers)

print("\nKET QUA CUOI CUNG")
for i in range(len(final_centers)):
    print(
        f"Cum C{i + 1}: {final_clusters[i]} "
        f"- tam ({final_centers[i][0]:.2f}, {final_centers[i][1]:.2f})"
    )
