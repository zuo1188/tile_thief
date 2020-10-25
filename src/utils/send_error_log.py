from datetime import datetime

def send_error_log(worker_dict, error_str):
    now = datetime.now()
    datestr = now.strftime("%m/%d/%Y, %H:%M:%S")
    error_message = datestr + ' '+ error_str
    worker_dict["error_message"] = worker_dict["error_message"] + [error_message]
    worker_dict["progress_value"] = -1