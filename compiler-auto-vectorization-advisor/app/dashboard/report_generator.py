from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)

from reportlab.lib.styles import (
    getSampleStyleSheet
)

import os


class ReportGenerator:

    def __init__(self, analysis, benchmark):

        self.analysis = analysis

        self.benchmark = benchmark

        self.output_path = (
            "static/reports/"
            "optimization_report.pdf"
        )


    # --------------------------------
    # GENERATE PDF REPORT
    # --------------------------------
    def generate_pdf(self):

        os.makedirs(
            "static/reports",
            exist_ok=True
        )

        doc = SimpleDocTemplate(
            self.output_path
        )

        styles = (
            getSampleStyleSheet()
        )

        elements = []

        title = Paragraph(
            "Compiler Optimization Report",
            styles['Title']
        )

        elements.append(title)

        elements.append(
            Spacer(1, 20)
        )

        # Analysis Section
        analysis_title = Paragraph(
            "Loop Analysis",
            styles['Heading2']
        )

        elements.append(
            analysis_title
        )

        analysis_text = Paragraph(
            self.analysis.replace(
                "\n",
                "<br/>"
            ),
            styles['BodyText']
        )

        elements.append(
            analysis_text
        )

        elements.append(
            Spacer(1, 20)
        )

        # Benchmark Section
        benchmark_title = Paragraph(
            "Benchmark Results",
            styles['Heading2']
        )

        elements.append(
            benchmark_title
        )

        benchmark_text = Paragraph(
            self.benchmark.replace(
                "\n",
                "<br/>"
            ),
            styles['BodyText']
        )

        elements.append(
            benchmark_text
        )

        doc.build(elements)

        print(
            "PDF report generated successfully"
        )
