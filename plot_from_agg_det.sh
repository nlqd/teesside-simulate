#!/bin/bash

source .venv/bin/activate

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.2' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.2' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.8' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.8' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=2.0' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=2.0' --plot-type efficiency &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.2' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.2' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.8' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.8' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=2.0' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=2.0' --plot-type efficiency &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=1.5' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=1.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=3.0' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=3.0' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=4.5' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=4.5' --plot-type efficiency &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=1.5' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=1.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=3.0' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=3.0' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=4.5' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=4.5' --plot-type efficiency &

### PGG -- DIFF
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.2' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=1.8' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy pop --game-param 'b=2.0' --plot-type diff &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.2' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=1.8' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pd --strategy neb --game-param 'b=2.0' --plot-type diff &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=1.5' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=3.0' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy pop --game-param 'r=4.5' --plot-type diff &

python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=1.5' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=3.0' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go --fig-prefix det --game pgg --strategy neb --game-param 'r=4.5' --plot-type diff &

### PGG -- 5groups

python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=1.5' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=1.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=1.5' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=3.0' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=3.0' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=3.0' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=4.5' --plot-type timeseries --theta 4.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=4.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy pop --game-param 'r=4.5' --plot-type diff &

python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=1.5' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=1.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=1.5' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=3.0' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=3.0' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=3.0' --plot-type diff &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=4.5' --plot-type timeseries --theta 5.5 &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=4.5' --plot-type efficiency &
python plot_from_agg.py --agg-dir data_agg_det_go_5groups --fig-prefix 5groups/det --game pgg --strategy neb --game-param 'r=4.5' --plot-type diff &

wait
