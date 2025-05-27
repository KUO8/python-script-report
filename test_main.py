import pytest
import os
from main import read_csv_file, calculate_payout_data, generate_payout_report

@pytest.fixture
def sample_data():
    return [
        {"name": "Alice", "department": "Marketing", "hours_worked": "160", "hourly_rate": "50"},
        {"name": "Bob", "department": "Design", "hours_worked": "150", "hourly_rate": "40"},
        {"name": "Carol", "department": "Design", "hours_worked": "170", "hourly_rate": "60"}
    ]

@pytest.fixture
def temp_csv(tmp_path, sample_data):
    file_path = os.path.join(tmp_path, "test.csv")
    with open(file_path, 'w') as f:
        f.write("name,department,hours_worked,hourly_rate\n")
        for row in sample_data:
            f.write(f"{row['name']},{row['department']},{row['hours_worked']},{row['hourly_rate']}\n")
    return file_path

def test_read_csv_file(temp_csv):
    data = read_csv_file(temp_csv)
    assert len(data) == 3
    assert data[0]['name'] == 'Alice'
    assert data[1]['department'] == 'Design'
    assert data[2]['hourly_rate'] == '60'

def test_calculate_payout_data(sample_data):
    result = calculate_payout_data(sample_data)
    
    assert 'Marketing' in result
    assert 'Design' in result
    
    assert len(result['Marketing']['employees']) == 1
    assert result['Marketing']['total_hours'] == 160
    assert result['Marketing']['total_payout'] == 8000
    
    assert len(result['Design']['employees']) == 2
    assert result['Design']['total_hours'] == 320
    assert result['Design']['total_payout'] == 16200

def test_generate_payout_report(sample_data):
    report = generate_payout_report(sample_data)
    lines = report.split('\n')
    
    assert "\t\tname      hours      rate       payout" in lines[0]
    
    assert "Marketing" in lines[1]
    assert "--------- Alice            160        50         $8000" in lines[2]
    assert "                           160                   $8000" in lines[3]
    
    assert "Design" in lines[5]
    assert "--------- Bob              150        40         $6000" in lines[6]
    assert "--------- Carol            170        60         $10200" in lines[7]
    assert "                           320                   $16200" in lines[8]

def test_main_integration(temp_csv, capsys):
    import main
    import sys
    
    sys.argv = ['main.py', temp_csv, '--report', 'payout']
    main.main()
    
    captured = capsys.readouterr()
    assert "\t\tname      hours      rate       payout" in captured.out
    assert "--------- Alice            160        50         $8000" in captured.out
    assert "--------- Bob              150        40         $6000" in captured.out