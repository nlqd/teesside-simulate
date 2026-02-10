"""Plot θ* (theta for optimal social welfare and cost) summary across all experiments."""
import argparse
import os
import numpy as np
from plot_from_agg import detect_strategy_params, build_diff_matrices
from plotting_utils_v2 import SimulationPlotter

GAMES = {
    'pd': {'params': ['b=1.2', 'b=1.8', 'b=2.0']},
    'pgg': {'params': ['r=1.5', 'r=3.0', 'r=4.5']},
}
STRATEGIES = ['pop', 'neb']
COOP_THRESHOLD = 90.0


def find_optimal_thetas_per_a(data_matrices, thetas, a_values):
    """
    For each a value and each strategy_param column, find:
      - SW: theta that maximizes welfare_a
      - Cost: lowest theta where coop > 90%.
              If never reachable, use theta at max coop (flagged as infeasible).

    Returns: {
        'sw': {a: [theta_stars]},
        'cost': {a: [{'theta': float, 'feasible': bool, 'max_coop': float}]}
    }
    """
    sw_result = {}
    cost_result = {}
    thetas_arr = np.array(thetas)
    coop_freq = data_matrices['coop_freq']  # shape [n_thetas, n_params]

    for a in a_values:
        cost_a = data_matrices['cost'] / a
        welfare_a = data_matrices['welfare'] - cost_a

        sw_result[a] = thetas_arr[np.argmax(welfare_a, axis=0)].tolist()

        cost_result[a] = []
        n_params = coop_freq.shape[1]
        for sp_idx in range(n_params):
            coop_col = coop_freq[:, sp_idx]
            feasible_mask = coop_col > COOP_THRESHOLD

            if feasible_mask.any():
                # Lowest theta where coop > 90%
                first_feasible_idx = np.where(feasible_mask)[0][0]
                cost_result[a].append({
                    'theta': thetas_arr[first_feasible_idx],
                    'feasible': True,
                    'max_coop': coop_col[first_feasible_idx],
                })
            else:
                # Never reaches 90%: use theta at max coop
                best_coop_idx = np.argmax(coop_col)
                cost_result[a].append({
                    'theta': thetas_arr[best_coop_idx],
                    'feasible': False,
                    'max_coop': coop_col[best_coop_idx],
                })

    return {'sw': sw_result, 'cost': cost_result}


def build_all_optimal_data(agg_dir, a_values):
    """Build θ* for SW and cost for all configurations.

    Returns: {
        'sw': {a: {game: {strategy: {game_param: {sp: theta}}}}},
        'cost': {a: {game: {strategy: {game_param: {sp: {theta, feasible, max_coop}}}}}}
    }
    """
    optimal = {
        'sw': {a: {} for a in a_values},
        'cost': {a: {} for a in a_values},
    }

    for game, game_cfg in GAMES.items():
        for metric in ('sw', 'cost'):
            for a in a_values:
                optimal[metric][a][game] = {}

        for strategy in STRATEGIES:
            for metric in ('sw', 'cost'):
                for a in a_values:
                    optimal[metric][a][game][strategy] = {}

            for game_param in game_cfg['params']:
                all_params = detect_strategy_params(agg_dir, game, strategy, game_param)
                if not all_params:
                    continue

                # Filter: POP pc >= 0.9, NEB nc >= 3
                if strategy == 'pop':
                    all_params = [p for p in all_params if float(p.split('=')[1]) >= 0.9]
                elif strategy == 'neb':
                    all_params = [p for p in all_params if float(p.split('=')[1]) >= 3]
                if not all_params:
                    continue

                data_matrices, thetas = build_diff_matrices(
                    agg_dir, game, strategy, game_param, all_params
                )
                results = find_optimal_thetas_per_a(data_matrices, thetas, a_values)

                for a in a_values:
                    optimal['sw'][a][game][strategy][game_param] = {}
                    optimal['cost'][a][game][strategy][game_param] = {}
                    for sp_idx, sp in enumerate(all_params):
                        optimal['sw'][a][game][strategy][game_param][sp] = results['sw'][a][sp_idx]
                        optimal['cost'][a][game][strategy][game_param][sp] = results['cost'][a][sp_idx]

    return optimal


def main():
    parser = argparse.ArgumentParser(description='Plot θ* summary for all experiments.')
    parser.add_argument('--agg-dir', default='data_agg_det_go', help='Aggregated data directory')
    parser.add_argument('--a-values', type=float, nargs='+', default=[0.5, 1.0, 1.5],
                        help='Efficiency a values')
    parser.add_argument('--output', default='fig/det/optimal_theta_summary.png', help='Output file')
    parser.add_argument('--show', action='store_true', help='Show plot')
    args = parser.parse_args()

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    print("Building optimal θ data for all configurations...")
    optimal = build_all_optimal_data(args.agg_dir, args.a_values)

    print("\nGenerating plot...")
    plotter = SimulationPlotter()
    plotter.plot_optimal_theta_summary(
        optimal_sw=optimal['sw'],
        optimal_cost=optimal['cost'],
        a_values=args.a_values,
        title='θ* for Optimal Social Welfare and Cost',
        output_filename=args.output,
        show_plot=args.show
    )


if __name__ == "__main__":
    main()
