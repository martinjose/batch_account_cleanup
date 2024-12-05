import os
from contextlib import redirect_stderr, redirect_stdout
from datetime import datetime
from pathlib import Path
from typing import Literal, TypeAlias

dir_env_var = os.getenv("AYA_BATCH_LOG_DIR")
file_env_var = os.getenv("AYA_BATCH_LOG_FILE")
workdir_env_var = os.getenv("AYA_BATCH_WORKDIR")

log_dir = Path(dir_env_var)
log_file = Path(log_dir, file_env_var)
batch_workdir = Path(workdir_env_var)

LogSeverity: TypeAlias = Literal["info", "error"]


def log(severity: LogSeverity, message):
    timestamp = datetime.now().strftime("%Y-%m-%d T %H:%M:%S.%f")
    print(f"[{severity}] {timestamp}: {str(message)}")


def cleanup(wd):
    wd_ls = os.listdir(wd)

    for file in wd_ls:
        subject_dir = Path(wd, file)
        m_date = datetime.fromtimestamp(os.path.getmtime(subject_dir))
        delta = datetime.now() - m_date
        if delta.days > 5:
            try:
                os.removedirs(subject_dir)
            except BaseException as e:
                log(
                    "info",
                    f"Encountered error purging: {subject_dir}",
                )
                log("error", e)


if __name__ == "__main__":
    # log_dir = Path("/mnt/aya_batch_cleanup/")
    # log_file = Path(log_dir, "aya_batch_cleanup.log")
    # batch_workdir = Path("/mnt/batch/tasks/workitems/adfv2-opssandwusba1-pool/job-1")

    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    with open(log_file, "a") as lf, redirect_stderr(lf), redirect_stdout(lf):
        cleanup(Path(os.path.realpath(__file__), "TestDir"))
