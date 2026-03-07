# RSAA HPC Skillshare -- PBS Tutorial

This repository contains example **PBS job scripts** and **Python
programs** used in the RSAA HPC Skillshare tutorial.

You can find Mark Krumholz's Introductory slides [here](https://github.com/svenbuder/rsaa_skillshare/blob/main/2026-03-supercomputing/rsaa-skillshare-supercomputing-slides.pdf)

------------------------------------------------------------------------

# SSH onto our RSAA HPC cluster mozzie (historically called avatar)

``` bash
ssh -Y MSO_USERNAME@mozzie.anu.edu.au
```


# Clone the repository

``` bash
git clone https://github.com/svenbuder/rsaa_hpc_tutorial.git
cd rsaa_hpc_tutorial
```

Repository structure:

    rsaa_hpc
    ├── code/       Python scripts executed by the jobs
    ├── logs/       PBS logs
    ├── output/     Output created by the jobs
    └── *.pbs       PBS job submission scripts

------------------------------------------------------------------------

# Submitting jobs

Example:

``` bash
qsub pbs_single_cpu.pbs
```

Check jobs:

``` bash
qstat
```

Cancel a job:

``` bash
qdel JOBID
```

------------------------------------------------------------------------

# Example 1 -- Single CPU job

    qsub pbs_single_cpu.pbs

Runs:

    code/hello_world.py

Logs appear in:

    logs/

------------------------------------------------------------------------

# Example 2 -- Multi‑CPU job

    qsub pbs_threaded_4cpu.pbs

Requests **4 CPUs** and runs a multiprocessing Python script.

------------------------------------------------------------------------

# Example 3 -- Job array

    qsub pbs_job_array.pbs

Launches **3 jobs simultaneously**.

Each job writes results to:

    output/

------------------------------------------------------------------------

# Example 4 -- Jupyter notebook on a compute node

    qsub pbs_jupyter_notebook.pbs

Then connect with SSH tunnelling from your computer:

``` bash
ssh -L 8888:localhost:8888 USERNAME@mozzie.anu.edu.au
```

Open:

    http://localhost:8888

------------------------------------------------------------------------

# Important PBS variable

All scripts contain:

    cd $PBS_O_WORKDIR

This ensures the job runs from the submission directory.
