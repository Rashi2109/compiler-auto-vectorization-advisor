import re


class DependencyChecker:

    def __init__(self, loop_code):

        self.loop_code = loop_code

    def check_dependency(self):

        """
        Detect patterns like:
        a[i] = a[i-1] + 1

        If same array appears with i-1,
        dependency exists.
        """

        # Detect array accesses
        accesses = re.findall(r'([a-zA-Z_]\w*)\s*\[(.*?)\]', self.loop_code)

        arrays = {}

        for array_name, index_expr in accesses:

            if array_name not in arrays:
                arrays[array_name] = []

            arrays[array_name].append(index_expr)

        # Dependency detection
        for array_name, indices in arrays.items():

            has_current = False
            has_previous = False

            for idx in indices:

                idx = idx.replace(" ", "")

                if idx == "i":
                    has_current = True

                if "i-1" in idx or "i - 1" in idx:
                    has_previous = True

            if has_current and has_previous:

                return {
                    "dependency": True,
                    "array": array_name,
                    "message": f"Dependency detected in array '{array_name}'"
                }

        return {
            "dependency": False,
            "message": "No dependency detected"
        }
