# RSAA HPC Skillshare -- PBS Tutorial

This repository contains example **PBS job scripts** and **Python
programs** used in the RSAA HPC Skillshare tutorial.

You can find Mark Krumholz's Introductory slides [here](https://github.com/svenbuder/rsaa_skillshare/blob/main/2026-03-supercomputing/rsaa-skillshare-supercomputing-slides.pdf)

## 1 SSH onto mozzie and clone the repository

SSH onto our RSAA HPC cluster mozzie (historically called avatar)

``` bash
ssh -Y MSO_USERNAME@mozzie.anu.edu.au
```

Clone the repository and list its content

``` bash
git clone https://github.com/svenbuder/rsaa_hpc_tutorial.git
cd rsaa_hpc_tutorial
ls
```

You should see the following repository structure:

    rsaa_hpc
    ├── code/       Python scripts executed by the jobs
    ├── logs/       PBS logs
    ├── output/     Output created by the jobs
    └── *.pbs       PBS job submission scripts

## 2 Submitting jobs

Example:

``` bash
qsub pbs_job_name.pbs
```

Check jobs:

``` bash
qstat
```

Cancel a job:

``` bash
qdel JOBID
```

### 2.1 Example 1 -- A job that works (but should not be used)

    qsub pbs_0_minimal.pbs

Runs the following `code/hello_world.py`:

```python
import time

print("Hello from the HPC cluster!")

for i in range(5):
    print(f"Step {i}")
    time.sleep(2)

print("Done")
```

The following logs appear in `logs/`:

    logs/
    ├── *.OU    Output logs (what would be printed to screen)
    └── *.ER    Error logs (here: I purposefully forgot an `echo`)

While this job runs, I would not use it. There some things one should fix or add to a job submission file.

### 2.2 Example 2 --- Single CPU job with output

Submit the job:

    qsub pbs_2_single_cpu.pbs

This example runs a slightly more realistic batch job.\
In addition to writing log messages, it produces scientific output
files when executing `code/sine_function.py`.

#### PBS script

``` bash
#!/bin/bash
#PBS -N 2_single_cpu
#PBS -l select=1:ncpus=1
# Each node has 28 CPUs
#PBS -q small
# Options for -q on mozzie include: small, large
#PBS -o logs/
#PBS -e logs/
#PBS -m ae

cd "$PBS_O_WORKDIR"

echo "Running on:"
hostname
echo "Working directory:"
pwd
echo "Job ID:"
echo "$PBS_JOBID"

python code/sine_function.py

echo "Job finished successfully."
```

#### Changes compared to Example 1

The PBS script is mostly the same as before, but now:

-   We submit the job to one of the more numerous `small` memory nodes
-   Email notifications are enabled (`#PBS -m ae`)
-   The job runs a Python script that produces a `pdf` and `png` file showing a sine-function as well as a `txt` file that has the `amplitude`, `frequency`, `phase`, and `offset` of the function.
-   These output files are saved in the `output/` directory to keep projects organised and makes it easier to find results from many jobs.

![Sine function example](output/sine_function.png)

## 2.3 Example 3 -- Threaded job with 4 CPUs

Submit the job:

```bash
qsub pbs_3_threaded_4cpu.pbs
```

Runs:

```text
code/threaded_sine_scan.py
```

This example requests **4 CPUs** and uses Python multiprocessing to split a simple numerical task across several worker processes.

### What changes compared to Example 2?

- the job now requests more than one CPU
- the Python script uses multiple worker processes
- the output still goes into `output/`
- this is an example of **shared-memory parallelism on one node**

### PBS script

```bash
#!/bin/bash
#PBS -N 3_threaded_4cpu
#PBS -l select=1:ncpus=4
#PBS -q small
# Options for -q on mozzie include: small, large
#PBS -o logs/
#PBS -e logs/
#PBS -m ae
# Optional: adjust email on (on new line): #PBS -M your.email@example.com

cd "$PBS_O_WORKDIR"

echo "Running on:"
hostname
echo "Working directory:"
pwd
echo "Job ID:"
echo "$PBS_JOBID"
echo "Allocated CPUs:"
echo "$PBS_NCPUS"

python code/threaded_sine_scan.py "$PBS_NCPUS"

echo "Job finished successfully."
```

### What the Python code does

The script evaluates several sine-function parameter combinations and computes a simple numerical summary for each case.

It:

1. creates a list of independent tasks
2. distributes them across the requested CPUs
3. gathers the results
4. writes them to

```text
output/threaded_sine_scan_results.txt
```

This example is useful to show that requesting multiple CPUs only helps if the code is actually written to use them.

---

## 2.4 Example 4 -- Job array

Submit the job:

```bash
qsub pbs_4_job_array.pbs
```

Runs:

```text
code/array_sine_function.py
```

This example launches a **job array**.  
Each array task gets a different value of `PBS_ARRAY_INDEX` and creates a slightly different sine function.

### Why job arrays are useful

Job arrays are ideal when you want to run many similar jobs, for example:

- scanning different parameters
- processing many input files
- repeating simulations with different seeds

### PBS script

```bash
#!/bin/bash
#PBS -N 4_job_array
#PBS -l select=1:ncpus=1
#PBS -q small
# Options for -q on mozzie include: small, large
#PBS -J 1-5
#PBS -o logs/
#PBS -e logs/
#PBS -m ae
# Optional: adjust email on (on new line): #PBS -M your.email@example.com

cd "$PBS_O_WORKDIR"

echo "Running on:"
hostname
echo "Working directory:"
pwd
echo "Job ID:"
echo "$PBS_JOBID"
echo "Array index:"
echo "$PBS_ARRAY_INDEX"

python code/array_sine_function.py "$PBS_ARRAY_INDEX"

echo "Job finished successfully."
```

### What the Python code does

For each array index, the script:

1. chooses a different sine-function frequency
2. creates a plot
3. saves the figure and parameters with filenames containing the array index

Example output files:

```text
output/array_sine_1.png
output/array_sine_1.txt
output/array_sine_2.png
output/array_sine_2.txt
...
```

This demonstrates how many related jobs can be submitted with one `qsub` command.

---

## 2.5 Example 5 -- Interactive Jupyter notebook

Submit the job:

```bash
qsub pbs_5_jupyter_notebook.pbs
```

This starts a **Jupyter notebook server on a compute node**.

### Why do this?

Interactive work should not run on the login node.  
Instead, you request resources via PBS and run Jupyter on the allocated compute node.

### PBS script

```bash
#!/bin/bash
#PBS -N 5_jupyter_notebook
#PBS -l select=1:ncpus=2
#PBS -q small
# Options for -q on mozzie include: small, large
#PBS -o logs/
#PBS -e logs/
#PBS -m ae
# Optional: adjust email on (on new line): #PBS -M your.email@example.com

cd "$PBS_O_WORKDIR"

PORT=8888

echo "Running on:"
hostname
echo "Working directory:"
pwd
echo "Job ID:"
echo "$PBS_JOBID"
echo
echo "To connect from your laptop, run:"
echo "ssh -L ${PORT}:localhost:${PORT} USERNAME@HEADNODE"
echo
echo "Then open:"
echo "http://localhost:${PORT}"
echo

jupyter notebook --no-browser --port="${PORT}" --ip=0.0.0.0
```

### How to connect

Once the job starts, create an SSH tunnel from your local computer:

```bash
ssh -L 8888:localhost:8888 USERNAME@HEADNODE
```

Then open:

```text
http://localhost:8888
```

in your browser.

Depending on the cluster configuration, you may need to adapt the SSH command.  
The main lesson is that the notebook runs on the compute node, not on the login node.

---

## 2.6 Example 6 -- Small scaling test

Submit the job:

```bash
qsub pbs_6_scaling_test.pbs
```

Runs:

```text
code/scaling_test.py
```

This example measures how the runtime of a parallel task changes when using:

```text
1, 2, 4, and 8 CPUs
```

### Why this is useful

A common mistake on HPC systems is to request more CPUs than a program can use efficiently.

A scaling test helps answer:

- does the code actually run faster?
- is the speed-up close to ideal?
- when do overheads become important?

### PBS script

```bash
#!/bin/bash
#PBS -N 6_scaling_test
#PBS -l select=1:ncpus=8
#PBS -q small
# Options for -q on mozzie include: small, large
#PBS -o logs/
#PBS -e logs/
#PBS -m ae
# Optional: adjust email on (on new line): #PBS -M your.email@example.com

cd "$PBS_O_WORKDIR"

echo "Running on:"
hostname
echo "Working directory:"
pwd
echo "Job ID:"
echo "$PBS_JOBID"
echo "Allocated CPUs:"
echo "$PBS_NCPUS"

python code/scaling_test.py

echo "Job finished successfully."
```

### What the Python code does

The script performs a Monte Carlo estimate of pi and repeats the calculation using 1, 2, 4, and 8 processes.

It then:

1. measures the runtime for each case
2. computes the speed-up relative to 1 CPU
3. writes a summary table to

```text
output/scaling_results.txt
```

4. saves two figures:

```text
output/scaling_runtime.png
output/scaling_speedup.png
```

### How to interpret the result

- **Runtime plot:** lower is better
- **Speed-up plot:** compares measured speed-up to ideal speed-up

In a perfect world, doubling the number of CPUs would halve the runtime.  
In practice, communication and process-management overheads mean scaling is usually less than ideal.
