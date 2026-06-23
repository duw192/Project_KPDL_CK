import math
from collections import Counter

# ──────────────────────────────────────────────
# DỮ LIỆU (15 mẫu)
# ──────────────────────────────────────────────
features = ["outlook", "temperature", "humidity", "wind"]

data = [
    # outlook     temperature   humidity   wind       play
    ["sunny",    "hot",       "high",    "weak",   "no"],
    ["sunny",    "hot",       "high",    "strong", "no"],
    ["overcast", "hot",       "high",    "weak",   "yes"],
    ["rainy",    "mild",      "high",    "weak",   "yes"],
    ["rainy",    "cool",      "normal",  "weak",   "yes"],
    ["rainy",    "cool",      "normal",  "strong", "no"],
    ["overcast", "cool",      "normal",  "strong", "yes"],
    ["sunny",    "mild",      "high",    "weak",   "no"],
    ["sunny",    "cool",      "normal",  "weak",   "yes"],
    ["rainy",    "mild",      "normal",  "weak",   "yes"],
    ["sunny",    "mild",      "normal",  "strong", "yes"],
    ["overcast", "mild",      "high",    "strong", "yes"],
    ["overcast", "hot",       "normal",  "weak",   "yes"],
    ["rainy",    "mild",      "high",    "strong", "no"],
    ["sunny",    "cool",      "normal",  "strong", "no"],
]

# ──────────────────────────────────────────────
# CÁC HÀM ID3
# ──────────────────────────────────────────────
def tinh_entropy(danh_sach_nhan):
    tong = len(danh_sach_nhan)
    if tong == 0:
        return 0
    e = 0
    for so_lan in Counter(danh_sach_nhan).values():
        p = so_lan / tong
        if p > 0:
            e -= p * math.log2(p)
    return e

def tinh_info_gain(du_lieu, chi_so_feature):
    nhan_goc = [mau[-1] for mau in du_lieu]
    entropy_goc = tinh_entropy(nhan_goc)
    nhom = {}
    for mau in du_lieu:
        gia_tri = mau[chi_so_feature]
        nhom.setdefault(gia_tri, []).append(mau[-1])
    entropy_sau = sum(
        (len(nhan) / len(nhan_goc)) * tinh_entropy(nhan)
        for nhan in nhom.values()
    )
    return entropy_goc - entropy_sau

def tao_la(nhan):
    return {"la": True, "nhan": nhan}

def xay_cay(du_lieu, cac_feature_con_lai):
    nhan_goc = [mau[-1] for mau in du_lieu]
    if len(set(nhan_goc)) == 1:
        return tao_la(nhan_goc[0])
    if not cac_feature_con_lai:
        return tao_la(Counter(nhan_goc).most_common(1)[0][0])

    feature_tot_nhat = max(
        cac_feature_con_lai,
        key=lambda i: tinh_info_gain(du_lieu, i)
    )
    nut = {
        "la": False,
        "ten_feature": features[feature_tot_nhat],
        "chi_so": feature_tot_nhat,
        "nhanh": {}
    }
    cac_feature_moi = [i for i in cac_feature_con_lai if i != feature_tot_nhat]
    for gia_tri in sorted(set(mau[feature_tot_nhat] for mau in du_lieu)):
        tap_con = [mau for mau in du_lieu if mau[feature_tot_nhat] == gia_tri]
        nut["nhanh"][gia_tri] = xay_cay(tap_con, cac_feature_moi)
    return nut

def du_doan_cay(nut, mau):
    if nut["la"]:
        return nut["nhan"]
    gia_tri = mau[nut["chi_so"]]
    if gia_tri not in nut["nhanh"]:
        return "Không xác định"
    return du_doan_cay(nut["nhanh"][gia_tri], mau)

# ──────────────────────────────────────────────
# HÀM IN CÂY RA TERMINAL
# ──────────────────────────────────────────────
def in_cay(nut, thut_le="", ten_nhanh=""):
    # Nếu là lá (kết quả)
    if nut["la"]:
        print(f"{thut_le}└── Nhánh {ten_nhanh} -> KẾT QUẢ: {nut['nhan']}")
        return
    
    # Nếu là nút quyết định
    if ten_nhanh:
        print(f"{thut_le}└── Nhánh {ten_nhanh} -> Kiểm tra [ {nut['ten_feature'].upper()} ]")
    else:
        print(f"{thut_le}└── NÚT GỐC: [ {nut['ten_feature'].upper()} ]")
        
    # Duyệt qua các nhánh con
    for gia_tri, con in nut["nhanh"].items():
        in_cay(con, thut_le + "    ", gia_tri)

# ──────────────────────────────────────────────
# CHẠY
# ──────────────────────────────────────────────
if __name__ == "__main__":
    print("--- ĐANG XÂY DỰNG CÂY QUYẾT ĐỊNH ID3 ---")
    cay = xay_cay(data, list(range(len(features))))
    
    print("\nCẤU TRÚC CÂY QUYẾT ĐỊNH:")
    in_cay(cay)
    print("-" * 40)

    # Kiểm thử dự đoán
    mau_thu = ["sunny", "cool", "high", "strong", "?"]
    ket_qua = du_doan_cay(cay, mau_thu)
    print(f"\nDự đoán cho mẫu {mau_thu[:-1]}: {ket_qua}")