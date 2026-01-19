#!/bin/bash

source .venv/bin/activate

python preprocess_seeds.py --data-dir data/pop_theta --output-dir data_agg &

### theta 4-5

# python preprocess_seeds.py --data-dir 'data/pop_theta_pgg_r=1.5' --output-dir data_agg &
# python preprocess_seeds.py --data-dir 'data/pop_theta_pgg_r=3.0' --output-dir data_agg &
# python preprocess_seeds.py --data-dir 'data/pop_theta_pgg_r=4.5' --output-dir data_agg &
# python preprocess_seeds.py --data-dir 'data/neb_theta_pgg_r=1.5' --output-dir data_agg &
# python preprocess_seeds.py --data-dir 'data/neb_theta_pgg_r=3.0' --output-dir data_agg &
# python preprocess_seeds.py --data-dir 'data/neb_theta_pgg_r=4.5' --output-dir data_agg &

# theta 0-10

python preprocess_seeds.py --data-dir 'data_py_theta010/pop_theta_pgg_r=1.5' --output-dir data_agg &
python preprocess_seeds.py --data-dir 'data_py_theta010/pop_theta_pgg_r=3.0' --output-dir data_agg &
python preprocess_seeds.py --data-dir 'data_py_theta010/pop_theta_pgg_r=4.5' --output-dir data_agg &
python preprocess_seeds.py --data-dir 'data_py_theta010/neb_theta_pgg_r=1.5' --output-dir data_agg &
python preprocess_seeds.py --data-dir 'data_py_theta010/neb_theta_pgg_r=3.0' --output-dir data_agg &
python preprocess_seeds.py --data-dir 'data_py_theta010/neb_theta_pgg_r=4.5' --output-dir data_agg &

python preprocess_seeds.py --data-dir 'data_go_theta010/pop_theta_pgg_r=1.5' --output-dir data_agg_go &
python preprocess_seeds.py --data-dir 'data_go_theta010/pop_theta_pgg_r=3.0' --output-dir data_agg_go &
python preprocess_seeds.py --data-dir 'data_go_theta010/pop_theta_pgg_r=4.5' --output-dir data_agg_go &
python preprocess_seeds.py --data-dir 'data_go_theta010/neb_theta_pgg_r=1.5' --output-dir data_agg_go &
python preprocess_seeds.py --data-dir 'data_go_theta010/neb_theta_pgg_r=3.0' --output-dir data_agg_go &
python preprocess_seeds.py --data-dir 'data_go_theta010/neb_theta_pgg_r=4.5' --output-dir data_agg_go &

# cpp PD data -- different b values
python preprocess_seeds.py --data-dir 'data_cpp/pop_theta_pd_b=1.2' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/pop_theta_pd_b=1.4' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/pop_theta_pd_b=1.6' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/pop_theta_pd_b=1.8' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/pop_theta_pd_b=2.0' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/neb_theta_pd_b=1.2' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/neb_theta_pd_b=1.4' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/neb_theta_pd_b=1.6' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/neb_theta_pd_b=1.8' --output-dir data_agg_cpp &
python preprocess_seeds.py --data-dir 'data_cpp/neb_theta_pd_b=2.0' --output-dir data_agg_cpp &

# deterministic go
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pd_b=1.2'  --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pd_b=1.8'  --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pd_b=2'    --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pgg_r=1.5' --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pgg_r=3'   --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/pop_theta_pgg_r=4.5' --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pd_b=1.2'  --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pd_b=1.8'  --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pd_b=2'    --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pgg_r=1.5' --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pgg_r=3'   --output-dir data_agg_det_go &
python preprocess_seeds.py --data-dir  'data_deterministic_go/neb_theta_pgg_r=4.5' --output-dir data_agg_det_go &

wait
