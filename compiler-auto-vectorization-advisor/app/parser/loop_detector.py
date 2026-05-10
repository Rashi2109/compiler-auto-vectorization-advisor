from clang import cindex

# Set the library path for libclang on macOS
cindex.conf.set_library_file('/opt/homebrew/opt/llvm/lib/libclang.dylib')

class LoopDetector:

    def __init__(self, file_path):
        self.file_path = file_path
        self.loops = []
        self.file_content = None

    def detect_loops(self):

        # Read file content
        with open(self.file_path, 'r') as f:
            self.file_content = f.readlines()

        # Create Clang Index
        index = cindex.Index.create()

        # Parse C file
        translation_unit = index.parse(self.file_path)

        # Traverse AST
        self.traverse_ast(translation_unit.cursor)

        return self.loops

    def get_loop_code(self, node):
        """Extract the code of the loop"""
        start_line = node.location.line - 1
        end_line = node.extent.end.line

        if self.file_content and start_line < len(self.file_content):
            code_lines = self.file_content[start_line:end_line]
            return ''.join(code_lines).strip()
        return ""

    def traverse_ast(self, node):

        # Detect FOR loops
        if node.kind == cindex.CursorKind.FOR_STMT:

            loop_code = self.get_loop_code(node)

            loop_info = {
                "type": "for",
                "line": node.location.line,
                "column": node.location.column,
                "code": loop_code
            }

            self.loops.append(loop_info)

        # Detect WHILE loops
        elif node.kind == cindex.CursorKind.WHILE_STMT:

            loop_code = self.get_loop_code(node)

            loop_info = {
                "type": "while",
                "line": node.location.line,
                "column": node.location.column,
                "code": loop_code
            }

            self.loops.append(loop_info)

        # Recursively traverse children
        for child in node.get_children():
            self.traverse_ast(child)
