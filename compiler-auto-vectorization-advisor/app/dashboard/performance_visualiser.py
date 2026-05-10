import matplotlib
matplotlib.use('agg')  # Use non-interactive backend for web applications
import matplotlib.pyplot as plt


class PerformanceVisualizer:

    def __init__(self, benchmark_results):

        self.results = benchmark_results

    def generate_execution_time_graph(self):

        labels = []
        execution_times = []

        for result in self.results:

            label = f"{result['compiler']}\n{result['flag']}"

            labels.append(label)

            execution_times.append(result['time'])

        plt.figure(figsize=(10, 6))

        bars = plt.bar(labels, execution_times)

        plt.xlabel("Compiler + Flag")
        plt.ylabel("Execution Time")
        plt.title("Cross Compiler Benchmark")

        for bar, time in zip(bars, execution_times):

            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f"{time:.4f}",
                ha='center',
                va='bottom'
            )

        plt.tight_layout()

        plt.savefig(
            "static/reports/execution_time_comparison.png"
        )

        plt.close()

    def generate_speedup_graph(self):

        baseline = max(result['time'] for result in self.results)

        labels = []
        speedups = []

        for result in self.results:

            label = f"{result['compiler']}\n{result['flag']}"

            speedup = baseline / result['time']

            labels.append(label)

            speedups.append(speedup)

        plt.figure(figsize=(10, 6))

        bars = plt.bar(labels, speedups)

        plt.xlabel("Compiler + Flag")
        plt.ylabel("Speedup")
        plt.title("Speedup Analysis")

        for bar, speedup in zip(bars, speedups):

            plt.text(
                bar.get_x() + bar.get_width()/2,
                bar.get_height(),
                f"{speedup:.2f}x",
                ha='center',
                va='bottom'
            )

        plt.tight_layout()

        plt.savefig(
            "static/reports/speedup_analysis.png"
        )

        plt.close()
