import re


class RecommendationEngine:

    def __init__(self, loop_code, dependency_result):

        self.loop_code = loop_code
        self.dependency_result = dependency_result

    def extract_loop_bound(self):

        """
        Extract loop bound from:
        for(int i=0; i<100; i++)

        Returns:
        100
        """

        pattern = r'i\s*<\s*(\d+)'

        match = re.search(pattern, self.loop_code)

        if match:
            return int(match.group(1))

        return None

    def generate_recommendations(self):

        recommendations = []

        loop_bound = self.extract_loop_bound()

        # CASE 1 — Dependency exists
        if self.dependency_result["dependency"]:

            recommendations.append(
                "Avoid SIMD vectorization due to data dependency"
            )

            recommendations.append(
                "Sequential execution recommended"
            )

            return recommendations

        # CASE 2 — Vectorizable loop
        recommendations.append(
            "Apply SIMD vectorization"
        )

        # CASE 3 — Small loop unrolling
        if loop_bound is not None:

            if loop_bound <= 8:

                recommendations.append(
                    "Apply full loop unrolling"
                )

            elif loop_bound <= 100:

                recommendations.append(
                    "Unroll loop by factor 4"
                )

            else:

                recommendations.append(
                    "Unroll loop by factor 8"
                )

        # CASE 4 — Memory optimization hint
        recommendations.append(
            "Enable compiler optimization flags (-O3 or -Ofast)"
        )

        return recommendations
