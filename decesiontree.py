
import math
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

# ──────────────────────────────────────────────
# DỮ LIỆU (đọc từ ảnh, 15 mẫu)
# cột: outlook, temperature, humidity, wind, play
# ──────────────────────────────────────────────
features = ["outlook", "temperature", "humidity", "wind"]

data = [
    # outlook     temperature  humidity   wind      play
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
    # Tất cả cùng nhãn → lá
    if len(set(nhan_goc)) == 1:
        return tao_la(nhan_goc[0])
    # Hết feature → lá với nhãn đa số
    if not cac_feature_con_lai:
        return tao_la(Counter(nhan_goc).most_common(1)[0][0])

    # Chọn feature có IG cao nhất
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
# VẼ CÂY
# ──────────────────────────────────────────────
def ve_cay(nut):
    fig, ax = plt.subplots(figsize=(16, 9))
    ax.axis("off")
    vi_tri = {}

    tap_nhan = set()
    def lay_nhan(t):
        if t["la"]: tap_nhan.add(t["nhan"])
        else:
            for con in t["nhanh"].values(): lay_nhan(con)
    lay_nhan(nut)

    ds_mau = ["#27ae60", "#e74c3c", "#8e44ad", "#d35400", "#16a085"]
    bang_mau_la = {
        nhan: ds_mau[i % len(ds_mau)]
        for i, nhan in enumerate(sorted(tap_nhan))
    }

    def dem_la(t):
        if t["la"]: return 1
        return sum(dem_la(v) for v in t["nhanh"].values())

    def gan_vi_tri(t, tang, x0, x1):
        vi_tri[id(t)] = ((x0 + x1) / 2, 1 - tang * 0.22)
        if not t["la"]:
            tong_la = dem_la(t)
            cur = x0
            for con in t["nhanh"].values():
                la_con = dem_la(con)
                gan_vi_tri(con, tang + 1, cur,
                           cur + (x1 - x0) * la_con / tong_la)
                cur += (x1 - x0) * la_con / tong_la

    def ve_nut(t, nut_cha=None, nhan_canh=""):
        p = vi_tri[id(t)]
        if nut_cha:
            ax.annotate(
                "", xy=p, xytext=nut_cha,
                arrowprops=dict(arrowstyle="->", color="#95a5a6",
                                lw=1.5, shrinkA=14, shrinkB=14)
            )
            mx = (p[0] + nut_cha[0]) / 2
            my = (p[1] + nut_cha[1]) / 2
            ax.text(mx, my, nhan_canh, ha="center", va="center",
                    fontsize=9, color="#2c3e50", fontweight="bold",
                    bbox=dict(boxstyle="round4,pad=0.25", fc="#ecf0f1",
                              ec="#bdc3c7", lw=0.8))
        if t["la"]:
            mau_nen = bang_mau_la.get(t["nhan"], "#7f8c8d")
            ax.text(*p, t["nhan"], ha="center", va="center",
                    fontsize=11, fontweight="bold", color="white",
                    bbox=dict(boxstyle="round4,pad=0.55", fc=mau_nen,
                              ec="none"))
        else:
            ax.text(*p, t["ten_feature"], ha="center", va="center",
                    fontsize=11, fontweight="bold", color="white",
                    bbox=dict(boxstyle="round4,pad=0.55", fc="#2980b9",
                              ec="none"))
            for gia_tri, con in t["nhanh"].items():
                ve_nut(con, p, gia_tri)

    gan_vi_tri(nut, 0, 0, 1)
    ve_nut(nut)

    plt.title("Cây Quyết Định ID3 — Play Tennis",
              fontsize=15, fontweight="bold", color="#2c3e50", pad=16)
    legend_handles = [
        mpatches.Patch(color="#2980b9", label="Nút quyết định (feature)")
    ]
    for nhan, mau in bang_mau_la.items():
        legend_handles.append(
            mpatches.Patch(color=mau, label=f"Kết quả: {nhan}")
        )
    plt.legend(handles=legend_handles, loc="lower right",
               fontsize=10, frameon=True, shadow=True, fancybox=True)
    plt.tight_layout()
    plt.savefig("decision_tree.png", dpi=150, bbox_inches="tight")
    plt.show()

# ──────────────────────────────────────────────
# CHẠY
# ──────────────────────────────────────────────
if __name__ == "__main__":
    cay = xay_cay(data, list(range(len(features))))
    ve_cay(cay)

    # Kiểm thử dự đoán
    mau_thu = ["sunny", "cool", "high", "strong", "?"]
    ket_qua = du_doan_cay(cay, mau_thu)
    print(f"Dự đoán: {ket_qua}")  # → no
