import subprocess
import time
import os


class BenchmarkRunner:

    def __init__(self, source_file):

        self.source_file = source_file

        self.compilers = {
            "gcc": "gcc",
            "clang": "clang"
        }

        self.optimization_flags = [
            "-O1",
            "-O2",
            "-O3",
            "-Ofast"
        ]

        self.results = []

    def compile_code(self, compiler, flag, output_name):

        command = [
            compiler,
            flag,
            self.source_file,
            "-o",
            output_name
        ]

        try:

            subprocess.run(
                command,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            return True

        except subprocess.CalledProcessError as e:

            print(f"Compilation failed: {e}")

            return False

    def run_executable(self, executable):

        start_time = time.perf_counter()

        subprocess.run(
            executable,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        end_time = time.perf_counter()

        execution_time = end_time - start_time

        return execution_time

    def benchmark(self):

        for compiler_name, compiler_cmd in self.compilers.items():

            for flag in self.optimization_flags:

                output_file = f"temp_{compiler_name}_{flag.replace('-', '')}"

                # Windows executable handling
                if os.name == "nt":
                    output_file += ".exe"

                # Compile
                success = self.compile_code(
                    compiler_cmd,
                    flag,
                    output_file
                )

                if success:

                    # Run benchmark
                    execution_time = self.run_executable(
                        f"./{output_file}" if os.name != "nt" else output_file
                    )

                    result = {
                        "compiler": compiler_name,
                        "flag": flag,
                        "time": execution_time
                    }

                    self.results.append(result)

                    # Cleanup executable
                    if os.path.exists(output_file):
                        os.remove(output_file)

        return self.results

    def get_best_result(self):

        if not self.results:
            return None

        return min(self.results, key=lambda x: x["time"])
