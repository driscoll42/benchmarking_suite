import time
from subprocess import run
from datetime import datetime
import numpy as np
import os
import glob
import pandas as pd
import re

# TODO: track CPU temp - https://hemant9807.blogspot.com/2020/11/get-cpu-and-gpu-temp-using-python.html
# TODO: Use MSI Afterburner?
# TODO: y-cruncher multi - I think it's a my CPU issue
# TODO: Readme.md with table
# TODO: Version independent
# TODO: Autodownload
# TODO: Steps to setup Blender
# TODO: Get CPU, GPU, Windows Version, drivers (look at R20) https://www.thepythoncode.com/article/get-hardware-system-information-python

def run_benchmark(num_runs, sleep_time, bench_name, args, out_start, out_end, caching_runs=0,
                  shell_val=False, read_from_file=False, csv_name='benchmarks.csv', split_pos=0, out_start2='',
                  out_end2='', bench_name2='', split_pos2=-1, stdout=True, hms=False):
    if not os.path.isfile(args[0]):
        print('WARNING: Cannot find file ' + args[0] + ' - Check that benchmark is installed and there are no typos')
        return

    try:
        df = pd.read_csv(bench_path + csv_name, index_col=0)

    except:
        # if file does not exist, create it
        dict = {'Run Datetime': [], 'Benchmark': [], 'Avg Score': [], 'Average Runtime': [], 'Stdev Score': [],
                'Stdev Time'  : [], 'Scores': [], 'Runtimes': [], 'args': []}
        df = pd.DataFrame(dict)

    scores = []
    run_times = []
    scores_two = []

    start_runtime = datetime.now()

    if caching_runs > 0:
        for i in range(caching_runs):
            run(args, capture_output=True, check=True)
        time.sleep(sleep_time)

    for i in range(num_runs):
        now = datetime.now()
        print('Running ' + bench_name + ' - run: ', i)

        start_run_time = time.perf_counter()
        output = run(args, capture_output=True, check=True, shell=shell_val)

        end_run_time = time.perf_counter()
        run_times.append(end_run_time - start_run_time)

        now_string = now.strftime('%y%m%d_%I%M%S%f')

        if read_from_file:
            list_of_files = glob.glob(bench_path + "Results\\*")  # * means all if need specific format then *.csv
            latest_file = max(list_of_files, key=os.path.getctime)
            run_out = open(latest_file, 'r').read()
        elif not stdout:
            run_out = str(output)
        else:
            run_out = output.stdout.decode('UTF-8')
            # print(run_out)

        if len(out_start2) == 0:
            start = run_out.rfind(out_start) + len(out_start)
            end = run_out[start:].find(out_end)
            print(run_out[start:start + end])
            print(run_out[start:start + end].split())
            if hms:
                run_score = run_out[start:start + end].split()
                hours = float(re.findall("\d+", run_score[0])[0]) * 60 * 60
                minutes = float(re.findall("\d+", run_score[1])[0]) * 60
                print(re.findall("\d+", run_score[2]))
                seconds = float(re.findall("\d+", run_score[2])[0]) + float(re.findall("\d+", run_score[2])[1])/1000
                print(seconds)
                run_score = hours + minutes + seconds
            else:
                run_score = run_out[start:start + end].split()[split_pos]
            print(run_score)
            run_score = float(run_score)
            scores.append(run_score)

            bench_name_no_space = bench_name.replace(" ", "")
            with open(bench_path + "Results\\" + bench_name_no_space + "-" + str(i) + "-" + str(now_string) + ".txt",
                      'xb') as f:
                f.write(output.stdout)
        else:
            start = run_out.find(out_start) + len(out_start)
            end = run_out[start:].find(out_end)
            run_scores = run_out[start:start + end].split()
            scores.append(float(run_scores[split_pos]))

            start = run_out.find(out_start2) + len(out_start2)
            end = run_out[start:].find(out_end2)
            run_scores = run_out[start:start + end].split()
            scores_two.append(float(run_scores[split_pos2]))

            bench_name_no_space = bench_name.replace(" ", "")
            with open(bench_path + "Results\\" + bench_name_no_space + "-" + str(i) + "-" + str(now_string) + ".txt",
                      'xb') as f:
                f.write(output.stdout)

        time.sleep(sleep_time)

    avg_score = np.mean(scores)
    std_score = np.std(scores)

    avg_time = np.mean(run_times)
    std_time = np.std(run_times)

    df__new = {'Run Datetime'   : start_runtime, 'Benchmark': bench_name, 'Avg Score': avg_score,
               'Average Runtime': avg_time,
               'Stdev Score'    : std_score, 'Stdev Time': std_time, 'Scores': scores, 'Runtimes': run_times,
               'args'           : args}
    df = df.append(df__new, ignore_index=True)

    if len(out_start2) > 0:
        avg_score2 = np.mean(scores_two)
        std_score2 = np.std(scores_two)

        df__new = {'Run Datetime'   : start_runtime, 'Benchmark': bench_name2, 'Avg Score': avg_score2,
                   'Average Runtime': avg_time,
                   'Stdev Score'    : std_score2, 'Stdev Time': std_time, 'Scores': scores_two, 'Runtimes': run_times,
                   'args'           : args}
        df = df.append(df__new, ignore_index=True)

    df.to_csv(bench_path + csv_name)

    print('Avg Score:', avg_score, 'Avg Runtime:', avg_time)


if __name__ == "__main__":
    bench_path = "C:\\Benchmarks\\"
    csv_name = 'benchmarks.csv'
    num_runs = 1
    sleep_timer = 0


    # GPUPI 100m
    run_benchmark(num_runs, sleep_timer, 'GPUPI 100M',
                  [bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "100M", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 1B
    run_benchmark(num_runs, sleep_timer, 'GPUPI 1B',
                  [bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "1B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)