
NAME=phits_mpi.slurm

.SUFFIXES:
.PHONY: clean run run_bancarizada

run: 
	sbatch $(NAME)

run_bancarizada:
	sbatch -p BANCARIZADA -A grcn $(NAME)

clean: 
	rm -f *.machines *.mpd.hosts *.slurm.err *.slurm.out phits.out cross_reg.* batch.out


