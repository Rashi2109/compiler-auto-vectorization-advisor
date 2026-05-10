from flask import Flask, render_template, request
import os

from app.parser.loop_detector import LoopDetector
from app.analyzer.dependency_checker import DependencyChecker
from app.optimizer.recommendation_engine import RecommendationEngine
from app.benchmark.benchmark_runner import BenchmarkRunner
from app.dashboard.performance_visualiser import PerformanceVisualizer

from app.ML.ml_predictor import MLPredictor
from app.ML.feature_extractor import FeatureExtractor


app = Flask(__name__)

# -----------------------------------
# CONFIGURATION
# -----------------------------------
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create upload folder if not exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# -----------------------------------
# HOME PAGE
# -----------------------------------
@app.route("/")
def home():

    return render_template("index.html")


# -----------------------------------
# ANALYSIS ROUTE
# -----------------------------------
@app.route("/analyze", methods=["POST"])
def analyze():

    uploaded_file = request.files.get("codefile")

    if not uploaded_file or not uploaded_file.filename or uploaded_file.filename == "":
        return "No file selected"

    # -----------------------------------
    # SAVE FILE
    # -----------------------------------
    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        uploaded_file.filename
    )

    uploaded_file.save(file_path)

    # -----------------------------------
    # TRAIN ML MODEL
    # -----------------------------------
    ml_model = MLPredictor()

    ml_model.train_model()

    # -----------------------------------
    # LOOP DETECTION
    # -----------------------------------
    detector = LoopDetector(file_path)

    loops = detector.detect_loops()

    analysis_output = ""

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

            # -----------------------------------
            # DEPENDENCY ANALYSIS
            # -----------------------------------
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

            # -----------------------------------
            # FEATURE EXTRACTION
            # -----------------------------------
            extractor = FeatureExtractor(
                loop["code"]
            )

            loop_size = (
                extractor.extract_loop_size()
            )

            array_accesses = (
                extractor.count_array_accesses()
            )

            dependency_value = (
                1 if dependency_result["dependency"]
                else 0
            )

            analysis_output += (
                f"Loop Size         : {loop_size}\n"
            )

            analysis_output += (
                f"Array Accesses    : "
                f"{array_accesses}\n"
            )

            # -----------------------------------
            # ML PREDICTION
            # -----------------------------------
            prediction = (
                ml_model.predict_best_optimization(
                    dependency_value,
                    loop_size,
                    array_accesses
                )
            )

            analysis_output += (
                f"ML Prediction     : "
                f"{prediction}\n"
            )

            # -----------------------------------
            # OPTIMIZATION RECOMMENDATIONS
            # -----------------------------------
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

    # -----------------------------------
    # BENCHMARKING
    # -----------------------------------
    benchmark = BenchmarkRunner(
        file_path
    )

    results = benchmark.benchmark()

    benchmark_output = (
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

    # -----------------------------------
    # BEST RESULT
    # -----------------------------------
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

    # -----------------------------------
    # GRAPH GENERATION
    # -----------------------------------
    visualizer = PerformanceVisualizer(
        results
    )

    visualizer.generate_execution_time_graph()

    visualizer.generate_speedup_graph()

    # -----------------------------------
    # RETURN RESULTS
    # -----------------------------------
    return render_template(
        "results.html",
        analysis=analysis_output,
        benchmark=benchmark_output
    )


# -----------------------------------
# MAIN ENTRY
# -----------------------------------
if __name__ == "__main__":

    app.run(
        debug=True,
        use_reloader=False
    )
