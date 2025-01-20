import json
import time
import gdown
import os

from tabulate import tabulate
from datasketch import HyperLogLog as HyperLogLogDS
from HyperLogLog import HyperLogLog


def count_uniq_ips_set(file_path):
    """
    Підрахунок унікальних IP-адрес за допомогою set.
    """
    unique_ips = set()

    with open(file_path, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                if "remote_addr" in log_entry and log_entry["remote_addr"]:
                    unique_ips.add(log_entry["remote_addr"])
            except json.JSONDecodeError:
                continue

    return len(unique_ips)


def count_uniq_ips_hll(file_path):
    """
    Підрахунок унікальних IP-адрес за допомогою HyperLogLog.
    """
    hll = HyperLogLog(p=14)

    with open(file_path, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                if "remote_addr" in log_entry and log_entry["remote_addr"]:
                    hll.add(log_entry["remote_addr"])
            except json.JSONDecodeError:
                continue

    return hll.count()


def count_uniq_ips_datasketch_hll(file_path):
    """
    Підрахунок унікальних IP-адрес за допомогою HyperLogLog  datasketch.
    """
    hll = HyperLogLogDS(p=14)

    with open(file_path, "r") as file:
        for line in file:
            try:
                log_entry = json.loads(line)
                if "remote_addr" in log_entry and log_entry["remote_addr"]:
                    hll.update(log_entry["remote_addr"].encode("utf-8"))
            except json.JSONDecodeError:
                continue

    return hll.count()


if __name__ == "__main__":
    url = "https://drive.google.com/uc?id=13NUCSG7l_z2B7gYuQubYIpIjJTnwOAOb"
    output = "lms-stage-access.log"
    gdown.download(url, output, quiet=False)
    file_path = "./lms-stage-access.log"

    start_time = time.time()
    result_set = count_uniq_ips_set(file_path)
    result_set_time = time.time() - start_time

    start_time = time.time()
    result_hll = count_uniq_ips_hll(file_path)
    hll_time = time.time() - start_time

    start_time = time.time()
    result_hll_ds = count_uniq_ips_datasketch_hll(file_path)
    result_hll_ds_time = time.time() - start_time

    print(
        tabulate(
            [
                ["Унікальні елементи", f"{result_set}", f"{result_hll}", result_hll_ds],
                [
                    "Час виконання (сек.)",
                    f"{result_set_time}",
                    f"{hll_time}",
                    f"{result_hll_ds_time}",
                ],
            ],
            headers=["", "Точний підрахунок", "HyperLogLog", "HyperLogLog datasketch"],
            tablefmt="grid",
        )
    )
    os.remove(file_path)
