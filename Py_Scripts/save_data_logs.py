from Py_Scripts.DataLogger import DataLogger

def save_data_logs(session, error_dict):
    try:
        error = DataLogger(
            files=error_dict['filename'],
            logs=error_dict['errors']
        )
        session.add(error)

        session.commit()
        session.close()

        return {"status": 200}
    except Exception as e:
        print(e.args)
        return {"status": 500}
