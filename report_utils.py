from fpdf import FPDF
from datetime import datetime

def save_report_to_pdf(results: list, candidate_name="Candidate", avg_score=None, filename="interview_report.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    # 📝 Set the report title
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, txt="Candidate Interview Report", ln=True, align="C")
    pdf.ln(4)

    # 🧑‍💼 Add candidate name and interview date
    interview_date = datetime.now().strftime("%B %d, %Y")
    pdf.set_font("Arial", "", 12)
    pdf.cell(100, 10, txt=f"Candidate: {candidate_name}", ln=True)
    pdf.cell(100, 10, txt=f"Date: {interview_date}", ln=True)

    # 📊 Add overall average score (if available)
    if avg_score is not None:
        pdf.set_font("Arial", "B", 12)
        pdf.cell(100, 10, txt=f"Overall Score: {avg_score:.2f}/10", ln=True)

    pdf.ln(8)  # Add space before questions

    # 🔄 Loop through all Q&A results and write them out
    for idx, result in enumerate(results, start=1):
        # Question text with emphasis
        pdf.set_font("Arial", "B", 12)
        pdf.set_text_color(0, 0, 128)  # Dark blue
        pdf.multi_cell(0, 10, f"Q{idx}: {result['question']}")

        # Reset style for answer text
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", "", 12)
        pdf.multi_cell(0, 10, f"Answer: {result['answer']}")

        # Numeric score
        pdf.cell(0, 10, txt=f"Score: {result['score']}/10", ln=True)

        # Evaluator comment
        pdf.multi_cell(0, 10, f"Comment: {result['comment']}")

        # High-level summary (in grey)
        pdf.set_text_color(105, 105, 105)  # grey
        pdf.multi_cell(0, 10, f"Summary: {result['summary']}")
        pdf.set_text_color(0, 0, 0)  # reset to black

        # Optional follow-up note, if present
        if result["follow_up"]:
            pdf.set_text_color(34, 139, 34)  # green
            pdf.multi_cell(0, 10, f"Follow-up: {result['follow_up']}")
            pdf.set_text_color(0, 0, 0)  # reset to black

        pdf.ln(5)  # Add space between entries

    # 📄 Save the final PDF to disk
    pdf.output(filename)
    print(f"\n📄 PDF saved to: {filename}")
