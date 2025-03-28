# Core app imports for handling job descriptions, interview logic, and utilities
from jd_parser import load_jd, extract_requirements
from interview_questions import generate_questions
from voice_interface import speak_text, transcribe_speech
from agent_logic import process_response  # Handles dynamic Q&A logic
from summary_logic import summarize_answer
from report_utils import save_report_to_pdf
from zoom_integration import schedule_zoom_meeting, join_zoom_meeting
from response_safety import is_empty, is_uncertain_response, is_too_short
from resume_parser import extract_resume_text
import time  # For tracking total interview duration


def main():
    start_time = time.time()  # Start timing the entire session

    # 🔗 Set up the Zoom call and connect
    meeting_link = schedule_zoom_meeting()
    join_zoom_meeting(meeting_link)

    # 🎤 Greet the candidate and warm them up
    print("\n👋 Starting interview with greeting...")
    greeting = "Hi there! I'm your AI interviewer for today. How are you feeling before we get started?"
    speak_text(greeting)

    greeting_response = transcribe_speech()
    print(f"🗣️ Candidate Greeting Response: {greeting_response}")
    speak_text("Great! Let's begin with your interview questions.")

    # 📄 Load and extract relevant info from the job description
    jd_text = load_jd("data/job_description.txt")
    parsed_info = extract_requirements(jd_text)
    print("\n📄 Extracted JD Info:")
    print(parsed_info)

    # 📑 Load and parse the candidate's resume
    resume_text = extract_resume_text("data/sample_resume.txt")
    print("\n📄 Resume Text Extracted.")

    # ❓ Generate customized interview questions using JD and resume data
    questions = generate_questions(parsed_info, resume_text=resume_text)
    print("\n💬 Interview Questions:")
    for idx, question in enumerate(questions, start=1):
        print(f"{idx}. {question}")

    # 🧾 Collect all Q&A results for scoring and reporting
    results = []

    print("\n🗣️ Voice Interview Starting...")
    for question in questions:
        # ⏳ Stop if interview exceeds 5 minutes
        if time.time() - start_time > 5 * 60:
            print("⏳ Interview time limit reached. Ending early.")
            speak_text("We're out of time for this interview. Thank you so much!")
            break

        print(f"\nBot: {question}")
        speak_text(question)

        response = transcribe_speech()
        print(f"Candidate: {response}")

        # 🚫 Handle non-responses or silence
        if is_empty(response):
            print("⚠️ No speech detected.")
            retry = input("🔁 Try again? (y/n): ").lower()
            if retry == "y":
                response = transcribe_speech()
                print(f"Candidate: {response}")
                if is_empty(response):
                    print("❌ Skipping question.")
                    continue
            else:
                print("❌ Skipping question.")
                continue

        # 🤔 Handle uncertain or vague responses
        if is_uncertain_response(response):
            print("⚠️ Candidate expressed uncertainty.")
            feedback = {
                "score": 2,
                "comment": "The candidate was unsure or did not provide an answer.",
                "follow_up": "Could you take a guess or share any related thoughts?"
            }
            summary = "Candidate was unsure how to answer this question."
            speak_text(feedback["follow_up"])
            response = transcribe_speech()

        # 📉 Handle overly short responses
        elif is_too_short(response):
            print("⚠️ Candidate response was very short.")
            feedback = {
                "score": 3,
                "comment": "The answer was too brief to evaluate fully.",
                "follow_up": "Could you elaborate a little more?"
            }
            summary = "Candidate gave a brief answer."
            speak_text(feedback["follow_up"])
            response = transcribe_speech()

        # 🔁 Dynamic Q&A loop with one follow-up allowed
        first_score = None
        first_comment = None
        full_answer = response
        follow_up_count = 0
        max_follow_ups = 1  # Limit to avoid long spirals

        while True:
            reply, is_follow_up, score = process_response(question, full_answer)

            if first_score is None:
                first_score = score
                first_comment = reply

            if is_follow_up:
                follow_up_count += 1
                if follow_up_count > max_follow_ups:
                    print("🚨 Max follow-ups reached. Moving on.")
                    speak_text("Thanks! Let's move to the next question.")
                    break

                print(f"Bot: {reply}")
                speak_text(reply)
                follow_up_response = transcribe_speech()
                full_answer += " " + follow_up_response
            else:
                print(f"Bot: {reply}")
                speak_text(reply)
                break

        # 📝 Summarize response for reporting
        summary = summarize_answer(question, full_answer)

        print(f"\n🧠 Score: {first_score}/10")
        print(f"💬 Comment: {first_comment}")
        print(f"📝 Summary: {summary}")

        # 🗃️ Store structured result
        results.append({
            "question": question,
            "answer": full_answer,
            "score": first_score,
            "comment": first_comment,
            "follow_up": "",
            "summary": summary
        })

    # 📊 Calculate average score across all questions
    avg_score = sum(r["score"] for r in results) / len(results)
    print(f"\n🏁 Overall Candidate Score: {avg_score:.2f}/10")

    # 📄 Generate and save interview report as a PDF
    candidate_name = input("\n🧾 Enter candidate's name: ").strip()
    save_report_to_pdf(results, candidate_name=candidate_name, avg_score=avg_score)

    end_time = time.time()
    total_duration = end_time - start_time
    print(f"\n⏱️ Total Interview Time: {total_duration:.2f} seconds")
    print("\n✅ Interview complete!")
    print("📄 PDF report saved as: interview_report.pdf")


# 👇 Run the interview bot if script is executed directly
if __name__ == "__main__":
    main()
