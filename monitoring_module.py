# monitoring_module.py

import logging
import time
import threading
import os
import sys

def setup_logger():
    logger = logging.getLogger('MonitoringModule')
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('monitoring_module.log')
    fh.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)
    return logger

logger = setup_logger()

class JobMonitor:
    def __init__(self):
        self.job_active = False
        self.progress = 0
        self.total_steps = 100  # Example total steps
        self.lock = threading.Lock()

    def start_job(self):
        with self.lock:
            self.job_active = True
            self.progress = 0
            logger.info("Job started.")

    def update_progress(self, steps=1):
        with self.lock:
            if self.job_active:
                self.progress += steps
                percent_complete = (self.progress / self.total_steps) * 100
                logger.info(f"Job progress: {percent_complete:.2f}%")
                if self.progress >= self.total_steps:
                    self.complete_job()

    def complete_job(self):
        with self.lock:
            self.job_active = False
            logger.info("Job completed successfully.")

    def abort_job(self):
        with self.lock:
            if self.job_active:
                self.job_active = False
                logger.warning("Job aborted.")

    def is_job_active(self):
        with self.lock:
            return self.job_active

def monitor_job(job_monitor):
    while job_monitor.is_job_active():
        job_monitor.update_progress()
        time.sleep(1)  # Simulate time between steps

def main():
    job_monitor = JobMonitor()
    try:
        job_monitor.start_job()
        monitor_thread = threading.Thread(target=monitor_job, args=(job_monitor,))
        monitor_thread.start()
        monitor_thread.join()
    except KeyboardInterrupt:
        logger.warning("Monitoring interrupted by user.")
        job_monitor.abort_job()
        sys.exit(1)
    except Exception as e:
        logger.exception("An error occurred in the monitoring module.")
        job_monitor.abort_job()
        sys.exit(1)

if __name__ == '__main__':
    main()
