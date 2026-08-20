from CourseRegistration import CourseRegistration


def run_qa_suite():
    passed = 0
    failed = 0

    print("====== STARTING AUTOMATED COURSE REGISTRATION QA SUITE ======\n")

    # Test 1: Valid Registration
    system1 = CourseRegistration()
    res1 = system1.register_student(
        student_id="S01",
        program="CS",
        semester=4,
        courses_selected=["DBMS"],
        max_credit_limit=15,
        completed_courses=["Programming"],
    )
    if res1["status"] == "ACCEPTED" and res1["total_credits"] == 4:
        print("[PASS] Test 1: Valid Registration")
        passed += 1
    else:
        print("[FAIL] Test 1: Valid Registration")
        failed += 1

    # Test 2: Missing Prerequisite
    system2 = CourseRegistration()
    res2 = system2.register_student(
        student_id="S02",
        program="CS",
        semester=4,
        courses_selected=["DBMS"],
        max_credit_limit=15,
        completed_courses=[],  # Lacks 'Programming'
    )
    if res2["status"] == "REJECTED" and "Missing prerequisite" in res2["reason"]:
        print("[PASS] Test 2: Missing Prerequisite")
        passed += 1
    else:
        print("[FAIL] Test 2: Missing Prerequisite")
        failed += 1

    # Test 3: Credit-Limit Violation
    system3 = CourseRegistration()
    res3 = system3.register_student(
        student_id="S03",
        program="CS",
        semester=5,
        courses_selected=["DBMS", "AI"],  # Total 4 + 4 = 8 credits
        max_credit_limit=6,  # Limit is 6
        completed_courses=["Programming", "Data Structures"],
    )
    if res3["status"] == "REJECTED" and res3["reason"] == "Credit-limit violation":
        print("[PASS] Test 3: Credit-Limit Violation")
        passed += 1
    else:
        print("[FAIL] Test 3: Credit-Limit Violation")
        failed += 1

    # Test 4: Timetable Conflict
    system4 = CourseRegistration()
    res4 = system4.register_student(
        student_id="S04",
        program="CS",
        semester=5,
        courses_selected=["DBMS", "ML"],  # Overlap on Mon/Wed 10:00-11:00
        max_credit_limit=15,
        completed_courses=["Programming", "Statistics"],
    )
    if res4["status"] == "REJECTED" and "Timetable conflict" in res4["reason"]:
        print("[PASS] Test 4: Timetable Conflict")
        passed += 1
    else:
        print("[FAIL] Test 4: Timetable Conflict")
        failed += 1

    # Test 5: Full Course
    system5 = CourseRegistration()
    res5 = system5.register_student(
        student_id="S05",
        program="CS",
        semester=6,
        courses_selected=["Cloud"],  # Pre-enrolled 2/2
        max_credit_limit=15,
        completed_courses=["Networking"],
    )
    if res5["status"] == "REJECTED" and "Course full" in res5["reason"]:
        print("[PASS] Test 5: Full Course")
        passed += 1
    else:
        print("[FAIL] Test 5: Full Course")
        failed += 1

    # Test 6: Duplicate Registration
    system6 = CourseRegistration()
    system6.register_student(
        student_id="S06",
        program="CS",
        semester=4,
        courses_selected=["DBMS"],
        max_credit_limit=15,
        completed_courses=["Programming"],
    )
    res6 = system6.register_student(
        student_id="S06",
        program="CS",
        semester=4,
        courses_selected=["DBMS"],
        max_credit_limit=15,
        completed_courses=["Programming"],
    )
    if res6["status"] == "REJECTED" and res6["reason"] == "Duplicate registration":
        print("[PASS] Test 6: Duplicate Registration")
        passed += 1
    else:
        print("[FAIL] Test 6: Duplicate Registration")
        failed += 1

    # Test 7: Invalid Course
    system7 = CourseRegistration()
    res7 = system7.register_student(
        student_id="S07",
        program="CS",
        semester=4,
        courses_selected=["QuantumComputing"],
        max_credit_limit=15,
        completed_courses=[],
    )
    if res7["status"] == "REJECTED" and "Invalid course" in res7["reason"]:
        print("[PASS] Test 7: Invalid Course")
        passed += 1
    else:
        print("[FAIL] Test 7: Invalid Course")
        failed += 1

    # Test 8: Semester Restriction
    system8 = CourseRegistration()
    res8 = system8.register_student(
        student_id="S08",
        program="CS",
        semester=1,  # AI is restricted to Semesters 5-7
        courses_selected=["AI"],
        max_credit_limit=15,
        completed_courses=["Data Structures"],
    )
    if res8["status"] == "REJECTED" and "Semester restriction" in res8["reason"]:
        print("[PASS] Test 8: Semester Restriction")
        passed += 1
    else:
        print("[FAIL] Test 8: Semester Restriction")
        failed += 1

    # Test 9: Boundary Credit Values (Exact max limit match)
    system9 = CourseRegistration()
    res9 = system9.register_student(
        student_id="S09",
        program="CS",
        semester=4,
        courses_selected=["DBMS"],  # 4 credits
        max_credit_limit=4,  # Exact boundary limit
        completed_courses=["Programming"],
    )
    if res9["status"] == "ACCEPTED" and res9["total_credits"] == 4:
        print("[PASS] Test 9: Boundary Credit Values")
        passed += 1
    else:
        print("[FAIL] Test 9: Boundary Credit Values")
        failed += 1

    print("\n====== QA TEST SUMMARY ======")
    print(f"Passed: {passed} / 9")
    print(f"Failed: {failed} / 9")


if __name__ == "__main__":
    run_qa_suite()
