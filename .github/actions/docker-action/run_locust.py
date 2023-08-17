# ./.github/actions/docker-action/test.py
import os
import subprocess
from datetime import datetime
from zipfile import ZipFile


def set_output(key, val, file):
    print(f"{key}={val}", file=file)


def get_input(key):
    return os.environ["INPUT_" + key.upper()]


def upload_artifact_with_gh_cli(file_path):
    # Construct the gh command to upload the artifact
    cmd = [
        "gh",
        "run",
        "upload",
        "--repo",
        os.environ["GITHUB_REPOSITORY"],
        "--name",
        "locust-output",
        file_path,
    ]

    # Run the command
    subprocess.run(cmd, check=True)


def get_current_time():
    currentDate = datetime.now()
    return f"{currentDate.strftime('%Y-%m-%d_%Hh-%Mm-%Ss')}"


def run():
    locustfile = get_input("locustfile")
    user_count = get_input("users")
    spawn_rate = get_input("spawn-rate")
    run_time = get_input("run-time")
    curr_time = get_current_time()

    log_dir = "./logfiles"
    html_dir = "./htmlfiles"
    csv_dir = f"./csvfiles/{curr_time}"
    json_dir = f"./jsonfiles/{curr_time}"

    locust_command = (
        "mkdir -p {log_dir} {html_dir} {csv_dir} {json_dir} && "
        "locust "
        "-f {locustfile} "
        "--users {user_count} "
        "--spawn-rate {spawn_rate} "
        "--run-time {run_time} "
        "--headless "
        "--logfile {log_dir}/{curr_time}_mylog.log --loglevel INFO "
        "--html {html_dir}/{curr_time}_myhtml.html "
        "--csv {csv_dir}/{curr_time} --csv-full-history "
        "--json "
        "--exit-code-on-error 1 "
        "--only-summary | awk '/\\[/{{flag=1}} flag; /\\]/{{flag=0; print}}' > {json_dir}/{curr_time}.json"
    ).format(
        log_dir=log_dir,
        html_dir=html_dir,
        csv_dir=csv_dir,
        json_dir=json_dir,
        locustfile=locustfile,
        user_count=user_count,
        spawn_rate=spawn_rate,
        run_time=run_time,
        curr_time=curr_time,
    )

    try:
        subprocess.check_call(locust_command, shell=True)
        with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
            set_output(key="JSON_DIR", val=json_dir, file=gh_output)
            set_output(key="CURR_TIME", val=curr_time, file=gh_output)

        # Compress json output for GitHub artifact upload
        with ZipFile(f"{json_dir}/{curr_time}_output.zip", "w") as zipf:
            zipf.write(f"{json_dir}/{curr_time}.json")

        # Upload the artifact using gh CLI
        upload_artifact_with_gh_cli(f"{json_dir}/{curr_time}_output.zip")

    except subprocess.CalledProcessError as e:
        print(f"Error running locust: {e}")


if __name__ == "__main__":
    run()


# # ./.github/actions/docker-action/test.py
# import os
# import subprocess
# from datetime import datetime
#
#
# def set_output(key, val, file):
#     print(f"{key}={val}", file=file)
#
#
# def get_input(key):
#     return os.environ["INPUT_" + key.upper()]
#
#
# def upload_artifact(file_name, token):
#     headers = {}
#
#
# def get_current_time():
#     currentDate = datetime.now()
#     return f"{currentDate.strftime('%Y-%m-%d_%Hh-%Mm-%Ss')}"
#
#
# def run():
#     locustfile = get_input("locustfile")
#     user_count = get_input("users")
#     spawn_rate = get_input("spawn-rate")
#     run_time = get_input("run-time")
#     curr_time = get_current_time()
#
#     log_dir = "./logfiles"
#     html_dir = "./htmlfiles"
#     csv_dir = f"./csvfiles/{curr_time}"
#     json_dir = f"./jsonfiles/{curr_time}"
#
#     locust_command = f"""
#         mkdir -p {log_dir} {html_dir} {csv_dir} {json_dir}
#         locust \
#           -f {locustfile} \
#           --users {user_count} \
#           --spawn-rate {spawn_rate} \
#           --run-time {run_time} \
#           --headless \
#           --logfile {log_dir}/{curr_time}_mylog.log --loglevel INFO \
#           --html {html_dir}/{curr_time}_myhtml.html \
#           --csv {csv_dir}/{curr_time} --csv-full-history \
#           --json \
#           --exit-code-on-error 1
#         """
#
#     try:
#         subprocess.check_call(locust_command, shell=True)
#         with open(os.environ["GITHUB_OUTPUT"], "a") as gh_output:
#             set_output(key="JSON_DIR", val=json_dir, file=gh_output)
#             set_output(key="CURR_TIME", val=curr_time, file=gh_output)
#     except subprocess.CalledProcessError as e:
#         print(f"Error running locust: {e}")
#
#
# if __name__ == "__main__":
#     run()
