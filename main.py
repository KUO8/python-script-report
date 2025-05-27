import argparse
from collections import defaultdict
from typing import List, Dict, Any

def read_csv_file(file_path: str) -> List[Dict[str, Any]]:
    data = []
    with open(file_path, 'r') as f:
        headers = f.readline().strip().split(',')
        for line in f:
            values = line.strip().split(',')
            row = dict(zip(headers, values))
            data.append(row)
    return data

def calculate_payout_data(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    departments = defaultdict(lambda: {'employees': [], 'total_hours': 0,
                                        'total_payout': 0})
    for row in data:
        department = row['department']
        name = row['name']
        hours = int(row['hours_worked'])
        rate = int(row['hourly_rate'])
        payout = hours * rate
        
        departments[department]['employees'].append({
            'name': name,
            'hours': hours,
            'rate': rate,
            'payout': payout
        })
        departments[department]['total_hours'] += hours
        departments[department]['total_payout'] += payout
    return dict(departments)

def generate_payout_report(data: List[Dict[str, Any]]) -> str:
    departments = calculate_payout_data(data)
    report_lines = []
    
    report_lines.append(f"{'\t\tname'.ljust(11)} {'hours'.
                            ljust(10)} {'rate'.ljust(10)} {'payout'}")
    
    for dept, data in departments.items():
        report_lines.append(f"{dept}")
        
        for emp in data['employees']:
            report_lines.append(
                f"--------- {emp['name'].ljust(16)} {str(emp['hours']).
                    ljust(10)} {str(emp['rate']).ljust(10)} ${emp['payout']}"
            )
        
        report_lines.append(f"{'  '.ljust(26)} {str(data['total_hours']).
                                ljust(10)} {' '.ljust(10)} ${data['total_payout']}")
        
        report_lines.append("")
    
    return "\n".join(report_lines)

REPORTS = {
    'payout': generate_payout_report,
}

def main():
    parser = argparse.ArgumentParser(description='Generate reports from employee data.')
    parser.add_argument('files', metavar='FILE', type=str, nargs='+',
                      help='CSV files containing employee data')
    parser.add_argument('--report', type=str, required=True,
                      choices=REPORTS.keys(), help='Type of report to generate')
    args = parser.parse_args()

    all_data = []
    for file_path in args.files:
        all_data.extend(read_csv_file(file_path))

    report_func = REPORTS[args.report]
    print(report_func(all_data))

if __name__ == "__main__":
    main()