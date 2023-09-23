import json
import logging

from flask import request, jsonify

from routes import app

logger = logging.getLogger(__name__)

@app.route('/calendar-scheduling', methods=['POST'])
def calendar_scheduling():
    data = request.get_json()

    results = schedule_lessons(data)

    return json.dumps(results)

def schedule_lessons(lessonList):
    lesson_requests = lessonList
    
    # Sort the lesson requests in descending order of potential earnings
    lesson_requests.sort(key=lambda x: x['potentialEarnings'], reverse=True)
    
    # Initialize the schedule dictionary
    schedule = {}
    
    # Initialize the total earnings
    total_earnings = 0

    # Map to track duration per day
    durationPerDay = {}
    
    # Iterate over the lesson requests
    for lesson_request in lesson_requests:
        lesson_id = lesson_request['lessonRequestId']
        duration = lesson_request['duration']
        earnings = lesson_request['potentialEarnings']
        available_days = lesson_request['availableDays']

        # If duration already exceed, exclude
        if duration > 12:
            continue

        # Find the first available day with enough hours for the lesson
        scheduled_day = None
        for day in available_days:
            if day not in schedule:
                schedule[day] = []
                durationPerDay[day] = 0
            if durationPerDay[day] + duration <= 12:
                scheduled_day = day
                break
        
        # Schedule the lesson if an available day is found
        if scheduled_day is not None:
            schedule[scheduled_day].append(lesson_id)
            durationPerDay[scheduled_day] += duration
            total_earnings += earnings
    
    # Return the schedule and total earnings as the response
    return schedule

# sample_data = [{
#     "lessonRequestId": "LR1",
#     "duration": 1,
#     "potentialEarnings": 100,
#     "availableDays": ["monday", "wednesday"]
# }, {
#     "lessonRequestId": "LR2",
#     "duration": 2,
#     "potentialEarnings": 50,
#     "availableDays": ["monday"]
# }, {
#     "lessonRequestId": "LR3",
#     "duration": 12,
#     "potentialEarnings": 1000,
#     "availableDays": ["wednesday"]
# }, {
#     "lessonRequestId": "LR4",
#     "duration": 13,
#     "potentialEarnings": 10000,
#     "availableDays": ["friday"]
# }]

# result = schedule_lessons(sample_data)
# print(result)