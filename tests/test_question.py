import pytest
import pandas as pd
import numpy as np
import requests
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tasks.task_manager import *

def test_calculate_mean():
    assert calculate_mean([70, 80, 90]) == 80.0

def test_calculate_median():
    assert calculate_median([70, 80, 90]) == 80.0
    assert calculate_median([70, 80, 90, 100]) == 85.0

def test_calculate_mode():
    assert calculate_mode([70, 70, 80, 90]) == 70

def test_calculate_std():
    assert round(calculate_std([10, 20, 30]), 2) == 8.16

def test_determine_best_statistic():
    assert determine_best_statistic([10, 10, 10, 80]) == 'median'

def test_calculate_percentile():
    assert calculate_percentile([10, 20, 30, 40, 50], 50) == 30

def test_calculate_quartiles():
    assert calculate_quartiles([10, 20, 30, 40, 50]) == (20.0, 30.0, 40.0)

def test_find_outliers():
    assert find_outliers([10, 12, 14, 100]) == [100]

def test_house_score_summary():
    data = {
        'Gryffindor': [80, 85, 90],
        'Slytherin': [60, 65, 70]
    }
    assert house_score_summary(data)['Gryffindor']['mean'] == 85.0

def test_find_top_house():
    data = {
        'Gryffindor': [80, 85, 90],
        'Slytherin': [60, 65, 70]
    }
    assert find_top_house(data) == 'Gryffindor'

def send_post_request(url: str, data: dict, headers: dict = None):
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()  # hata varsa exception fırlatır
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - Status Code: {response.status_code}")
    except Exception as err:
        print(f"Other error occurred: {err}")

class ResultCollector:
    def __init__(self):
        self.passed = 0
        self.failed = 0

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if report.passed:
                self.passed += 1
            elif report.failed:
                self.failed += 1

def run_tests():
    collector = ResultCollector()
    pytest.main(["tests"], plugins=[collector])
    print(f"\nToplam Başarılı: {collector.passed}")
    print(f"Toplam Başarısız: {collector.failed}")
    
    user_score = (collector.passed / (collector.passed + collector.failed)) * 100
    print(round(user_score, 2))
    
    url = "https://kaizu-api-8cd10af40cb3.herokuapp.com/projectLog"
    payload = {
        "user_id": 518,
        "project_id": 634,
        "user_score": round(user_score, 2),
        "is_auto": False
    }
    headers = {
        "Content-Type": "application/json"
    }
    send_post_request(url, payload, headers)

if __name__ == "__main__":
    run_tests()
