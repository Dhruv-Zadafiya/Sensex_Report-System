import time
import schedule
import logging

logger = logging.getLogger(__name__)

def start_scheduler(job_func, interval_minutes=None, daily_time="15:30"):
    """
    Sets up the scheduling framework and runs a loop to invoke the stock market updates.
    
    :param job_func: The callable task to run (the main app pipeline).
    :param interval_minutes: Optional. Runs the job every N minutes (useful for testing/demo).
    :param daily_time: Standard daily execution time (default: 15:30 SENSEX close).
    """
    schedule.clear()
    
    if interval_minutes:
        logger.info(f"Scheduling updater job to run every {interval_minutes} minute(s) for testing/demo.")
        schedule.every(interval_minutes).minutes.do(job_func)
    else:
        logger.info(f"Scheduling updater job to run daily at {daily_time} (market close).")
        schedule.every().day.at(daily_time).do(job_func)
        
    logger.info("Scheduler background loop started. Press Ctrl+C to terminate.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("Scheduler background loop stopped by user.")
    except Exception as e:
        logger.critical(f"Scheduler loop encountered a fatal exception: {e}")
