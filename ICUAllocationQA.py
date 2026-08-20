from ICUAllocation import ICUAllocation


def run_qa_suite():
    passed = 0
    failed = 0

    print("====== STARTING AUTOMATED ICU ALLOCATION QA SUITE ======\n")

    # Test 1: Critical Patient Allocation
    system1 = ICUAllocation(total_beds=2)
    res1 = system1.process_patient(
        "P01",
        age=65,
        oxygen_level=82,
        heart_rate=140,
        bp_systolic=80,
        temperature=38.5,
        conditions_count=2,
    )
    if res1["status"] == "ALLOCATED" and res1["category"] == "CRITICAL":
        print("[PASS] Test 1: Critical Patient")
        passed += 1
    else:
        print("[FAIL] Test 1: Critical Patient")
        failed += 1

    # Test 2: Normal / Low Priority Patient
    system2 = ICUAllocation(total_beds=2)
    res2 = system2.process_patient(
        "P02",
        age=25,
        oxygen_level=98,
        heart_rate=72,
        bp_systolic=120,
        temperature=36.6,
        conditions_count=0,
    )
    if res2["status"] == "ALLOCATED" and res2["category"] == "LOW":
        print("[PASS] Test 2: Normal Patient")
        passed += 1
    else:
        print("[FAIL] Test 2: Normal Patient")
        failed += 1

    # Test 3: Emergency Case Allocation & Override
    system3 = ICUAllocation(total_beds=1)
    system3.process_patient(
        "P03_LOW",
        age=20,
        oxygen_level=99,
        heart_rate=70,
        bp_systolic=120,
        temperature=36.5,
    )
    res3 = system3.process_patient(
        "P03_EMG",
        age=40,
        oxygen_level=95,
        heart_rate=80,
        bp_systolic=120,
        temperature=37.0,
        is_emergency=True,
    )
    if (
        res3["status"] == "ALLOCATED_OVERRIDE"
        and res3["preempted_patient_id"] == "P03_LOW"
    ):
        print("[PASS] Test 3: Emergency Case Override")
        passed += 1
    else:
        print("[FAIL] Test 3: Emergency Case Override")
        failed += 1

    # Test 4: No ICU Beds Available (Waitlisted)
    system4 = ICUAllocation(total_beds=0)
    res4 = system4.process_patient(
        "P04",
        age=50,
        oxygen_level=95,
        heart_rate=80,
        bp_systolic=120,
        temperature=37.0,
    )
    if res4["status"] == "WAITLISTED" and res4["waitlist_position"] == 1:
        print("[PASS] Test 4: No ICU Beds (Waitlisted)")
        passed += 1
    else:
        print("[FAIL] Test 4: No ICU Beds (Waitlisted)")
        failed += 1

    # Test 5: Duplicate Patient Rejection
    system5 = ICUAllocation(total_beds=2)
    system5.process_patient(
        "P05",
        age=30,
        oxygen_level=98,
        heart_rate=75,
        bp_systolic=120,
        temperature=36.6,
    )
    res5 = system5.process_patient(
        "P05",
        age=30,
        oxygen_level=98,
        heart_rate=75,
        bp_systolic=120,
        temperature=36.6,
    )
    if res5["status"] == "REJECTED" and res5["reason"] == "Duplicate patient ID":
        print("[PASS] Test 5: Duplicate Patient ID")
        passed += 1
    else:
        print("[FAIL] Test 5: Duplicate Patient ID")
        failed += 1

    # Test 6: Invalid Oxygen Level (> 100%)
    system6 = ICUAllocation(total_beds=2)
    res6 = system6.process_patient(
        "P06",
        age=30,
        oxygen_level=105,
        heart_rate=75,
        bp_systolic=120,
        temperature=36.6,
    )
    if res6["status"] == "REJECTED" and res6["reason"] == "Invalid oxygen level":
        print("[PASS] Test 6: Invalid Oxygen Level")
        passed += 1
    else:
        print("[FAIL] Test 6: Invalid Oxygen Level")
        failed += 1

    # Test 7: Invalid Heart Rate (< 0 bpm)
    system7 = ICUAllocation(total_beds=2)
    res7 = system7.process_patient(
        "P07",
        age=30,
        oxygen_level=95,
        heart_rate=-10,
        bp_systolic=120,
        temperature=36.6,
    )
    if res7["status"] == "REJECTED" and res7["reason"] == "Invalid heart rate":
        print("[PASS] Test 7: Invalid Heart Rate")
        passed += 1
    else:
        print("[FAIL] Test 7: Invalid Heart Rate")
        failed += 1

    # Test 8: Priority Boundary Values (Category shift)
    system8 = ICUAllocation(total_beds=2)
    # Score below threshold (40 -> MEDIUM) vs score above threshold (45 -> HIGH)
    res8_a = system8.process_patient(
        "P08_A",
        age=30,
        oxygen_level=88,
        heart_rate=75,
        bp_systolic=120,
        temperature=36.6,
    )  # Oxygen <90 -> 30 pts = MEDIUM
    res8_b = system8.process_patient(
        "P08_B",
        age=65,
        oxygen_level=88,
        heart_rate=115,
        bp_systolic=120,
        temperature=36.6,
    )  # Oxygen <90 (30) + Age>=60 (5) + HR>110 (15) = 50 pts -> HIGH
    if res8_a["category"] == "MEDIUM" and res8_b["category"] == "HIGH":
        print("[PASS] Test 8: Priority Boundary Values")
        passed += 1
    else:
        print("[FAIL] Test 8: Priority Boundary Values")
        failed += 1

    # Test 9: Multiple Patients Competing for Bed (Higher score wins waitlist position 1)
    system9 = ICUAllocation(total_beds=0)
    system9.process_patient(
        "P09_MEDIUM",
        age=30,
        oxygen_level=91,
        heart_rate=75,
        bp_systolic=120,
        temperature=36.6,
    )  # Lower priority
    res9 = system9.process_patient(
        "P09_CRITICAL",
        age=70,
        oxygen_level=80,
        heart_rate=140,
        bp_systolic=80,
        temperature=39.0,
    )  # Higher priority
    if (
        res9["status"] == "WAITLISTED"
        and res9["category"] == "CRITICAL"
        and res9["waitlist_position"] == 1
    ):
        print("[PASS] Test 9: Multiple Patients Competing for Bed")
        passed += 1
    else:
        print("[FAIL] Test 9: Multiple Patients Competing for Bed")
        failed += 1

    print("\n====== QA TEST SUMMARY ======")
    print(f"Passed: {passed} / 9")
    print(f"Failed: {failed} / 9")


if __name__ == "__main__":
    run_qa_suite()
