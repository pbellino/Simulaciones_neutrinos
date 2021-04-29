#!/bin/bash
#SBATCH -J Si_1MeV_1mm            # Job NAME (human)
##SBATCH -p COMPARTIDA            # Job QUEUE (human)
##SBATCH -p BANCARIZADA            # Job QUEUE (human)
##SBATCH -A grcn
#SBATCH -n 24                   # number of cores (human)
#SBATCH --wait-all-nodes=1       # Do not begin execution until all nodes are ready for use
#SBATCH -o %j.slurm.out          # STDOUT
#SBATCH -e %j.slurm.err          # STDERR
#SBATCH --mem-per-cpu=1G         # Minimum memory required per allocated CPU (human input)
# #SBATCH --mem 0                  # 0 = all node memory allocated
#SBATCH --cpu-freq high
#SBATCH --verbose
# #SBATCH -w compute-1-3
# #SBATCH --depend 19208 
############################## MAIN ################################


#Limpia enviroment
module purge

#Modulos propios del usuario
module load use.own 

#Modulo MKL y Compiladores intel
module load intel/intel_2015.3.187 

#Modulo Intel MPI 5
module load intel/impi_5.0.3.048 

#Modulo para usar solo infiniband
module load intel/impi_fabric_ib 

#Modulo para cuando se usa hypertherading
module load intel/impi_pinning_HT 

#Modulo para cuando se quiere verbose y stats de intel mpi
#module load intel/impi_verbose

#Particulares del job
# module load mcnp


#ulimit and show user limits
echo
ulimit -s unlimited
echo "User limits:"
echo
ulimit -a
echo
#Show slurm var:
echo
echo "Slurm enviroment:"
echo
if [ -z "$SLURM_NPROCS" ] ; then
    if [ -z "$SLURM_NTASKS_PER_NODE" ] ; then
      SLURM_NTASKS_PER_NODE=1
    fi
    SLURM_NPROCS=$(( $SLURM_JOB_NUM_NODES * $SLURM_NTASKS_PER_NODE ))
fi

echo "SLURM_JOB_NAME          = " $SLURM_JOB_NAME
echo "SLURM_JOBID             = " $SLURM_JOBID
echo "SLURM_JOB_NODELIST      = " $SLURM_JOB_NODELIST
echo "SLURM_JOB_PARTITION     = " $SLURM_JOB_PARTITION
echo "SLURM_MEM_PER_CPU       = " $SLURM_MEM_PER_CPU
echo "SLURM_MEM_PER_NODE      = " $SLURM_MEM_PER_NODE
echo "SLURM_ARRAY_JOB_ID      = " $SLURM_ARRAY_JOB_ID
echo "SLURM_ARRAY_TASK_ID     = " $SLURM_ARRAY_TASK_ID
echo "SLURMTMPDIR             = " $SLURMTMPDIR
echo "SLURM_TASKS_PER_NODE    = " $SLURM_TASKS_PER_NODE
echo "SLURM_NTASKS            = " $SLURM_NTASKS
echo "SLURM_NTASKS_PER_CORE   = " $SLURM_NTASKS_PER_CORE
echo "SLURM_NTASKS_PER_NODE   = " $SLURM_NTASKS_PER_NODE
echo "SLURM_NTASKS_PER_SOCKET = " $SLURM_NTASKS_PER_SOCKET
echo "SLURM_JOB_NUM_NODES     = " $SLURM_JOB_NUM_NODES 
echo "SLURM_NNODES            = " $SLURM_NNODES 
echo "SLURM_CPUS_PER_TASK     = " $SLURM_CPUS_PER_TASK
echo "SLURM_NPROCS            = " $SLURM_NPROCS
echo "SLURM_SUBMIT_DIR        = " $SLURM_SUBMIT_DIR
echo "SLURM_SUBMIT_HOST       = " $SLURM_SUBMIT_HOST
echo "SLURM_CPU_FREQ_REQ      = " $SLURM_CPU_FREQ_REQ

cd $SLURM_SUBMIT_DIR


srun --nodes=${SLURM_NNODES} bash -c 'hostname'> $SLURM_JOBID.machines
srun --nodes=${SLURM_NNODES} bash -c 'hostname' | sort -r | uniq > $SLURM_JOBID.mpd.hosts


NUM_PROCS=`cat $SLURM_JOBID.machines|wc -l`
NUM_NODES=`cat $SLURM_JOBID.mpd.hosts|wc -l`

echo NUM_PROCS = $NUM_PROCS
echo NUM_NODES = $NUM_NODES

bin="/home/pbellino/grcn/phits3.17/phits317B/phits/bin/phits_LinIfort_MPI"
echo
echo
echo -n "pwd: "
pwd
echo -n "which mpiexec: "
which mpiexec
echo -n "which mpirun: "
which mpirun
echo -n "LD_LIBRARY_PATH: "
echo $LD_LIBRARY_PATH
echo "BEGIN MPI RUN"
echo
export I_MPI_PMI_LIBRARY=/usr/lib64/libpmi.so
echo srun -n $SLURM_NTASKS $bin
echo
echo "Se lee input del archivo 'phits.in'"
echo
srun -n $SLURM_NTASKS $bin
echo
echo "END MPI RUN"
