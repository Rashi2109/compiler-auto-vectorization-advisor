import re


class FeatureExtractor:

    def __init__(self, loop_code):

        self.loop_code = loop_code

    def extract_loop_size(self):

        pattern = r'i\s*<\s*(\d+)'

        match = re.search(pattern, self.loop_code)

        if match:

            return int(match.group(1))

        return 100

    def count_array_accesses(self):

        accesses = re.findall(
            r'[a-zA-Z_]\w*\s*\[.*?\]',
            self.loop_code
        )

        return len(accesses)
