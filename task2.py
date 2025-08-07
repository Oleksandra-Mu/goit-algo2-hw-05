from datasketch import HyperLogLog
import json
import time


def ip_addresses(path):
    ip_list = []

    with open(path, "r", encoding="utf-8") as file:
        for row in file:
            try:
                data = json.loads(row)
                for key in ["remote_addr"]:
                    ip = data.get(key, "")
                    if ip:
                        ip_list.append(ip.encode("utf-8"))
                        break

            except json.JSONDecodeError:
                continue

    return ip_list


def count_unique_ip_addresses_set(ip_list):
    ip_set = set(ip_list)
    return len(ip_set)


def count_unique_ip_addresses_hll(ip_list):
    hll = HyperLogLog(p=14)
    for ip in ip_list:
        hll.update(ip)
    return hll.count()


def run_with_timing(func, *args, **kwargs):
    start = time.perf_counter()
    result = func(*args, **kwargs)
    end = time.perf_counter()
    elapsed = end - start
    return result, elapsed


def main():
    path = "lms-stage-access.log"
    ip_list = ip_addresses(path)
    exact_count, time_exact = run_with_timing(count_unique_ip_addresses_set, ip_list)
    hll_count, time_hll = run_with_timing(count_unique_ip_addresses_hll, ip_list)

    print("Результати порівняння:")
    print(f"{'':<30} {'Точний підрахунок':<20} {'HyperLogLog':<20}")
    print(f"{'Унікальні елементи':<30} {exact_count:<20} {hll_count:<20}")
    print(f"{'Час виконання (сек.)':<30} {time_exact:<20.4f} {time_hll:<20.4f}")


if __name__ == "__main__":
    main()
