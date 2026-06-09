import numpy as np


# Input: [70, 80, 90]
# Output: 80
def calculate_mean(scores: list) -> float:
    """Öğrencilerin notlarının ortalamasını hesapla."""
    return sum(scores) / len(scores)


# Input: [70, 80, 90, 100]
# Output: 85.0
def calculate_median(scores: list) -> float:
    """Öğrencilerin notlarının medyanını hesapla."""
    scores_sorted = sorted(scores)
    scores_len = len(scores_sorted)
    median = scores_len // 2  # 0, 1, 2, 3, 4 , /5

    if scores_len % 2 == 0:
        return (scores_sorted[median] + scores_sorted[median - 1]) / 2
    else:
        return scores_sorted[median]


# Input: [70, 70, 80, 90]
# Output: 70
def calculate_mode(scores: list) -> int:
    """En sık görülen notu hesapla (mode)."""
    max_score = scores[0]
    max_score_count = 0

    for score in set(scores):
        if scores.count(score) > max_score_count:
            max_score = score
            max_score_count = scores.count(score)

    return max_score


# Input: [10, 20, 30]
# Output: 8.16
def calculate_std(scores: list) -> float:
    """Standart sapmayı hesapla."""
    avg = sum(scores) / len(scores)
    sum_diff = 0

    for score in scores:
        sum_diff += (score - avg) ** 2

    return (sum_diff / len(scores)) ** 0.5


# Input: [10, 10, 10, 80] ise output median olmalı
# Input: [1,1,1,1] ise output mode
# Input: [10,15,20,25] ise output mean olmalı.
# Hardcoded bir şey olmamalı. Data içeriğine bakarak bu 3 hesaplamadan hangisini yapabileceğine bir kural ile kara vermelisin.
def determine_best_statistic(data: list) -> str:
    """Veri kümesine göre en uygun merkezi eğilim ölçüsünü seç ('mean', 'median' ya da 'mode')."""
    if len(set(data)) == 1:
        return "mode"

    avg = calculate_mean(data)
    med = calculate_median(data)

    if abs(avg - med) > 0.2 * abs(avg):
        return "median"
    return "mean"


# Input: ([10, 20, 30, 40, 50], 50)
# Output: 30
def calculate_percentile(scores: list, percentile: float) -> float:
    """Belirli bir persentil değerini hesapla (örn. 90. persentil)."""
    return float(np.percentile(scores, percentile))


# Input: ([10, 20, 30, 40, 50])
# Output: (20.0, 30.0, 40.0)
def calculate_quartiles(scores: list) -> tuple:
    """Q1, Q2, Q3 çeyrek değerlerini hesapla."""
    q1 = float(np.percentile(scores, 25))
    q2 = float(np.percentile(scores, 50))
    q3 = float(np.percentile(scores, 75))
    return (q1, q2, q3)


# Input: [10, 12, 14, 100]
# Output: [100]
# Bu işlemi yapmak için iqr dediğimiz bir hesaplama kullanmalısın.
# iqr = q3-q1(q: quartile)
# Daha sonrasonda lower ve upper adında iki tane değişken tanımlamalısın.
# lower = q1 - 1.5 * iqr, upper = q3 + 1.5 * iqr
# eğer dizideki elemanlar bu lower ve higher değerleri arasındaysa outlier değildirler.
def find_outliers(scores: list) -> list:
    """IQR kullanarak aykırı değerleri tespit et."""
    q1, q2, q3 = calculate_quartiles(scores)
    iqr = q3 - q1
    bottom_limit = q1 - 1.5 * iqr
    up_limit = q3 + 1.5 * iqr

    outliers = []
    for x in scores:
        if x < bottom_limit or x > up_limit:
            outliers.append(x)
    return outliers


# Input:
# data = {
#         'Gryffindor': [80, 85, 90],
#         'Slytherin': [60, 65, 70]
# }
# Output:
# {
#   'Gryffindor': 85.0,
#   'Slytherin': 65.0
# }
def house_score_summary(house_scores: dict) -> dict:
    """Her bir grup (Gryffindor, Slytherin vb.) için ortalama ve medyan notları döndür."""
    summary = {}
    for group, scores in house_scores.items():
        summary[group] = {
            "mean": calculate_mean(scores),
            "median": calculate_median(scores)
        }
    return summary


# Input:
#  data = {
#         'Gryffindor': [80, 85, 90],
#         'Slytherin': [60, 65, 70]
# }
# Output: 'Gryffindor'
def find_top_house(house_scores: dict) -> str:
    """En yüksek ortalamaya sahip grubu döndür."""
    best_group = ""
    best_score = 0
    for group, scores in house_scores.items():
        avg = calculate_mean(scores)
        if avg > best_score:
            best_score = avg
            en_iyi_grup = group
    return en_iyi_grup