import re


def read_log_file(file_path):
    with open(file_path, "r") as file:
        return file.read()


def parse_siege_logs(log_data):
    # Split log entries based on the pattern of each "****"
    log_entries = log_data.strip().split("****")

    parsed_logs = []

    for entry in log_entries:
        if not entry.strip():
            continue

        # Extract c, d, r values
        match = re.search(r"=c=(\d+),\s+d=(\d+),\s+r=(\d+)", entry)
        if match:
            c, d, r = match.groups()

        fields = entry.split(",")
        if len(fields) > 3:
            timestamp = fields[0].strip()
            transactions = int(fields[1].strip())
            elapsed_time = float(fields[2].strip())
            data_transferred = float(fields[3].strip())
            response_time = float(fields[4].strip())
            transaction_rate = float(fields[5].strip())
            throughput = float(fields[6].strip())
            concurrency = float(fields[7].strip())
            successful_transactions = int(fields[8].strip())
            failed_transactions = int(fields[9].strip())

            log_entry = {
                "timestamp": timestamp,
                "c": int(c),
                "d": int(d),
                "r": int(r),
                "transactions": int(transactions),
                "elapsed_time": float(elapsed_time),
                "data_transferred": float(data_transferred),
                "response_time": float(response_time),
                "transaction_rate": float(transaction_rate),
                "throughput": float(throughput),
                "concurrency": float(concurrency),
                "successful_transactions": int(successful_transactions),
                "failed_transactions": int(failed_transactions),
            }

            parsed_logs.append(log_entry)

    return parsed_logs
