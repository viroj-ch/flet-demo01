from datetime import datetime
import json
from enum import Enum

class SubAccountCode(Enum):
    SA01 = "SA01"
    SA02 = "SA02"
    SA03 = "SA03"
    SA04 = "SA04"
    SA05 = "SA05"

class RuleCode(Enum):
    R0001 = "R0001"
    R0002 = "R0002"
    R0003 = "R0003"
    R0004 = "R0004"
    R0005 = "R0005"
    R0006 = "R0006"
    R0007 = "R0007"
    R0008 = "R0008"
    R0009 = "R0009"

def get_rule_required_fields(rule_id):
    match rule_id:
        case "R0001": return ["start_date", "end_date"]
        case "R0002"| "R0003": return ["start_date", "end_date", "sub_account"]
        case "R0004": return ["start_date", "end_date", "sub_account", "amount"]
        case "R0005": return ["start_date", "end_date", "sub_account", "amount", "number_of_days"]
        case "R0006": return ["start_date", "end_date", "sub_account", "amount", "number_of_days", "times"]
        case "R0007": return ["start_date", "end_date", "sub_account", "amount", "times"]
        case "R0008": return ["start_date", "end_date", "amount"]
        case "R0009": return ["start_date", "end_date", "amount", "times"]
        case _: raise KeyError(f"No match for rule_id={rule_id}")

def validate_fields(data, required_fields):
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return False, f"Missing fields: {', '.join(missing_fields)}"
    return True, "All required fields are present."

def gen_sql_argument_value(data):
    mydict={"sql_argument": {"params": []}}
    for key, value in data.items():
        new_param = {"name": key, "value": value}
        mydict["sql_argument"]["params"].append(new_param)
    return mydict

def yyyymmdd_to_date_string_with_time(date_string):
    # Convert to datetime object
    date_object = datetime.strptime(date_string, "%Y%m%d")

    # Convert back to string with time in desired format
    date_string_with_time = date_object.strftime("%Y-%m-%d %H:%M:%S")
    return date_string_with_time

def gen_insert_sql(data):
    submission_id = data.get('submission_id')
    rule_id=data.get('rule_id')
    bzb_mission_id=data.get('bzb_mission_id')
    start_date=yyyymmdd_to_date_string_with_time(data.get('sql_argument_value').get('start_date'))
    end_date=yyyymmdd_to_date_string_with_time(data.get('sql_argument_value').get('end_date'))
    sql_argument = json.dumps(data.get('sql_argument'))

    sql = f"""INSERT INTO t_submission (submission_id, rule_id, sql_argument, bzb_mission_id, start_date, end_date, create_datetime, modify_datetime, del) VALUES ('{submission_id}', '{rule_id}', '{sql_argument}', '{bzb_mission_id}', '{start_date}', '{end_date}', now(), now(), 0);"""
    return sql

def processing(data):
    required_fields = get_rule_required_fields(data.get('rule_id'))
    is_valid, message = validate_fields(data.get('sql_argument_value'), required_fields)
    if is_valid:
        sql_argument = gen_sql_argument_value(data.get('sql_argument_value'))
        data['sql_argument']= sql_argument
        sql = gen_insert_sql(data)
        return sql
    else:
        print(message)   # Output: Missing fields: times

class SubmissionSQL():
    def __init__(self, data):
        required_fields = get_rule_required_fields(data.get('rule_id'))
        is_valid, message = validate_fields(data.get('sql_argument_value'), required_fields)
        if is_valid:
            sql_argument = gen_sql_argument_value(data.get('sql_argument_value'))
            data['sql_argument']= sql_argument
            self.sql = gen_insert_sql(data)
        else:
            self.sql = message
            # print(message)   # Output: Missing fields: times

    def get_value(self):
        return self.sql

def main():
    data = {
        "submission_id": "test_vcp",
        "rule_id": RuleCode.R0004.value,
        "bzb_mission_id": "",
        "sql_argument_value": {
            "start_date": "20230101",
            "end_date": "20230131",
            "sub_account": SubAccountCode.SA02.value,
            "amount": 1000,
            # "number_of_days": 0,
            # "times": 0,
        }
    }
    sql = processing(data)
    print(sql)

if __name__ == "__main__":
    main()