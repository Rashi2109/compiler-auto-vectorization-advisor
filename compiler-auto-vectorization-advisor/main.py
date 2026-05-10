from flask import Flask, render_template, request
import os
import webbrowser

from app.parser.loop_detector import LoopDetector
from app.analyzer.dependency_checker import DependencyChecker
from app.optimizer.recommendation_engine import RecommendationEngine
from app.benchmark.benchmark_runner import BenchmarkRunner
from app.dashboard.performance_visualiser import PerformanceVisualizer


# ------------------------------------------------
# FLASK APP
# ------------------------------------------------
app = Flask(
    __name__,
    template_folder="app/templates"
)

# ------------------------------------------------
# FOLDERS
# ------------------------------------------------
UPLOAD_FOLDER = "uploads"

STATIC_REPORTS = "static/reports"

# Create folders automatically
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

os.makedirs(STATIC_REPORTS, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# ------------------------------------------------
# HOME PAGE
# ------------------------------------------------
@app.route("/")
def home():

    return render_template("index.html")


# ------------------------------------------------
# ANALYZE ROUTE
# ------------------------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    try:

        # ----------------------------------------
        # FILE UPLOAD
        # ----------------------------------------
        uploaded_file = request.files.get("codefile")

        if not uploaded_file:
            return "No file uploaded"

        if not uploaded_file.filename or uploaded_file.filename == "":
            return "No file selected"

        # Save uploaded file
        file_path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            str(uploaded_file.filename)
        )

        uploaded_file.save(file_path)

        # ----------------------------------------
        # LOOP DETECTION
        # ----------------------------------------
        detector = LoopDetector(file_path)

        loops = detector.detect_loops()

        analysis_output = ""

        # ----------------------------------------
        # LOOP ANALYSIS
        # ----------------------------------------
        if loops:

            for idx, loop in enumerate(loops, start=1):

                analysis_output += (
                    f"\n========== LOOP #{idx} ==========\n"
                )

                analysis_output += (
                    f"Loop Type : {loop['type']}\n"
                )

                analysis_output += (
                    f"Line No   : {loop['line']}\n"
                )

                analysis_output += (
                    "\nLoop Code:\n"
                )

                analysis_output += (
                    loop["code"] + "\n"
                )

                # --------------------------------
                # DEPENDENCY ANALYSIS
                # --------------------------------
                checker = DependencyChecker(
                    loop["code"]
                )

                dependency_result = (
                    checker.check_dependency()
                )

                analysis_output += (
                    "\n===== DEPENDENCY ANALYSIS =====\n"
                )

                if dependency_result["dependency"]:

                    analysis_output += (
                        "Dependency Found : YES\n"
                    )

                    analysis_output += (
                        "Vectorizable     : NO\n"
                    )

                else:

                    analysis_output += (
                        "Dependency Found : NO\n"
                    )

                    analysis_output += (
                        "Vectorizable     : YES\n"
                    )

                # --------------------------------
                # RECOMMENDATIONS
                # --------------------------------
                engine = RecommendationEngine(
                    loop["code"],
                    dependency_result
                )

                recommendations = (
                    engine.generate_recommendations()
                )

                analysis_output += (
                    "\n===== OPTIMIZATION "
                    "RECOMMENDATIONS =====\n"
                )

                for rec in recommendations:

                    analysis_output += (
                        f"- {rec}\n"
                    )

                analysis_output += (
                    "\n"
                    + "=" * 60
                    + "\n"
                )

        else:

            analysis_output = (
                "No loops detected."
            )

        # ----------------------------------------
        # BENCHMARKING
        # ----------------------------------------
        benchmark_output = ""

        try:

            benchmark = BenchmarkRunner(
                file_path
            )

            results = benchmark.benchmark()

            benchmark_output += (
                "\n===== CROSS COMPILER "
                "BENCHMARK =====\n\n"
            )

            for result in results:

                benchmark_output += (
                    f"Compiler : "
                    f"{result['compiler']}\n"
                )

                benchmark_output += (
                    f"Flag     : "
                    f"{result['flag']}\n"
                )

                benchmark_output += (
                    f"Time     : "
                    f"{result['time']:.6f} sec\n"
                )

                benchmark_output += (
                    "-" * 40 + "\n"
                )

            # ------------------------------------
            # BEST RESULT
            # ------------------------------------
            best = benchmark.get_best_result()

            if best:

                benchmark_output += (
                    "\n===== BEST CONFIGURATION =====\n"
                )

                benchmark_output += (
                    f"Best Compiler : "
                    f"{best['compiler']}\n"
                )

                benchmark_output += (
                    f"Best Flag     : "
                    f"{best['flag']}\n"
                )

                benchmark_output += (
                    f"Execution Time: "
                    f"{best['time']:.6f} sec\n"
                )

            # ------------------------------------
            # GRAPH GENERATION
            # ------------------------------------
            visualizer = (
                PerformanceVisualizer(results)
            )

            visualizer.generate_execution_time_graph()

            visualizer.generate_speedup_graph()

        except Exception as benchmark_error:

            benchmark_output = (
                f"Benchmark Error:\n"
                f"{str(benchmark_error)}"
            )

        # ----------------------------------------
        # RENDER RESULTS PAGE
        # ----------------------------------------
        return render_template(
            "results.html",
            analysis=analysis_output,
            benchmark=benchmark_output
        )

    except Exception as e:

        return f"Application Error: {str(e)}"


# ------------------------------------------------
# MAIN
# ------------------------------------------------
if __name__ == "__main__":

    webbrowser.open(
        "http://127.0.0.1:5000"
    )

    app.run(
        debug=True,
        use_reloader=False
    )
