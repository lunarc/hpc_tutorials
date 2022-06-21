
squeue -u bmjl
             JOBID PARTITION     NAME     USER ST       TIME  NODES NODELIST(REASON)
           6655262        lu paramete     bmjl  R       5:44      1 au007

#SBATCH -N 1

slurmstepd: error: *** JOB 6655192 ON au007 CANCELLED AT 2022-06-17T15:13:45 DUE TO TIME LIMIT ***

#SBATCH -t 00:20:00

Render Time:
  Photon Time:      0 hours  0 minutes  2 seconds (2.108 seconds)
              using 23 thread(s) with 2.129 CPU-seconds total
  Radiosity Time:   No radiosity
  Trace Time:       0 hours 14 minutes 39 seconds (879.038 seconds)
              using 20 thread(s) with 877.617 CPU-seconds total
POV-Ray finished


#SBATCH --tasks-per-node=20

Render Time:
  Photon Time:      0 hours  0 minutes  1 seconds (1.800 seconds)
              using 23 thread(s) with 2.136 CPU-seconds total
  Radiosity Time:   No radiosity
  Trace Time:       0 hours  0 minutes 46 seconds (46.386 seconds)
              using 20 thread(s) with 891.289 CPU-seconds total

#SBATCH --tasks-per-node=10

Render Time:
  Photon Time:      0 hours  0 minutes  1 seconds (1.757 seconds)
              using 23 thread(s) with 2.081 CPU-seconds total
  Radiosity Time:   No radiosity
  Trace Time:       0 hours  1 minutes 27 seconds (87.700 seconds)
              using 20 thread(s) with 865.305 CPU-seconds total
POV-Ray finished

#SBATCH --tasks-per-node=5

Render Time:
  Photon Time:      0 hours  0 minutes  1 seconds (1.772 seconds)
              using 23 thread(s) with 2.115 CPU-seconds total
  Radiosity Time:   No radiosity
  Trace Time:       0 hours  2 minutes 54 seconds (174.506 seconds)
              using 20 thread(s) with 868.146 CPU-seconds total
POV-Ray finished


#SBATCH -oe povray_%j.out


