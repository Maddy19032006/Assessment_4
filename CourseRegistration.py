class CourseRegistration:

    def __init__(self):
        # Master Course Catalog: {course_id: {credits, prerequisite, capacity, enrolled, schedule, allowed_semesters}}
        self.catalog = {
            "DBMS": {
                "credits": 4,
                "prerequisite": "Programming",
                "capacity": 30,
                "enrolled": 0,
                "schedule": [("Mon", 9, 11), ("Wed", 9, 11)],
                "allowed_semesters": [3, 4, 5, 6],
            },
            "AI": {
                "credits": 4,
                "prerequisite": "Data Structures",
                "capacity": 25,
                "enrolled": 0,
                "schedule": [("Tue", 10, 12), ("Thu", 10, 12)],
                "allowed_semesters": [5, 6, 7],
            },
            "ML": {
                "credits": 3,
                "prerequisite": "Statistics",
                "capacity": 20,
                "enrolled": 0,
                "schedule": [("Mon", 10, 12), ("Wed", 10, 12)],  # Clashes with DBMS on Mon/Wed 10-11
                "allowed_semesters": [5, 6, 7, 8],
            },
            "Cloud": {
                "credits": 3,
                "prerequisite": "Networking",
                "capacity": 2,
                "enrolled": 2,  # Already at full capacity
                "schedule": [("Fri", 14, 16)],
                "allowed_semesters": [6, 7, 8],
            },
            "Programming": {
                "credits": 3,
                "prerequisite": None,
                "capacity": 50,
                "enrolled": 10,
                "schedule": [("Mon", 14, 16)],
                "allowed_semesters": [1, 2, 3, 4],
            },
        }

        # Student Database: {student_id: {completed_courses, registered_courses, program, semester}}
        self.students = {}

    def register_student(
        self,
        student_id,
        program,
        semester,
        courses_selected,
        max_credit_limit,
        completed_courses,
    ):
        # 1. Prevent duplicate student registration session
        if student_id in self.students:
            return {"status": "REJECTED", "reason": "Duplicate registration"}

        occupied_slots = []
        registered_courses = []
        total_credits = 0

        for course in courses_selected:
            # 2. Check Invalid Course
            if course not in self.catalog:
                return {
                    "status": "REJECTED",
                    "reason": f"Invalid course: {course}",
                }

            course_info = self.catalog[course]

            # 3. Check Semester Restriction
            if semester not in course_info["allowed_semesters"]:
                return {
                    "status": "REJECTED",
                    "reason": f"Semester restriction violated for {course}",
                }

            # 4. Verify Prerequisites
            prereq = course_info["prerequisite"]
            if prereq and prereq not in completed_courses:
                return {
                    "status": "REJECTED",
                    "reason": f"Missing prerequisite: {prereq} for {course}",
                }

            # 5. Check Course Capacity
            if course_info["enrolled"] >= course_info["capacity"]:
                return {
                    "status": "REJECTED",
                    "reason": f"Course full: {course}",
                }

            # 6. Check Credit-Limit Violation & Boundary
            if total_credits + course_info["credits"] > max_credit_limit:
                return {
                    "status": "REJECTED",
                    "reason": "Credit-limit violation",
                }

            # 7. Detect Timetable Clashes
            for day, start, end in course_info["schedule"]:
                for o_day, o_start, o_end in occupied_slots:
                    if day == o_day:
                        # Time overlap check: start1 < end2 and start2 < end1
                        if start < o_end and o_start < end:
                            return {
                                "status": "REJECTED",
                                "reason": f"Timetable conflict for {course}",
                            }

            # Reserve schedule slots & accumulator updates
            for slot in course_info["schedule"]:
                occupied_slots.append(slot)

            registered_courses.append(course)
            total_credits += course_info["credits"]

        # Finalize Registration
        self.students[student_id] = {
            "program": program,
            "semester": semester,
            "registered_courses": registered_courses,
            "total_credits": total_credits,
        }

        # Update Course Enrollment Counts
        for course in registered_courses:
            self.catalog[course]["enrolled"] += 1

        return {
            "status": "ACCEPTED",
            "student_id": student_id,
            "registered_courses": registered_courses,
            "total_credits": total_credits,
        }
