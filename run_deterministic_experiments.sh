#!/usr/bin/env bash

# run deterministic or stochastic experiments, each run takes 2h8m
# spec: CPU: AMD Ryzen 9 7900X (24) @ 5.733GHz
#       Memory: 64GB
#
# NOTE: Flag discrepancies between py, cpp, go:
#   - Beta: py uses --b, cpp/go use --beta
#   - Output dir: py has none, cpp defaults to data_cpp, go defaults to data_go
#   - Theta params: py has none, cpp/go have --theta-start, --theta-end, --theta-step
#   - Deterministic: cpp requires --deterministic=true, py/go use --deterministic flag
#
# final time result
#     pd pop = 1350 35m07s
#     pd neb =  600 15m23s
#     pd pop = 1350 14m08s
#     pd pop =  600 6m42s

go build -o teesside-go main.go

t=$(nproc)
# save a core so that you can feel safe running this
t=$((t - 1))

parallel_params="--halt now,fail=1 -j $t --eta --progress --bar"

pd_params="--game-type pd --beta {1}"
pd_param_betas="1.2 1.8 2.0"

pgg_params="--game-type pgg --r {1}"
pgg_param_rs="1.5 3.0 4.5"

pop_params="--strategy pop --pc {2}"
pop_param_pcs="0.25 0.5 0.75 0.90 0.92 0.94 0.96 0.98 1.0"

neb_params="--strategy neb --nc {2}"
neb_param_ncs="1 2 3 4"

command_params="--deterministic --output-dir data_deterministic_go_pgg_5groups"
# command_params="--output-dir data_go_pgg_5groups"

parallel $parallel_params ./teesside-go $command_params $pd_params $pop_params --seed-start {3} --seed-end '$(('{3}'+1))' \
    ::: $pd_param_betas \
    ::: $pop_param_pcs \
    ::: {0..49}

parallel $parallel_params ./teesside-go $command_params $pd_params $neb_params --seed-start {3} --seed-end '$(('{3}'+1))' \
    ::: $pd_param_betas \
    ::: $neb_param_ncs \
    ::: {0..49}

parallel $parallel_params ./teesside-go $command_params $pgg_params $pop_params --seed-start {3} --seed-end '$(('{3}'+1))' \
    ::: $pgg_param_rs \
    ::: $pop_param_pcs \
    ::: {0..49}

parallel $parallel_params ./teesside-go $command_params $pgg_params $neb_params --seed-start {3} --seed-end '$(('{3}'+1))' \
    ::: $pgg_param_rs \
    ::: $neb_param_ncs \
    ::: {0..49}
