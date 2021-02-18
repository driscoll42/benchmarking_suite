import time
from subprocess import run
from datetime import datetime
import numpy as np
import os
import glob
import pandas as pd
import re


# TODO: Get CPU, GPU, Windows Version, drivers (look at R20) https://www.thepythoncode.com/article/get-hardware-system-information-python
# TODO: track CPU temp - https://hemant9807.blogspot.com/2020/11/get-cpu-and-gpu-temp-using-python.html
# TODO: Use MSI Afterburner?
# TODO: y-cruncher multi - I think it's a my CPU issue
# TODO: Readme.md with table
# TODO: Version independent
# TODO: Autodownload
# TODO: Steps to setup Blender
# TODO: GPUPi reminders
# TODO: Make Stress testing mode, basic mode, exhaustive mode, super exhaustive mode
# TODO: Config file
# TODO: Use Current directory

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
            # print(run_out)
        elif not stdout:
            run_out = str(output)
        else:
            run_out = output.stdout.decode('UTF-8')
            # print(run_out)

        if len(out_start2) == 0:
            start = run_out.rfind(out_start) + len(out_start)
            end = run_out[start:].find(out_end)

            if hms:
                run_score = run_out[start:start + end].split()

                hours = float(re.findall("\d+", run_score[0])[0]) * 60 * 60
                minutes = float(re.findall("\d+", run_score[1])[0]) * 60
                seconds = float(re.findall("\d+", run_score[2])[0]) + float(re.findall("\d+", run_score[2])[1])/1000
                run_score = hours + minutes + seconds
            else:
                run_score = run_out[start:start + end].split()[split_pos]


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
    bench_path = "C:\\benchmarking_suite\\Benchmarks\\"
    csv_name = 'benchmarks.csv'
    num_runs = 1
    sleep_timer = 0

    # Run Dolphin
    # run_benchmark(num_runs, 5, 'Dolphin', "Dolphin 5.0 CPU Benchmark\\Run benchmark.bat", "", 'CB ', ' (', 0)


    # Run Cinebench R15 Extreme Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Extreme Multi',
                  [bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  'Rendering (Multiple CPU) : ', ' pts', 0, csv_name=csv_name)


    # GPUPI 3.3.3 100m
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.3.3 100M',
                  [bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "100M", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.3.3 1B
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.3.3 1B',
                  [bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "1B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.3.3 1B
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.3.3 10B',
                  [bench_path + "GPUPI 3.3.3\\GPUPI-CLI.exe", "-d", "10B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 100m
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.2 100M',
                  [bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "100M", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 1B
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.2 1B',
                  [bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "1B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # GPUPI 3.2 1B
    run_benchmark(num_runs, sleep_timer, 'GPUPI 3.2 1B',
                  [bench_path + "GPUPI 3.2\\GPUPI-CLI.exe", "-d", "10B", "-c"],
                  'finished.', ' PI value output', 0, csv_name=csv_name, hms=True)

    # Blender CPU barbershop_interior
    run_benchmark(num_runs, sleep_timer, 'Blender CPU barbershop_interior',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\barbershop_interior\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)


    # Blender CPU classroom
    run_benchmark(num_runs, sleep_timer, 'Blender CPU classroom',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\classroom\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU fishy_cat
    run_benchmark(num_runs, sleep_timer, 'Blender CPU fishy_cat',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\fishy_cat\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU BMW27
    run_benchmark(num_runs, sleep_timer, 'Blender CPU BMW27',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\bmw27\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU koro
    run_benchmark(num_runs, sleep_timer, 'Blender CPU koro',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\koro\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU pavillon_barcelona
    run_benchmark(num_runs, sleep_timer, 'Blender CPU pavillon_barcelona',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\pavillon_barcelona\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Blender CPU victor
    run_benchmark(num_runs, sleep_timer, 'Blender CPU victor',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\victor\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)


    # Blender CPU BMW27
    run_benchmark(num_runs, sleep_timer, 'Blender CPU BMW27',
                  [bench_path + "blender-2.91.2-windows64\\blender.exe", "--background", "--factory-startup",
                   "-noaudio",
                   "--debug-cycles", "--enable-autoexec", "--engine", "CYCLES",
                   bench_path + "blender_scenes\\bmw27\\main.blend", "--python",
                   bench_path + "blender-benchmark-script-2.0.0\\main.py", "--", "--device-type", "CPU"]
                  , 'Total render time:', '\\n', shell_val=True, csv_name=csv_name, split_pos=0, stdout=False)

    # Single Thread 7zip
    run_benchmark(num_runs, sleep_timer, '7zip Compress ST',
                  [bench_path + "7-zip\\7z.exe", "b", "1", "-mmt1"],
                  'Avr:', 'Tot:', shell_val=True, csv_name=csv_name, split_pos=2, bench_name2='7zip Decompress ST',
                  out_start2='Avr:', out_end2='Tot:', split_pos2=6)

    # Multi Thread 7zip
    run_benchmark(num_runs, sleep_timer, '7zip Compress MT',
                  [bench_path + "7-zip\\7z.exe", "b", "1"],
                  'Avr:', 'Tot:', shell_val=True, csv_name=csv_name, split_pos=2, bench_name2='7zip Decompress MT',
                  out_start2='Avr:', out_end2='Tot:', split_pos2=6)

    # Run y-cruncher 25m Single
    run_benchmark(num_runs, sleep_timer, 'y-cruncher 25m Single',
                  [bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench", "25m",
                   "-TD:1", "-PF:none", "-o", bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 1b Single
    run_benchmark(num_runs, sleep_timer, 'y-cruncher 250m Single',
                  [bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench", "250m",
                   "-TD:1", "-PF:none", "-o", bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 1b Single
    run_benchmark(num_runs, sleep_timer, 'y-cruncher 1b Single',
                  [bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench", "1b",
                   "-TD:1", "-PF:none", "-o", bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 2.5b Single
    run_benchmark(num_runs, sleep_timer, 'y-cruncher 2.5b Single',
                  [bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench", "2.5b",
                   "-TD:1", "-PF:none", "-o", bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run y-cruncher 10b Single
    run_benchmark(num_runs, sleep_timer, 'y-cruncher 10b Single',
                  [bench_path + "y-cruncher v0.7.8.9507\\y-cruncher.exe", "colors:0", "priority:2", "bench", "10b",
                   "-TD:1", "-PF:none", "-o", bench_path + "Results", "-od:0"],
                  'Total Computation Time: ', ' seconds', shell_val=True, read_from_file=True, csv_name=csv_name)

    # Run pifast
    run_benchmark(num_runs, sleep_timer, 'pifast',
                  [bench_path + "hexus_pifast\\pifast41.exe", "<" + bench_path + "hexus_pifast\\hexus.txt"],
                  'Total computation time : ', ' seconds', shell_val=True, csv_name=csv_name)

    # Run Cinebench R23 Single
    run_benchmark(num_runs, sleep_timer, 'Cinebench 23 Single',
                  [bench_path + "CinebenchR23\\Cinebench.exe", "-g_CinebenchCpu1Test=true"],
                  'CB ', ' (', 0, csv_name=csv_name)

    # Run Cinebench R23 Multi
    run_benchmark(num_runs, 0, 'Cinebench 23 Multi',
                  [bench_path + "CinebenchR23\\Cinebench.exe", "-g_CinebenchCpuXTest=true",
                   "-g_CinebenchMinimumTestDuration=1"],
                  'CB ', ' (', 0, csv_name=csv_name)

    # Run Cinebench R11 OpenGL
    run_benchmark(num_runs, sleep_timer, 'Cinebench 11 OpenGL',
                  [bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_opengl"],
                  'Shading (OpenGL)                : ', ' fps', 0, csv_name=csv_name)

    # Run Cinebench R11 Single
    run_benchmark(num_runs, sleep_timer, 'Cinebench 11 Single',
                  [bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_cpu1"],
                  'Rendering (Single   CPU) : ', ' pts', 0, csv_name=csv_name)

    # Run Cinebench R11 Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 11 Multi',
                  [bench_path + "CINEBENCH_11.529\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  'Rendering (Multiple CPU) : ', ' pts', 0, csv_name=csv_name)

    # Run Cinebench R15 OpenGL
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 OpenGL',
                  [bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_opengl"],
                  'Shading (OpenGL)                : ', ' fps', 0, csv_name=csv_name)

    # Run Cinebench R15 Single
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Single',
                  [bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_cpu1"],
                  'Rendering (Single   CPU) : ', ' pts', 0, csv_name=csv_name)

    # Run Cinebench R15 Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Multi',
                  [bench_path + "CINEBENCH R15.038_RC184115\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  'Rendering (Multiple CPU) : ', ' pts', 0, csv_name=csv_name)

    # Run Cinebench R20 Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 20 Multi',
                  [bench_path + "CinebenchR20\\Cinebench.exe", "-g_CinebenchCpuXTest=true"],
                  'CB ', ' (', 0, csv_name=csv_name)

    # Run Cinebench R20 Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 20 Single',
                  [bench_path + "CinebenchR20\\Cinebench.exe", "-g_CinebenchCpu1Test=true"],
                  'CB ', ' (', 0, csv_name=csv_name)


    # Run Cinebench R15 Extreme OpenGL
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Extreme OpenGL',
                  [bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe", "-cb_opengl"],
                  'Shading (OpenGL)                : ', ' fps', 0, csv_name=csv_name)

    # Run Cinebench R15 Extreme Single
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Extreme Single',
                  [bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe", "-cb_cpu1"],
                  'Rendering (Single   CPU) : ', ' pts', 0, csv_name=csv_name)

    # Run Cinebench R15 Extreme Multi
    run_benchmark(num_runs, sleep_timer, 'Cinebench 15 Extreme Multi',
                  [bench_path + "CINEBENCH R15.038_RC184115_Extreme\\CINEBENCH Windows 64 Bit.exe", "-cb_cpux"],
                  'Rendering (Multiple CPU) : ', ' pts', 0, csv_name=csv_name)