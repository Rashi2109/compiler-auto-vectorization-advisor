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

        "/usr/lib/llvm-14/lib/libclang.so.1",

        "/usr/lib/llvm-15/lib/libclang.so.1",

        "/usr/lib/llvm-16/lib/libclang.so.1",

        "/usr/lib/x86_64-linux-gnu/libclang-14.so.1",

        "/usr/lib/x86_64-linux-gnu/libclang-15.so.1"
    ]

# -----------------------------------
# AUTO DETECT VALID PATH
# -----------------------------------

for path in possible_paths:

    if os.path.exists(path):

        cindex.Config.set_library_file(path)

        print(f"Using libclang: {path}")

        break
