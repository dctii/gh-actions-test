# ./.github/actions/docker-action/test.py
import os
import subprocess
from datetime import datetime


# NOTE: Set output via print, works like echo
def set_output(key, val, file):
    print(f"{key}={val}", file=file)


# NOTE: Get input value
def get_input(key):
    return os.environ["INPUT_" + key.upper()]


def get_current_time():
    currentDate = datetime.now()
    return f"{currentDate.strftime('%Y-%m-%d_%Hh-%Mm-%Ss')}"


def run():
    # NOTE: Get input values
    locustfile = get_input("locustfile")
    user_count = get_input("users")
    spawn_rate = get_input("spawn-rate")
    run_time = get_input("run-time")
    curr_time = get_current_time()

    # Locust CLI
    locust_command = f"""
        locust \
          -f {locustfile} \
          --users {user_count} \
          --spawn-rate {spawn_rate} \
          --run-time {run_time} \
          --headless \
          --json \
          --exit-code-on-error 1
        """

    try:
        # NOTE: Run locust
        subprocess.check_call(locust_command, shell=True)
        # #NOTE: Set output of curr time, same as `"key=val" >> $GITHUB_OUTPUT`
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
            set_output(key="CURR_TIME", val=curr_time, file=gh_output)
    except subprocess.CalledProcessError as e:
        print(f"Error running locust: {e}")


if __name__ == "__main__":
    run()
