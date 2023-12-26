from eve.celery import app


@app.task
def update_star_db():
    with open('eve_log.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(f"---------NEW RECORDING---------")

