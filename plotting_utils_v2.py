import matplotlib.pyplot as plt
import numpy as np
import csv
import re
import os
from typing import List, Dict, Tuple, Optional, Any, Callable
from dataclasses import dataclass


@dataclass
class PlotConfig:
    COLORS = {
        'cooperator': '#6B7FD7',
        'defector': '#FF7875',
        'cost': '#B88BBD',
        'welfare': '#F18F01'
    }

    max_generations: int = 50
    population_size: int = 10000

    dpi: int = 300

    label_fontsize: int = 12
    tick_fontsize: int = 8
    title_fontsize: int = 11

    color_map = "inferno"
    color_interp = "bilinear"


class DataLoader:
    """Handles loading and parsing simulation data from CSV files."""

    METRIC_COLUMNS = {
        'cooperator_frequency': 'Cooperator_Frequency',
        'cost': 'Cost',
        'social_welfare': 'Social_Welfare',
        'population_payoff': 'Payoff'
    }

    METRIC_COLUMNS_NEB = {
        'cooperator_frequency': 'Final_Cooperator_Frequency',
        'cost': 'Final_Cost',
        'social_welfare': 'Final_Social_Welfare',
        'population_payoff': 'Final_Fitnesses'
    }

    @staticmethod
    def parse_array(array_str: str) -> List[float]:
        """Parse array string - handles np.int64(val), [1,2,3], and space-separated formats."""
        # Try numpy format: np.int64(value)
        pattern = r'np\.(int64|float64)\(([^)]+)\)'
        matches = re.findall(pattern, array_str)
        if matches:
            return [float(val) for _, val in matches]

        # Strip brackets
        array_str = array_str.strip().strip('[]')

        # Try comma-separated
        if ',' in array_str:
            return [float(x.strip()) for x in array_str.split(',') if x.strip()]

        # Fall back to space-separated
        return [float(x) for x in array_str.split() if x.strip()]

    @staticmethod
    def load_csv(filepath: str) -> List[Dict[str, Any]]:
        with open(filepath, 'r') as f:
            return list(csv.DictReader(f))

    @classmethod
    def load_pop_data(cls, data_dir: str, metric: str, pc_value: str, seed: int,
                      theta_range: str = None) -> List[Dict[str, Any]]:
        """Load POP strategy data."""
        if theta_range:
            filepath = f"{data_dir}/seed_{seed}_theta_{theta_range}_pc={pc_value}_{metric}.csv"
        else:
            filepath = f"{data_dir}/seed_{seed}_pc={pc_value}_{metric}.csv"
        return cls.load_csv(filepath)

    @classmethod
    def load_neb_data(cls, data_dir: str, nc_value: int) -> List[Dict[str, Any]]:
        """Load NEB strategy data from consolidated file."""
        return cls.load_csv(f"{data_dir}/nc_{nc_value}_final_all.csv")

    @classmethod
    def get_metric_array(cls, row: Dict[str, Any], metric: str, is_neb: bool = False) -> List[float]:
        """Extract and parse metric array from a data row."""
        columns = cls.METRIC_COLUMNS_NEB if is_neb else cls.METRIC_COLUMNS
        column = columns.get(metric)
        if not column:
            raise ValueError(f"Unknown metric: {metric}")
        return cls.parse_array(row[column])

    @classmethod
    def get_theta_values(cls, data_dir: str, pc_value: str, seed: int,
                         theta_range: str = None) -> List[float]:
        """Get sorted unique theta values from data."""
        data = cls.load_pop_data(data_dir, 'cooperator_frequency', pc_value, seed, theta_range)
        return sorted(set(float(row['Theta']) for row in data))

    @classmethod
    def load_metric_data(cls, data_dir: str, metric: str, param_value: str, seed: int,
                         param_name: str = 'pc', theta_range: str = None) -> List[Dict[str, Any]]:
        """Load metric data with flexible param_name (pc or nc). Auto-detects _det suffix."""
        if theta_range:
            filepath = f"{data_dir}/seed_{seed}_theta_{theta_range}_{param_name}={param_value}_{metric}.csv"
            if not os.path.exists(filepath):
                filepath = f"{data_dir}/seed_{seed}_theta_{theta_range}_{param_name}={param_value}_det_{metric}.csv"
        else:
            filepath = f"{data_dir}/seed_{seed}_{param_name}={param_value}_{metric}.csv"
            if not os.path.exists(filepath):
                filepath = f"{data_dir}/seed_{seed}_{param_name}={param_value}_det_{metric}.csv"
        return cls.load_csv(filepath)

    @classmethod
    def parse_metric_from_row(cls, row: Dict[str, Any], metric: str) -> List[float]:
        """Parse metric array from row (for POP data)."""
        column = cls.METRIC_COLUMNS.get(metric)
        if not column:
            raise ValueError(f"Unknown metric: {metric}")
        return cls.parse_array(row[column])


def pad_to_length(data: List[float], target_len: int) -> List[float]:
    """Pad list with last value or truncate to target length."""
    if len(data) >= target_len:
        return data[:target_len]
    return data + [data[-1]] * (target_len - len(data))


def find_convergence_idx(welfare: List[float]) -> Optional[int]:
    """Find index where welfare drops to 0 after being non-zero."""
    for i in range(1, len(welfare)):
        if welfare[i] == 0 and welfare[i - 1] > 0:
            return i
    return None


def prepare_timeseries(coop: List[float], cost: List[float], welfare: List[float],
                       max_gen: int) -> Tuple[List[float], List[float], List[float]]:
    """Prepare time series data: handle convergence and pad to max_gen."""
    conv_idx = find_convergence_idx(welfare)

    if conv_idx is not None:
        last_welfare = welfare[conv_idx - 1]
        welfare = welfare[:conv_idx] + [last_welfare] * (max_gen - conv_idx)

    return (
        pad_to_length(coop, max_gen),
        pad_to_length(cost, max_gen),
        pad_to_length(welfare, max_gen)
    )


def setup_timeseries_ax(ax, generations, y_data, color: str, ylabel: str = None,
                        xlabel: str = None, ylim: Tuple = None, fill_to_100: bool = False,
                        fill_color_top: str = None, legend_labels: Tuple[str, str] = None,
                        config: PlotConfig = None):
    """Configure a time series axis with fill_between styling."""
    config = config or PlotConfig()
    max_gen = config.max_generations

    if fill_to_100 and fill_color_top:
        ax.fill_between(generations, 0, y_data, color=color, alpha=1.0,
                        linewidth=0.5, edgecolor=color, label=legend_labels[0] if legend_labels else None)
        ax.fill_between(generations, y_data, 100, color=fill_color_top, alpha=1.0,
                        linewidth=0.5, edgecolor=fill_color_top, label=legend_labels[1] if legend_labels else None)
    else:
        ax.fill_between(generations, y_data, color=color, alpha=1.0 if 'welfare' not in str(ylabel).lower() else 0.8,
                        linewidth=0.5, edgecolor=color)

    ax.set_xlim(0, max_gen)
    ax.set_xticks([0, 10, 20, 30, 40, max_gen])
    ax.tick_params(labelsize=config.tick_fontsize)
    ax.grid(True, alpha=0.35, linewidth=0.5, color='gray')

    if ylim:
        ax.set_ylim(ylim)
        if ylim[1] == 100:
            ax.set_yticks([0, 20, 40, 60, 80, 100])

    if ylabel:
        ax.set_ylabel(ylabel, fontsize=10)
    if xlabel:
        ax.set_xlabel(xlabel, fontsize=10)


def save_figure(fig, output_path: str, dpi: int = 300, show: bool = False, message: str = None):
    """Save figure, print message, optionally show, then close."""
    plt.savefig(output_path, dpi=dpi, bbox_inches='tight')
    import subprocess
    subprocess.run(['mogrify', '-resize', '1920x1920>', '-quality', '90', output_path], check=True)
    if message:
        print(message)
    else:
        print(f"Saved: {output_path}")

    if show:
        plt.show()
    else:
        plt.close()


class SimulationPlotter:
    def __init__(self, config: Optional[PlotConfig] = None):
        self.config = config or PlotConfig()
        self.loader = DataLoader()

    def _load_multiseed_timeseries(
        self,
        load_fn: Callable[[int], Tuple[List[float], List[float], List[float]]],
        seeds: List[int]
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Load and stack time series data from multiple seeds."""
        all_coop, all_cost, all_welfare = [], [], []

        for seed in seeds:
            try:
                coop, cost, welfare = load_fn(seed)
                coop, cost, welfare = prepare_timeseries(coop, cost, welfare, self.config.max_generations)
                all_coop.append(coop)
                all_cost.append(cost)
                all_welfare.append(welfare)
            except (FileNotFoundError, StopIteration):
                continue

        return np.array(all_coop), np.array(all_cost), np.array(all_welfare)

    def _plot_timeseries_column(self, axes_col, generations, coop_pct, costs, welfare,
                                 std_coop=None, std_cost=None, std_welfare=None,
                                 title: str = None, is_first_col: bool = False,
                                 is_last_col: bool = False, show_std: bool = True):
        """Plot a single column (3 rows) of time series data."""
        colors = self.config.COLORS

        # Row 0: Frequency
        ax_freq = axes_col[0]
        setup_timeseries_ax(ax_freq, generations, coop_pct, colors['cooperator'],
                            ylabel='frequency' if is_first_col else None,
                            ylim=(0, 100), fill_to_100=True,
                            fill_color_top=colors['defector'],
                            legend_labels=('C', 'D'), config=self.config)
        if show_std and std_coop is not None:
            ax_freq.fill_between(generations, coop_pct - std_coop, coop_pct + std_coop,
                                 color='white', alpha=0.3)
        if is_last_col:
            ax_freq.legend(loc='upper right', fontsize=8, frameon=True, fancybox=False)
        if title:
            ax_freq.set_title(title, fontsize=self.config.title_fontsize, fontweight='bold')

        # Row 1: Cost
        ax_cost = axes_col[1]
        setup_timeseries_ax(ax_cost, generations, costs, colors['cost'],
                            ylabel='cost' if is_first_col else None, config=self.config)
        if show_std and std_cost is not None:
            ax_cost.fill_between(generations, costs - std_cost, costs + std_cost,
                                 color=colors['cost'], alpha=0.3)

        # Row 2: Social Welfare
        ax_welfare = axes_col[2]
        setup_timeseries_ax(ax_welfare, generations, welfare, colors['welfare'],
                            ylabel='SW (a=1)' if is_first_col else None,
                            xlabel='generation', config=self.config)
        if show_std and std_welfare is not None:
            ax_welfare.fill_between(generations, welfare - std_welfare, welfare + std_welfare,
                                    color=colors['welfare'], alpha=0.3)

    def _plot_heatmap(self, ax, data: np.ndarray, x_values: List[str], y_values: List[float],
                      title: str, xlabel: str, ylabel: str, colorbar_label: str):
        """Plot a single heatmap."""
        im = ax.imshow(data, aspect='auto', cmap=self.config.color_map, origin='lower', interpolation=self.config.color_interp)

        ax.set_xticks(np.arange(len(x_values)))
        ax.set_xticklabels([f'{float(x):.2f}' for x in x_values])
        ax.set_yticks(np.arange(len(y_values)))
        ax.set_yticklabels([f'{t:.1f}' for t in y_values])

        ax.set_xlabel(xlabel, fontsize=self.config.label_fontsize)
        ax.set_ylabel(ylabel, fontsize=self.config.label_fontsize)
        ax.set_title(title, fontsize=self.config.title_fontsize, fontweight='bold')

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label(colorbar_label, rotation=270, labelpad=15)

    def _load_multiseed_heatmap(
        self,
        data_dir: str,
        param_values: List[str],
        theta_values: List[float],
        seeds: List[int],
        metrics: List[str],
        aggregation: Dict[str, str],
        theta_range: str = None
    ) -> Dict[str, np.ndarray]:
        """Load heatmap data averaged across seeds."""
        all_data = {m: np.zeros((len(seeds), len(theta_values), len(param_values))) for m in metrics}

        for seed_idx, seed in enumerate(seeds):
            for pc_idx, pc in enumerate(param_values):
                for metric in metrics:
                    try:
                        metric_data = self.loader.load_pop_data(data_dir, metric, pc, seed, theta_range)

                        for theta_idx, theta in enumerate(theta_values):
                            row = next((r for r in metric_data if abs(float(r['Theta']) - theta) < 0.01), None)
                            if row:
                                values = self.loader.get_metric_array(row, metric)
                                if aggregation.get(metric) == 'sum':
                                    value = sum(values)
                                else:
                                    value = values[-1] if values else 0

                                if metric == 'cooperator_frequency':
                                    value = (value / self.config.population_size) * 100

                                all_data[metric][seed_idx, theta_idx, pc_idx] = value
                    except FileNotFoundError:
                        continue

        return {m: np.mean(all_data[m], axis=0) for m in metrics}

    def plot_timeseries_from_agg(
        self,
        agg_data: Dict[str, Dict[str, Dict[float, Dict[str, List[float]]]]],
        strategy_params: List[str],
        theta: float,
        title: str = '',
        show_std: bool = True,
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ) -> str:
        """
        Plot timeseries grid from pre-aggregated data.

        Args:
            agg_data: {strategy_param: {metric: {theta: {'mean': [...], 'std': [...]}}}}
            strategy_params: List of strategy param labels (e.g. ['pc=0.25', 'pc=0.5'])
            theta: Theta value to plot
            title: Overall figure title
            show_std: Whether to show standard deviation bands
        """
        n_cols = len(strategy_params)
        pop_size = self.config.population_size
        colors = self.config.COLORS

        fig, axes = plt.subplots(3, n_cols, figsize=(4 * n_cols, 6),
                                 gridspec_kw={'hspace': 0.3, 'wspace': 0.25})
        if n_cols == 1:
            axes = axes.reshape(-1, 1)

        for col_idx, sp in enumerate(strategy_params):
            sp_data = agg_data.get(sp, {})
            coop = sp_data.get('cooperator_frequency', {}).get(theta)
            cost = sp_data.get('cost', {}).get(theta)
            welfare = sp_data.get('social_welfare', {}).get(theta)

            if not coop:
                print(f"Warning: theta={theta} not found for {sp}")
                continue

            max_gen = self.config.max_generations

            def pad_series(arr, target_len, pad_value=None):
                """Pad array to target length. If pad_value is None, use last value."""
                arr = np.array(arr)
                if len(arr) >= target_len:
                    return arr[:target_len]
                fill = pad_value if pad_value is not None else arr[-1]
                return np.concatenate([arr, np.full(target_len - len(arr), fill)])

            coop_mean = pad_series(coop['mean'], max_gen)
            coop_std = pad_series(coop['std'], max_gen)
            cost_mean = pad_series(cost['mean'], max_gen, pad_value=0)
            cost_std = pad_series(cost['std'], max_gen, pad_value=0)
            welfare_mean = pad_series(welfare['mean'], max_gen)
            welfare_std = pad_series(welfare['std'], max_gen)

            generations = np.arange(max_gen)
            coop_pct = (coop_mean / pop_size) * 100
            std_coop_pct = (coop_std / pop_size) * 100

            is_first = col_idx == 0
            is_last = col_idx == n_cols - 1

            # Row 0: Frequency
            ax_freq = axes[0, col_idx]
            setup_timeseries_ax(ax_freq, generations, coop_pct, colors['cooperator'],
                                ylabel='frequency' if is_first else None,
                                ylim=(0, 100), fill_to_100=True,
                                fill_color_top=colors['defector'],
                                legend_labels=('C', 'D'), config=self.config)
            if show_std:
                ax_freq.fill_between(generations, coop_pct - std_coop_pct, coop_pct + std_coop_pct,
                                     color='white', alpha=0.3)
            if is_last:
                ax_freq.legend(loc='upper right', fontsize=8, frameon=True, fancybox=False)
            ax_freq.set_title(sp, fontsize=self.config.title_fontsize, fontweight='bold')

            # Row 1: Cost (clip std band at 0 - cost can't be negative)
            ax_cost = axes[1, col_idx]
            setup_timeseries_ax(ax_cost, generations, cost_mean, colors['cost'],
                                ylabel='cost' if is_first else None, config=self.config)
            if show_std:
                cost_lower = np.maximum(cost_mean - cost_std, 0)
                ax_cost.fill_between(generations, cost_lower, cost_mean + cost_std,
                                     color=colors['cost'], alpha=0.3)

            # Row 2: Social Welfare
            ax_welfare = axes[2, col_idx]
            setup_timeseries_ax(ax_welfare, generations, welfare_mean, colors['welfare'],
                                ylabel='SW (a=1)' if is_first else None,
                                xlabel='generation', config=self.config)
            if show_std:
                ax_welfare.fill_between(generations, welfare_mean - welfare_std, welfare_mean + welfare_std,
                                        color=colors['welfare'], alpha=0.3)

        if title:
            fig.suptitle(title, fontsize=12, y=1.02)

        if output_filename:
            save_figure(fig, output_filename, self.config.dpi, show_plot)
        else:
            plt.show()

        return output_filename

    def plot_heatmap_grid_from_agg(
        self,
        data_matrices: Dict[str, np.ndarray],
        strategy_params: List[str],
        theta_values: List[float],
        a_values: List[float],
        title: str = '',
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ) -> str:
        """
        Plot heatmap grid for different 'a' values (cost efficiency).

        Args:
            data_matrices: {'cost': array, 'welfare': array} with shape [theta, param]
            a_values: List of efficiency values to plot
        """
        n_cols = len(a_values)
        fig, axes = plt.subplots(2, n_cols, figsize=(5 * n_cols, 8))

        for col_idx, a in enumerate(a_values):
            cost_a = data_matrices['cost'] / a
            welfare_a = data_matrices['welfare_base'] - cost_a

            # Row 0: Cost
            ax_cost = axes[0, col_idx]
            im_cost = ax_cost.imshow(cost_a, aspect='auto', cmap=self.config.color_map, origin='lower', interpolation=self.config.color_interp)
            ax_cost.set_title(f'a = {a}', fontsize=self.config.title_fontsize, fontweight='bold')
            ax_cost.set_xticks(range(len(strategy_params)))
            ax_cost.set_xticklabels([sp.split('=')[1] for sp in strategy_params], fontsize=8)
            n_ticks = min(11, len(theta_values))
            tick_step = max(1, len(theta_values) // n_ticks)
            ax_cost.set_yticks(range(0, len(theta_values), tick_step))
            ax_cost.set_yticklabels([f"{theta_values[i]:.1f}" for i in range(0, len(theta_values), tick_step)], fontsize=8)
            if col_idx == 0:
                ax_cost.set_ylabel('Total Cost\n\nθ', fontsize=self.config.label_fontsize)
            plt.colorbar(im_cost, ax=ax_cost)

            # Row 1: Social Welfare
            ax_welfare = axes[1, col_idx]
            im_welfare = ax_welfare.imshow(welfare_a, aspect='auto', cmap=self.config.color_map, origin='lower', interpolation=self.config.color_interp)
            is_neb = strategy_params[0].startswith('nc')
            ax_welfare.set_xlabel('$n_C$' if is_neb else '$p_C$', fontsize=self.config.label_fontsize)
            ax_welfare.set_xticks(range(len(strategy_params)))
            ax_welfare.set_xticklabels([sp.split('=')[1] for sp in strategy_params], fontsize=8)
            ax_welfare.set_yticks(range(0, len(theta_values), tick_step))
            ax_welfare.set_yticklabels([f"{theta_values[i]:.1f}" for i in range(0, len(theta_values), tick_step)], fontsize=8)
            if col_idx == 0:
                ax_welfare.set_ylabel('Social Welfare\n\nθ', fontsize=self.config.label_fontsize)
            plt.colorbar(im_welfare, ax=ax_welfare)

        if title:
            fig.suptitle(title, fontsize=14, y=1.02)

        plt.tight_layout()

        if output_filename:
            save_figure(fig, output_filename, self.config.dpi, show_plot)
        else:
            plt.show()

        return output_filename

    def plot_diff_plot_from_agg(
        self,
        data_matrices: Dict[str, np.ndarray],
        strategy_params: List[str],
        theta_values: List[float],
        a_values: List[float],
        title: str = '',
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ):
        """
        Plot different line plot from pre-aggregated final values.

        Args:
            data_matrices: {'cost': array, 'welfare': array, 'coop_freq': array} with shape [theta, param]
            strategy_params: List of strategy param labels
            theta_values: List of theta values
            title: Plot title
        """
        
        if 'pc' in strategy_params[0]: # plot for POP
            return self._plot_diff_plot_from_agg_pop(
                data_matrices, strategy_params, theta_values, a_values, title, output_filename, show_plot
            )
        return self._plot_diff_plot_from_agg_neb(
            data_matrices, strategy_params, theta_values, a_values, title, output_filename, show_plot
        )

    def _plot_diff_plot_from_agg_pop(
        self,
        data_matrices: Dict[str, np.ndarray],
        strategy_params: List[str],
        theta_values: List[float],
        a_values: List[float],
        title: str = '',
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ):
        """
        Plot POP line plot from pre-aggregated final values.

        Args:
            data_matrices: {'cost': array, 'welfare': array, 'coop_freq': array} with shape [theta, param]
            strategy_params: List of strategy param labels
            theta_values: List of theta values
            title: Plot title
        """
        n_cols = len(a_values)
        fig, axes = plt.subplots(1, n_cols, figsize=(15, 4))

        for i, a in enumerate(a_values):
            cost_a = data_matrices['cost'] / a
            welfare_a = data_matrices['welfare'] - cost_a
            coop_freq_nc3_to_compare = data_matrices['coop_freq'][:, len(strategy_params) - 1]
            cost_nc3_to_compare = cost_a[:, len(strategy_params) - 1]
            sw_nc3_to_compare = welfare_a[:, len(strategy_params) - 1]
            cost_nc3_min = theta_values[np.where(coop_freq_nc3_to_compare > 90)[0][0]]
            sw_nc3_max = theta_values[np.where(sw_nc3_to_compare/max(sw_nc3_to_compare) == 1)[0][0]]

            coef = 1
            if (cost_nc3_min > sw_nc3_max):
                coef = -1

            axes[i].plot(sorted(theta_values), (cost_nc3_to_compare - min(cost_nc3_to_compare))/(max(cost_nc3_to_compare) - min(cost_nc3_to_compare)), color='red', label='Total Cost')
            axes[i].plot(sorted(theta_values), (sw_nc3_to_compare - min(sw_nc3_to_compare))/(max(sw_nc3_to_compare) - min(sw_nc3_to_compare)), label='Social Welfare')
            axes[i].axhline(0.9, color='gray', linestyle=':', alpha=0.5, label='>90% coop')
            axes[i].axhline(0.9, xmin=(0.2)/(coef*(sw_nc3_max - cost_nc3_min) + 0.4), xmax=(coef*(sw_nc3_max-cost_nc3_min)+0.2)/(coef*(sw_nc3_max - cost_nc3_min) + 0.4), color ='green', linestyle='--')
            axes[i].axvline(cost_nc3_min, linestyle='--', color='red')
            axes[i].axvline(sw_nc3_max, linestyle='--')
            axes[i].text(cost_nc3_min+0.01, 0.5, round(cost_nc3_min, 1), rotation=90, va='center')
            axes[i].text(sw_nc3_max+0.01, 0.5, round(sw_nc3_max, 1), rotation=90, va='center')
            axes[i].text((cost_nc3_min + sw_nc3_max)/2, 0.92, 'Δθ', va='center')
            axes[i].plot([cost_nc3_min], [0.9], color='green', marker="o")
            axes[i].plot([sw_nc3_max], [0.9], color='green', marker="o")
            if (coef == -1):
                axes[i].set_xlim(sw_nc3_max - 0.2, cost_nc3_min + 0.2)
            else:
                axes[i].set_xlim(cost_nc3_min - 0.2, sw_nc3_max + 0.2)
            axes[i].set_ylim(0, 1.1)
            axes[i].set_xlabel('Per-individual investment cost, θ', fontsize=self.config.label_fontsize)
            axes[i].set_ylabel('Normalized Value', fontsize=self.config.label_fontsize)
            axes[i].set_title(f'{strategy_params[len(strategy_params) - 1]}, a={a}', fontsize=self.config.title_fontsize, fontweight='bold')

        handles, labels = axes[0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1))
        
        if title:
            fig.suptitle(title, fontsize=14, y=1.05)
        
        plt.tight_layout()

        if output_filename:
            save_figure(fig, output_filename, self.config.dpi, show_plot)
        else:
            plt.show()

        return output_filename

    def _plot_diff_plot_from_agg_neb(
        self,
        data_matrices: Dict[str, np.ndarray],
        strategy_params: List[str],
        theta_values: List[float],
        a_values: List[float],
        title: str = '',
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ):
        """
        Plot NEB line plot from pre-aggregated final values.

        Args:
            data_matrices: {'cost': array, 'welfare': array, 'coop_freq': array} with shape [theta, param]
            strategy_params: List of strategy param labels
            theta_values: List of theta values
            title: Plot title
        """
        n_cols = len(a_values)
        n_rows = 2 # Plot for nc=3 and nc=4
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(15, 8))
        for i in range(n_rows):
            for j in range(n_cols):
                a = a_values[j]
                cost_a = data_matrices['cost'] / a
                welfare_a = data_matrices['welfare'] - cost_a
                coop_freq_nc3_to_compare = data_matrices['coop_freq'][:, len(strategy_params) - 2 + i]
                cost_nc3_to_compare = cost_a[:, len(strategy_params) - 2 + i]
                sw_nc3_to_compare = welfare_a[:, len(strategy_params) - 2 + i]
                cost_nc3_min = theta_values[np.where(coop_freq_nc3_to_compare > 90)[0][0]]
                sw_nc3_max = theta_values[np.where(sw_nc3_to_compare/max(sw_nc3_to_compare) == 1)[0][0]]
                
                coef = 1
                if (cost_nc3_min > sw_nc3_max):
                    coef = -1

                axes[i][j].plot(sorted(theta_values), (cost_nc3_to_compare - min(cost_nc3_to_compare))/(max(cost_nc3_to_compare) - min(cost_nc3_to_compare)), color='red', label='Total Cost')
                axes[i][j].plot(sorted(theta_values), (sw_nc3_to_compare - min(sw_nc3_to_compare))/(max(sw_nc3_to_compare) - min(sw_nc3_to_compare)), label='Social Welfare')
                axes[i][j].axhline(0.9, color='gray', linestyle=':', alpha=0.5, label='>90% coop')
                axes[i][j].axhline(0.9, xmin=(0.2)/(coef*(sw_nc3_max - cost_nc3_min) + 0.4), xmax=(coef*(sw_nc3_max-cost_nc3_min)+0.2)/(coef*(sw_nc3_max - cost_nc3_min) + 0.4), color ='green', linestyle='--')
                axes[i][j].axvline(cost_nc3_min, linestyle='--', color='red')
                axes[i][j].axvline(sw_nc3_max, linestyle='--')
                axes[i][j].text(cost_nc3_min+0.01, 0.5, round(cost_nc3_min, 1), rotation=90, va='center')
                axes[i][j].text(sw_nc3_max+0.01, 0.5, round(sw_nc3_max, 1), rotation=90, va='center')
                axes[i][j].text((cost_nc3_min + sw_nc3_max)/2, 0.92, 'Δθ', va='center')
                axes[i][j].plot([cost_nc3_min], [0.9], color='green', marker="o")
                axes[i][j].plot([sw_nc3_max], [0.9], color='green', marker="o")
                if (coef == 1):
                    axes[i][j].set_xlim(cost_nc3_min - 0.2, sw_nc3_max + 0.2)
                else:
                    axes[i][j].set_xlim(sw_nc3_max - 0.2, cost_nc3_min + 0.2)
                axes[i][j].set_xlabel('Per-individual investment cost, θ', fontsize=self.config.label_fontsize)
                axes[i][j].set_ylabel('Normalized Value', fontsize=self.config.label_fontsize)
                axes[i][j].set_title(f'{strategy_params[len(strategy_params) - 2 + i]}, a={a}', fontsize=self.config.title_fontsize, fontweight='bold')

        handles, labels = axes[0][0].get_legend_handles_labels()
        fig.legend(handles, labels, loc='upper center', ncol=3, bbox_to_anchor=(0.5, 1))

        if title:
            fig.suptitle(title, fontsize=14, y=1.05)

        plt.tight_layout()

        if output_filename:
            save_figure(fig, output_filename, self.config.dpi, show_plot)
        else:
            plt.show()

        return output_filename

    def plot_optimal_theta_summary(
        self,
        optimal_sw: Dict[float, Dict[str, Dict[str, Dict[str, Dict[str, float]]]]],
        optimal_cost: Dict[float, Dict[str, Dict[str, Dict[str, Dict[str, float]]]]],
        a_values: List[float],
        title: str = '',
        output_filename: Optional[str] = None,
        show_plot: bool = False
    ):
        """
        Plot grid showing θ* vs strategy params. Scatter only (no lines).
        Filled markers = SW optimal, hollow markers = Cost optimal.
        Rows = a values, Columns = game × strategy.

        Args:
            optimal_sw: {a: {game: {strategy: {game_param: {sp: theta_star}}}}}
            optimal_cost: same structure but for cost
            a_values: List of efficiency values
        """
        game_labels = {'pd': 'PD', 'pgg': 'PGG'}
        strategy_labels = {'pop': 'POP', 'neb': 'NEB'}
        game_param_display = {
            'pd': ['b=1.2', 'b=1.8', 'b=2.0'],
            'pgg': ['r=1.5', 'r=3.0', 'r=4.5'],
        }

        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']
        markers = ['o', 's', '^']

        games = sorted(optimal_sw[a_values[0]].keys())
        output_files = []

        for game in games:
            n_rows = len(a_values)
            fig, axes = plt.subplots(n_rows, 2, figsize=(10, 4 * n_rows))
            if n_rows == 1:
                axes = axes[np.newaxis, :]

            for row_idx, a in enumerate(a_values):
                for col, strategy in enumerate(['pop', 'neb']):
                    ax = axes[row_idx, col]
                    sw_strat = optimal_sw.get(a, {}).get(game, {}).get(strategy, {})
                    cost_strat = optimal_cost.get(a, {}).get(game, {}).get(strategy, {})

                    if not sw_strat:
                        ax.text(0.5, 0.5, 'No data', ha='center', va='center', transform=ax.transAxes)
                        continue

                    # Spread annotations per game_param index to avoid overlap
                    sw_offsets = [(-18, 8), (5, 8), (12, -10)]
                    cost_offsets = [(-18, -12), (5, -12), (12, 4)]

                    for idx, game_param in enumerate(sorted(sw_strat.keys())):
                        sp_data_sw = sw_strat[game_param]
                        sp_data_cost = cost_strat.get(game_param, {})

                        sp_vals = sorted(sp_data_sw.keys(), key=lambda x: float(x.split('=')[1]))
                        x_vals = [float(sp.split('=')[1]) for sp in sp_vals]
                        y_sw = [sp_data_sw[sp] for sp in sp_vals]

                        color = colors[idx % len(colors)]
                        marker = markers[idx % len(markers)]
                        sw_off = sw_offsets[idx % len(sw_offsets)]
                        cost_off = cost_offsets[idx % len(cost_offsets)]

                        for sp_i, sp in enumerate(sp_vals):
                            x = x_vals[sp_i]
                            theta_sw = y_sw[sp_i]
                            cost_info = sp_data_cost.get(sp, {})
                            feasible = cost_info.get('feasible', True)

                            if not feasible:
                                continue

                            # SW point (filled)
                            ax.scatter([x], [theta_sw], marker=marker, color=color, s=60, zorder=3)
                            ax.annotate(f'{theta_sw:.1f}', (x, theta_sw),
                                        textcoords='offset points', xytext=sw_off,
                                        fontsize=5.5, color=color)

                            # Cost point (hollow)
                            theta_c = cost_info.get('theta', 0)
                            ax.scatter([x], [theta_c], marker=marker, facecolors='none',
                                       edgecolors=color, s=60, linewidths=1.5, zorder=3)
                            ax.annotate(f'{theta_c:.1f}', (x, theta_c),
                                        textcoords='offset points', xytext=cost_off,
                                        fontsize=5.5, color=color)

                    ax.set_xlabel('$p_C$' if strategy == 'pop' else '$n_C$', fontsize=self.config.label_fontsize)
                    ax.set_xticks(x_vals)
                    ax.grid(True, alpha=0.3)
                    ax.autoscale(axis='y')
                    y_min, y_max = ax.get_ylim()
                    margin = (y_max - y_min) * 0.15
                    ax.set_ylim(y_min - margin, y_max + margin)

                    if col == 0:
                        ax.set_ylabel(f'a={a}\nθ*', fontsize=self.config.label_fontsize)
                    if row_idx == 0:
                        ax.set_title(strategy_labels[strategy],
                                     fontsize=self.config.title_fontsize)

            from matplotlib.lines import Line2D
            legend_handles = []
            for idx, param_label in enumerate(game_param_display[game]):
                legend_handles.append(Line2D([0], [0], marker=markers[idx], color='w',
                                             markerfacecolor=colors[idx], markersize=8,
                                             label=param_label))
            legend_handles.append(Line2D([0], [0], marker='o', color='w',
                                         markerfacecolor='gray', markersize=8, label='Filled = SW'))
            legend_handles.append(Line2D([0], [0], marker='o', color='w',
                                         markerfacecolor='none', markeredgecolor='gray',
                                         markeredgewidth=1.5, markersize=8, label='Hollow = Cost'))
            fig.legend(handles=legend_handles, loc='upper center', ncol=5,
                       bbox_to_anchor=(0.5, 1.0), fontsize=10, frameon=True)

            game_title = f'{title} — {game_labels[game]}' if title else game_labels[game]
            fig.suptitle(game_title, fontsize=14, y=1.05)
            plt.tight_layout(rect=[0, 0, 1, 0.96])

            if output_filename:
                base, ext = os.path.splitext(output_filename)
                out = f'{base}_{game}{ext}'
                save_figure(fig, out, self.config.dpi, show_plot)
                output_files.append(out)
            else:
                plt.show()

        return output_files
