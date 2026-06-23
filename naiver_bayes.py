from collections import Counter

data = [
    [1,  "sunny",    "slope",      "hot",  "high",   "weak",   "no"],
    [2,  "sunny",    "undulating", "hot",  "low",    "strong", "no"],
    [3,  "overcast", "slope",      "hot",  "high",   "low",    "yes"],
    [4,  "rainy",    "flat",       "mild", "high",   "weak",   "no"],
    [5,  "rainy",    "undulating", "cool", "low",    "weak",   "yes"],
    [6,  "rainy",    "flat",       "cool", "normal", "low",    "no"],
    [7,  "overcast", "undulating", "cool", "normal", "strong", "yes"],
    [8,  "sunny",    "flat",       "mild", "high",   "weak",   "no"],
    [9,  "sunny",    "slope",      "cool", "normal", "weak",   "yes"],
    [10, "rainy",    "slope",      "mild", "low",    "weak",   "no"],
    [11, "sunny",    "flat",       "mild", "normal", "low",    "no"],
    [12, "overcast", "undulating", "mild", "high",   "strong", "yes"],
    [13, "overcast", "undulating", "hot",  "normal", "weak",   "yes"],
    [14, "rainy",    "slope",      "mild", "high",   "low",    "no"],
    [15, "sunny",    "flat",       "cool", "normal", "strong", "yes"],
    [16, "overcast", "flat",       "mild", "normal", "low",    "yes"],
    [17, "rainy",    "undulating", "mild", "high",   "strong", "no"],
]

test_data = [
    [18, "overcast", "slope",      "cool", "high",   "low"],
    [19, "rainy",    "undulating", "cool", "low",    "strong"],
    [20, "overcast", "slope",      "mild", "low",    "strong"],
    [21, "sunny",    "flat",       "cool", "high",   "low"],
    [22, "rainy",    "undulating", "cool", "normal", "weak"],
]


feature_names = ["outlook", "terrain", "temperature", "humidity", "wind"]

def predict_naive_bayes(train_data, sample, feature_names):
    """
    train_data: dữ liệu đã có nhãn play
    sample: mẫu cần dự đoán, gồm 5 thuộc tính:
            outlook, terrain, temperature, humidity, wind
    """
    total = len(train_data)
    if len(sample) != len(feature_names):
        raise ValueError("sample and feature_names must have the same length")

    labels = [row[-1] for row in train_data]
    label_counts = Counter(labels)
    
    classes = label_counts.keys()

    scores = {}

    for c in classes:
        # P(c)
        prior = label_counts[c] / total

        # Lọc các dòng có nhãn c
        rows_of_class = [row for row in train_data if row[-1] == c]

        probability = prior

        print(f"\nTính cho class = {c}")
        print(f"P({c}) = {label_counts[c]}/{total} = {prior}")

        # Tính P(x1|c) * P(x2|c) * ...
        for i in range(len(sample)):
            value = sample[i]

            count_value = 0

            for row in rows_of_class:
                if row[i + 1] == value:
                    count_value += 1

            conditional_prob = count_value / label_counts[c]

            print(
                f"P({feature_names[i]} = {value} | {c}) "
                f"= {count_value}/{label_counts[c]} = {conditional_prob}"
            )

            probability *= conditional_prob

        scores[c] = probability

        print(f"Score({c}) = {probability}")

    # Chọn class có xác suất lớn nhất
    predicted_label = max(scores, key=scores.get)

    return predicted_label, scores

for test_row in test_data:
    sample_id = test_row[0]
    sample_features = test_row[1:]

    print("\n" + "=" * 60)
    print(f"Dự đoán mẫu {sample_id}: {sample_features}")
    print(f"Số mẫu train hiện tại: {len(data)}")

    predicted_label, scores = predict_naive_bayes(data, sample_features, feature_names)

    print(f"\nKết quả mẫu {sample_id}: {predicted_label}")
    print(f"Xác suất: {scores}")

    # Thêm mẫu vừa dự đoán vào tập dữ liệu
    new_row = test_row + [predicted_label]
    data.append(new_row)

    print(f"Đã thêm mẫu {sample_id} vào tập train với nhãn: {predicted_label}")

print("\n" + "=" * 60)
print("Tập dữ liệu sau khi dự đoán tăng dần:")

for row in data:
    print(row)
