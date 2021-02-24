import time
from subprocess import run
from datetime import datetime
import numpy as np
import os
import glob
import pandas as pd
import re
import sysinfo


# TODO: Get CPU details - model, drivers, freq, temp
# TODO: Get GPU details - model, drivers, freq, temp
# TODO: Get memory
# TODO: Get HDD Details
# TODO: Use Current directory
# TODO: Make Stress testing mode, basic mode, exhaustive mode, super exhaustive mode, hwbot mode
# TODO: Readme.md with table
# TODO: Steps to setup Blender
# TODO: GPUPi reminders
# TODO: Version independent

# TODO: track CPU temp - https://hemant9807.blogspot.com/2020/11/get-cpu-and-gpu-temp-using-python.html
# TODO: Use MSI Afterburner?
# TODO: Autodownload
# TODO: Config file

# https://stackoverflow.com/questions/13009675/find-all-the-occurrences-of-a-character-in-a-string
# https://stackoverflow.com/questions/4664850/how-to-find-all-occurrences-of-a-substring
def findOccurrences(full_string, sub_str):
    return [m.start() for m in re.finditer(sub_str, full_string)]


def run_benchmark(num_runs, sleep_time, base_dir, bench_path, bench_name, args, out_start, out_end, caching_runs=0,
                  shell_val=False, read_from_file=False, csv_name='benchmarks.csv', split_pos=0, out_start2='',
                  out_end2='', bench_name2='', split_pos2=-1, stdout=True, hms=False, file_dir="results\\",
                  results_dir="results\\", debug=False, occur_val=-1):
    if not os.path.isfile(args[0]):
        print('WARNING: Cannot find file ' + args[0] + ' - Check that benchmark is installed and there are no typos')
        return

    try:
        df = pd.read_csv(base_dir + bench_path + csv_name, index_col=0)

    except:
        # if file does not exist, create it
        dict = {'Run Datetime' : [], 'Benchmark': [], 'Avg Score': [], 'Average Runtime': [], 'Stdev Score': [],
                'Stdev Time'   : [], 'Scores': [], 'Runtimes': [], 'args': [], 'Windows Version': [],
                'Computer Name': []}
        df = pd.DataFrame(dict)

    scores = []
    run_times = []
    scores_two = []
    file_wri_type = 'xb'

    window_version, computer_name = sysinfo.os_details()

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
            list_of_files = glob.glob(
                    base_dir + bench_path + file_dir + "*.txt")  # * means all if need specific format then *.csv
            if debug: print(list_of_files)

            latest_file = max(list_of_files, key=os.path.getmtime)
            run_out = open(latest_file, 'r').read()
            if debug: print(run_out)
            file_wri_type = 'x'

        elif not stdout:
            run_out = str(output)
            file_wri_type = 'x'
            if debug: print(run_out)
        else:
            run_out = output.stdout.decode('UTF-8')
            file_wri_type = 'x'
            if debug: print(run_out)

        if len(out_start2) == 0:
            run_out_search = run_out.replace("\\n", ' ')
            start = findOccurrences(run_out_search, out_start)[occur_val] + len(out_start)
            end = findOccurrences(run_out_search[start:], out_end)[occur_val]

            if hms:
                run_score = run_out_search[start:start + end].split()
                if debug: print(run_score)

                hours = float(re.findall("\d+", run_score[0])[0]) * 60 * 60
                minutes = float(re.findall("\d+", run_score[1])[0]) * 60
                seconds = float(re.findall("\d+", run_score[2])[0]) + float(re.findall("\d+", run_score[2])[1]) / 1000
                run_score = hours + minutes + seconds
            else:
                run_score = run_out_search[start:start + end].split()[split_pos]

            run_score = float(run_score)
            scores.append(run_score)

            bench_name_no_space = bench_name.replace(" ", "")
            with open(base_dir + bench_path + file_dir + bench_name_no_space + "-" + str(i) + "-" + str(
                    now_string) + ".txt",
                      file_wri_type) as f:
                f.write(run_out)
        else:
            run_out_search = run_out.replace("\\n", ' ')
            start = findOccurrences(run_out_search, out_start)[occur_val] + len(out_start)
            end = findOccurrences(run_out_search[start:], out_end)[occur_val]
            run_scores = run_out_search[start:start + end].split()
            scores.append(float(run_scores[split_pos]))

            start = findOccurrences(run_out_search, out_start2)[occur_val] + len(out_start2)
            end = findOccurrences(run_out_search[start:], out_end2)[occur_val]
            run_scores = run_out_search[start:start + end].split()
            scores_two.append(float(run_scores[split_pos2]))

            bench_name_no_space = bench_name.replace(" ", "")

            with open(base_dir + results_dir + bench_name_no_space + "-" + str(i) + "-" + str(
                    now_string) + ".txt",
                      file_wri_type) as f:
                f.write(run_out)

        time.sleep(sleep_time)

    if debug: print(scores)

    avg_score = np.mean(scores)
    std_score = np.std(scores)

    avg_time = np.mean(run_times)
    std_time = np.std(run_times)

    df__new = {'Run Datetime'   : start_runtime, 'Benchmark': bench_name, 'Avg Score': avg_score,
               'Average Runtime': avg_time,
               'Stdev Score'    : std_score, 'Stdev Time': std_time, 'Scores': scores, 'Runtimes': run_times,
               'args'           : args, 'Windows Version': window_version, 'Computer Name': computer_name}
    df = df.append(df__new, ignore_index=True)
    print(bench_name + ' Avg Score:', avg_score, 'Avg Runtime:', avg_time)

    if len(out_start2) > 0:
        if debug: print(scores_two)
        avg_score2 = np.mean(scores_two)
        std_score2 = np.std(scores_two)

        df__new = {'Run Datetime'   : start_runtime, 'Benchmark': bench_name2, 'Avg Score': avg_score2,
                   'Average Runtime': avg_time,
                   'Stdev Score'    : std_score2, 'Stdev Time': std_time, 'Scores': scores_two, 'Runtimes': run_times,
                   'args'           : args, 'Windows Version': window_version, 'Computer Name': computer_name}
        df = df.append(df__new, ignore_index=True)
        print(bench_name2 + ' Avg Score:', avg_score2, 'Avg Runtime:', avg_time)

    df.to_csv(base_dir + bench_path + csv_name)


if __name__ == "__main__":
    base_dir = "C:\\benchmarking_suite\\"
    bench_path = "Benchmarks\\"
    csv_name = 'benchmarks.csv'
    num_runs = 1
    sleep_timer = 0

    # Run Dolphin
    # run_benchmark(num_runs, 5, 'Dolphin', "Dolphin 5.0 CPU Benchmark\\Run benchmark.bat", "", 'CB ', ' (', 0)

    # Run CPUZ
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'CPUZ Single Thread',
                  [base_dir + bench_path + "cpuz\\cpuz_x64.exe", "-bench"],
                  '"', '","', 0, csv_name=csv_name, read_from_file=True, file_dir="cpuz\\",
                  bench_name2='CPUZ Multi Thread',
                  out_start2='","', out_end2='"', split_pos2=0, occur_val=0)

    # GPUPI 3.3.3 100m
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.3.3 100M',
                  [base_dir + bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "100M", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.3.3 1B
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.3.3 1B',
                  [base_dir + bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "1B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.3.3 10B
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.3.3 10B',
                  [base_dir + bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "10B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 100m
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.2 100M',
                  [base_dir + bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "100M", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 1B
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.2 1B',
                  [base_dir + bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "1B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 10B
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'GPUPI 3.2 1B',
                  [base_dir + bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "10B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # Blender CPU barbershop_interior
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU barbershop_interior',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\barbershop_interior\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU classroom
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU classroom',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\classroom\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU fishy_cat
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU fishy_cat',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\fishy_cat\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU BMW27
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU BMW27',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\bmw27\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU koro
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU koro',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\koro\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU pavillon_barcelona
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU pavillon_barcelona',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\pavillon_barcelona\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU victor
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU victor',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\victor\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU BMW27
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Blender CPU BMW27',
                  [base_dir + bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   base_dir + bench_path + "blender_scenes\\bmw27\\main.blend", "--python",
                   base_dir + bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', ' I', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Single Thread 7zip
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, '7zip Compress ST',
                  [base_dir + bench_path + "7-zip\\7z.exe", "b", "1", "-mmt1"],
                  'Avr:', 'Tot:', shell_val=True, csv_name=csv_name, split_pos=2, bench_name2='7zip Decompress ST',
                  out_start2='Avr:', out_end2='Tot:', split_pos2=6)

    # Multi Thread 7zip
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, '7zip Compress MT',
                  [base_dir + bench_path + "7-zip\\7z.exe", "b", "1"],
                  'Avr:', 'Tot:', shell_val=True, csv_name=csv_name, split_pos=2, bench_name2='7zip Decompress MT',
                  out_start2='Avr:', out_end2='Tot:', split_pos2=6)

    # Run y-cruncher 25m Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'y-cruncher 25m Single',
                  [base_dir + bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench",
                   "25m",
                   "-TD:1", "-PF:none", "-o", base_dir + bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 250m Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'y-cruncher 250m Single',
                  [base_dir + bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench",
                   "250m",
                   "-TD:1", "-PF:none", "-o", base_dir + bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 1b Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'y-cruncher 1b Single',
                  [base_dir + bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench",
                   "1b",
                   "-TD:1", "-PF:none", "-o", base_dir + bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 2.5b Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'y-cruncher 2.5b Single',
                  [base_dir + bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench",
                   "2.5b",
                   "-TD:1", "-PF:none", "-o", base_dir + bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 10b Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'y-cruncher 10b Single',
                  [base_dir + bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench",
                   "10b",
                   "-TD:1", "-PF:none", "-o", base_dir + bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run pifast
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'pifast',
                  [base_dir + bench_path + "hexus_pifast\\pifast41.exe",
                   "<" + base_dir + bench_path + "hexus_pifast\\hexus.txt"],
                  'Total computation time : ', ' seconds', shell_val=True, csv_name=csv_name)

    # Run Cinebench R23 Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 23 Single',
                  [base_dir + bench_path + "CinebenchR23\\Cinebench.exe", "-g_CinebenchCpu1Test=true"],
                  'CB ', ' ', csv_name=csv_name)

    # Run Cinebench R23 Multi
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 23 Multi',
                  [base_dir + bench_path + "CinebenchR23\\Cinebench.exe", "-g_CinebenchCpuXTest=true",
                   "-g_CinebenchMinimumTestDuration=1"],
                  'CB ', ' ', csv_name=csv_name)

    # Run Cinebench R11 OpenGL
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 11 OpenGL',
                  [base_dir + bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_opengl"],
                  ': ', ' fps', csv_name=csv_name)

    # Run Cinebench R11 Single
    run_benchmark(num_runs, sleep_timer, 'Cinebench 11 Single',
                  [base_dir + bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_cpu1"],
                  ' : ', ' pts', csv_name=csv_name)

    # Run Cinebench R11 Multi
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 11 Multi',
                  [base_dir + bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  ' : ', ' pts', csv_name=csv_name)

    # Run Cinebench R15 OpenGL
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 OpenGL',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_opengl"],
                  '             : ', ' fps', csv_name=csv_name)

    # Run Cinebench R15 Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 Single',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_cpu1"],
                  ' : ', ' pts', csv_name=csv_name)

    # Run Cinebench R15 Multi
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 Multi',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  ' : ', ' pts', csv_name=csv_name)

    # Run Cinebench R20 Multi
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 20 Multi',
                  [base_dir + bench_path + "CinebenchR20\\Cinebench.exe", "-g_CinebenchCpuXTest=true"],
                  'CB ', ' ', csv_name=csv_name)

    # Run Cinebench R20 Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 20 Single',
                  [base_dir + bench_path + "CinebenchR20\\Cinebench.exe", "-g_CinebenchCpu1Test=true"],
                  'CB ', ' ', csv_name=csv_name)

    # Run Cinebench R15 Extreme OpenGL
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 Extreme OpenGL',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe",
                   "-cb_opengl"],
                  '                : ', ' fps', csv_name=csv_name)

    # Run Cinebench R15 Extreme Single
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 Extreme Single',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe",
                   "-cb_cpu1"],
                  ' : ', ' pts', csv_name=csv_name)

    # Run Cinebench R15 Extreme Multi
    run_benchmark(num_runs, sleep_timer, base_dir, bench_path, 'Cinebench 15 Extreme Multi',
                  [base_dir + bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe",
                   "-cb_cpux"],
                  ' : ', ' pts', csv_name=csv_name)
