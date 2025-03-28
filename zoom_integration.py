import time
import webbrowser
from datetime import datetime, timedelta

def schedule_zoom_meeting():
    """
    Simulates scheduling a Zoom meeting.
    
    Returns:
        str: A mock Zoom meeting link.
    """
    # Set a mock start time for the meeting, 5 minutes from now
    start_time = datetime.now() + timedelta(minutes=5)

    # Fake meeting link (replace with your dummy link)
    meeting_link = "https://us05web.zoom.us/j/86105992714?pwd=Fdkp1a23seECSkKZjg3OOH7v8Yecdk.1"

    # Log scheduling progress
    print("📅 Scheduling Zoom interview...")
    time.sleep(1)
    print(f"✅ Zoom meeting scheduled for {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"🔗 Meeting Link: {meeting_link}")

    return meeting_link


def join_zoom_meeting(meeting_link):
    """
    Simulates joining a Zoom meeting by opening the link in the default web browser.

    Parameters:
        meeting_link (str): The Zoom meeting URL to open.
    """
    print("\n🧠 Agent preparing to join Zoom interview...")
    time.sleep(1)

    # Open the meeting link in the browser (simulating the join)
    print("🔗 Opening Zoom meeting link...")
    webbrowser.open(meeting_link)
    time.sleep(1)

    print("✅ Agent has joined the meeting (simulated)")
