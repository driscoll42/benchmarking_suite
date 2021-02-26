# WARNING: Use at your own risk. This suite will run a number of benchmarks on your computer and could potentially damge it, especially if you're overclocked. Read what this does carefully and run the tests you mean to run.


# Python Based Benchmarking Suite

This is a benchmarking suite to automate running various benchmarks on your machine using their CLI interfaces including the following features:

* Run benchmarking multiple times and compute average + standard deviation
* Wait a certain amount of time between benchmarks
* Discard initial runs to cache data
* Wait for CPU temperature/load to drop below a threshold before running (TODO)
* Store output into csv for future reference
* Extract OS, CPU, GPU, driver versions and other system data on each run

Note: This repo does not contain any of the benchmarks inherently as I do not have permission to share them. Please see the Install instructions below for how to set up the benchmarks

Note: Currently only supports Windows-based CPU benchmarks

Note: I have only tested this on my personal computers, if bugs are found please report them!

# CPU Benchmarks

### Implemented CPU Benchmarks

| Benchmark  | Description | Official CLI Documentation | Unofficial CLI Documentation | Notes
| --------  | ------------------- |------------------- | --------------------- | --------------------- |
[Cinebench R11.5](https://www.guru3d.com/files-details/cinebench-11-5.html) | | |		[Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/) |
[Cinebench R15](https://www.techspot.com/downloads/6709-cinebench.html) | | |		[Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)
[Cinebench R15 Extreme](https://www.guru3d.com/files-details/cinebench-r15-extreme-edition-download.html) | | | [Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)			
[Cinebench R20](https://www.techspot.com/downloads/6709-cinebench.html) | | |		[Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)
[Cinebench R23](https://www.maxon.net/en/downloads) | |	[Link](https://www.maxon.net/en/cinebench) | [Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)
[Pi Fast](https://hwbot.org/benchmark/pifast/) |	|| | Not really CLI, loads file	
[y-cruncher](http://www.numberworld.org/y-cruncher/) | |	Download zip and open "Command Lines.txt"		
[Blender](https://opendata.blender.org/) | |	[Link](https://opendata.blender.org/about/)	
[7 Zip](https://www.7-zip.org/) | |	[Link](	https://documentation.help/7-Zip/bench.htm)	
[GPUPI 3.3.3](https://www.overclockers.at/news/gpupi-international-support-thread) | |	[Link](https://www.overclockers.at/news/gpupi-3-is-now-official)	
[GPUPI 3.2](https://www.overclockers.at/news/gpupi-international-support-thread) | |		[Link](https://www.overclockers.at/news/gpupi-3-is-now-official)
[CPU-Z](https://www.cpuid.com/softwares/cpu-z.html) | | Download zip and open "cpuz_readme.txt"

### Unsupported CPU Benchmarks
| Benchmark  |  Reason for Lack of Support | CLI Documentation
| --------  |  --------------------- | --------------------- |
[HWBot x265](https://hwbot.org/benchmark/hwbot_x265_benchmark_-_1080p/) |	No CLI Interface
[HWBOT Prime](https://hwbot.org/benchmark/hwbot_prime/) |No CLI Interface
[Super Pi](http://www.superpi.net/) | No CLI Interface
[Corona 1.3](https://blog.corona-renderer.com/corona-1-3-benchmark/) | No CLI Interface (Anandtech has a special version with CLI)
[XTU](https://downloadcenter.intel.com/download/29183/Intel-Extreme-Tuning-Utility-Intel-XTU-)|Not supported on AMD CPUs
[Geekbench 3](https://www.geekbench.com/geekbench3/)| Requires Pro License for CLI | [Link](http://support.primatelabs.com/kb/geekbench/geekbench-3-command-line-tool)
[Geekbench 4](https://www.geekbench.com/geekbench4/) | Requires Pro License for CLI | [Link](http://support.primatelabs.com/kb/geekbench/geekbench-4-pro-command-line-tool)
[Geekbench 5](https://www.geekbench.com/)	| Requires Pro License for CLI | [Link](http://support.primatelabs.com/kb/geekbench/geekbench-5-pro-command-line-tool)
[SPEC 2006](https://www.spec.org/cpu2006/) | Requires Pro License for CLI | [Link](https://www.spec.org/cpu2006/Docs/install-guide-windows.html)
[SPEC CPU 2017](https://www.spec.org/cpu2017/)	| Requires Pro License for CLI | [Link](https://www.spec.org/cpu2017/Docs/install-guide-windows.html)
[PCMark2002](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[PCMark04](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[PCMark05](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[PCMark Vantage](https://benchmarks.ul.com/legacy-benchmarks) | Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/PCMark_Vantage_Whitepaper.pdf)
[PCMark 7](https://benchmarks.ul.com/legacy-benchmarks) | Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/pcmark7-command-line-guide.pdf)
[PCMark 8](https://benchmarks.ul.com/legacy-benchmarks) | Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/pcmark8-command-line-guide.pdf)
[PCMark 10](https://benchmarks.ul.com/pcmark10) |Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/pcmark10-command-line-guide.pdf)
[PCMark2002](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark99](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark2000](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark2001](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark03](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark05](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark06](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI
[3DMark Vantage](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/3DMark-Vantage-CommandLineGuide.pdf)
[3DMark 11](https://benchmarks.ul.com/legacy-benchmarks) |Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/3dmark11-command-line-guide.pdf)
[3DMark](https://benchmarks.ul.com/3dmark) |Requires Pro License for CLI | [Link](https://support.benchmarks.ul.com/en/support/solutions/articles/44002145411-run-3dmark-benchmarks-from-the-command-line)
[VRMark](https://benchmarks.ul.com/vrmark) |Requires Pro License for CLI | [Link](https://s3.amazonaws.com/download-aws.futuremark.com/vrmark-command-line-guide.pdf)

### Potential CPU Benchmarks
| Benchmark  | Official CLI Documentation | Unofficial CLI Documentation | Notes
| --------  | ------------------- | --------------------- | --------------------- |
[pyprime 1.x](http://pyprime.servehttp.com/PYPrime/PYPrime.html) |
[pyprime 2.x](http://pyprime.servehttp.com/PYPrime/PYPrime2.html) |
[AI-benchmark](https://ai-benchmark.com/alpha.html) |
[wPrime](http://www.wprime.net/) |
[Realbench](https://rog.asus.com/rog-pro/realbench-v2-leaderboard/)		 |
Sisoft Sandra Crytp		 |
[Dolphin](https://forums.dolphin-emu.org/Thread-unofficial-new-dolphin-5-0-cpu-benchmark-results-automatically-updated--45007) |
[Handbrake](https://handbrake.fr/) |
Cygwin GCC 9.3.0 Compile with MT |
Chromium Compile with MSVC, Clang, Ninja |
[Prime95](https://www.mersenne.org/download/) |
Adobe After Effects 2020 Puget Systesms |
Matlab R2020 Built-In Bnechmark |
Microsfot Excel Large Number Crunching Test |
Adobe Acrobat PDF Export PDF to PNG Images |
Adobe Photoshop Puget Systems Benchmark |
Adobe Premiere Warp Stabilizer |
DaVinci Resolve STudio Puget Systems Benchmark |
Adobe Premiere Puget Systems Export Test |
Adobe Premiere 4K 2 Pass H.264 Export |
Office |
Agisoft Photoscan 1.3: 2D to 3D Conversion |
Application Loading Time: GIMP 2.10.18 from a fresh install |
Compile Testing (WIP) |
Science |
3D Particle Movement v2.1 (Non-AVX + AVX2/AVX512) |
NAMD 2.13: Nanoscale Molecular Dynamics on ApoA1 protein |
Simulation |
Digicortex 1.35: Brain stimulation simulation |
Dwarf Fortress 0.44.12: Fantasy world creation and time passage |
Rendering |
Crysis CPU-Only: Can it run Crysis? What, on just the CPU at 1080p? Sure |
POV-Ray 3.7.1: Another Ray Tracing Test |
V-Ray: Another popular renderer |
Encoding |
AES Encoding: Instruction accelerated encoding |
WinRAR 5.90: Popular compression tool |
Legacy |
3DPM v1: Naïve version of 3DPM v2.1 with no acceleration |
X264 HD3.0: Vintage transcoding benchmark |
Web |
Kraken 1.1: Depreciated web test with no successor |
Octane 2.0: More comprehensive test (but also deprecated with no successor) |
Speedometer 2: List-based web-test with different frameworks |
Synthetic |
AIDA Memory Bandwidth |
Linux OpenSSL Speed (rsa2048 sign/verify, sha256, md5) |
LinX 0.9.5 LINPACK (where appropriate) |


# GPU Benchmarks

### Implemented GPU Benchmarks

| Benchmark  | Official CLI Documentation | Unofficial CLI Documentation | Notes
| --------  | ------------------- | --------------------- | --------------------- |
[Cinebench R11.5](https://www.guru3d.com/files-details/cinebench-11-5.html) | |		[Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/) |
[Cinebench R15](https://www.techspot.com/downloads/6709-cinebench.html) | |		[Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)
[Cinebench R15 Extreme](https://www.guru3d.com/files-details/cinebench-r15-extreme-edition-download.html) | | [Link](http://forum.notebookreview.com/threads/cinebench-r15-r15-extreme-r20-command-line-syntax-bat-loop-detailed-output.815101/)			


### Potential GPU Benchmarks
| Benchmark  | Official CLI Documentation | Unofficial CLI Documentation | Notes
| --------  | ------------------- | --------------------- | --------------------- |
[GPUPI 3.3.3](https://www.overclockers.at/news/gpupi-international-support-thread) |	[Link](https://www.overclockers.at/news/gpupi-3-is-now-official)	
[GPUPI 3.2](https://www.overclockers.at/news/gpupi-international-support-thread) |		[Link](https://www.overclockers.at/news/gpupi-3-is-now-official)
[Blender](https://opendata.blender.org/) |	[Link](https://opendata.blender.org/about/)	
Unigine Benchmarks |
Many game benchmarks |

# Install Instructions

* Create an Anaconda 3.8 python environment
* See environment.yml for full list of packages
* Need to add in about anaconda, benchmark setup, etc...

# How to Run
* Run main.py
* Add other details

#  Parameters
TBD

