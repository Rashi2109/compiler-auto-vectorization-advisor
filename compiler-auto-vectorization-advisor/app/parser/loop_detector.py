from clang import cindex
import platform
import os


# -----------------------------------
# LIBCLANG CONFIGURATION
# -----------------------------------

system_name = platform.system()

# macOS
if system_name == "Darwin":

    possible_paths = [

        "/opt/homebrew/opt/llvm/lib/libclang.dylib",

        "/usr/local/opt/llvm/lib/libclang.dylib"
    ]

# Linux (GitHub Actions / Ubuntu)
elif system_name == "Linux":

    possible_paths = [

        "/usr/lib/llvm-14/lib/libclang.so.1"
    ]


# -----------------------------------
# AUTO DETECT LIBCLANG
# -----------------------------------

for path in possible_paths:

    if os.path.exists(path):

        cindex.Config.set_library_file(path)

        print(f"Using libclang: {path}")

        break


# -----------------------------------
# LOOP DETECTOR CLASS
# -----------------------------------

class LoopDetector:

    def __init__(self, filename):

        self.filename = filename

        self.loops = []


    # --------------------------------
    # DETECT LOOPS
    # --------------------------------
    def detect_loops(self):

        index = cindex.Index.create()

        translation_unit = index.parse(
            self.filename
        )

        self.visit_nodes(
            translation_unit.cursor
        )

        return self.loops


    # --------------------------------
    # VISIT AST NODES
    # --------------------------------
    def visit_nodes(self, node):

        loop_kinds = [

            cindex.CursorKind.FOR_STMT,

            cindex.CursorKind.WHILE_STMT,

            cindex.CursorKind.DO_STMT
        ]

        if node.kind in loop_kinds:

            self.loops.append({

                "type": str(node.kind).split(".")[-1],

                "line": node.location.line,

                "code": self.get_source_code(
                    node
                )
            })

        for child in node.get_children():

            self.visit_nodes(child)


    # --------------------------------
    # GET SOURCE CODE
    # --------------------------------
    def get_source_code(self, node):

        try:

            with open(self.filename, "r") as file:

                lines = file.readlines()

            start = node.extent.start.line - 1

            end = node.extent.end.line

            return "".join(lines[start:end])

        except Exception as e:

            return f"Source code unavailable: {e}"
