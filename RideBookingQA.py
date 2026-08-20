from RideBooking import RideBooking


def run_qa_suite():
    system = RideBooking()
    passed = 0
    failed = 0

    print("====== STARTING AUTOMATED QA SUITE ======\n")

    # Test 1: Normal Booking
    res1 = system.process_booking(
        "C01", "A", "B", 10.0, 2, "Sedan", "2026-03-30 14:00", True, 0.0
    )
    if (
        res1["status"] == "ACCEPTED"
        and res1["final_fare"] == 175.0
        and res1["assigned_driver"] == "DRIVER_SEDAN_01"
    ):
        print("[PASS] Test 1: Normal Booking")
        passed += 1
    else:
        print("[FAIL] Test 1: Normal Booking")
        failed += 1

    # Test 2: Peak-Hour Booking (8:30 AM)
    res2 = system.process_booking(
        "C02", "A", "B", 10.0, 1, "Sedan", "2026-03-30 08:30", True, 0.0
    )
    if res2["status"] == "ACCEPTED" and res2["final_fare"] == 212.5:
        print("[PASS] Test 2: Peak-Hour Booking")
        passed += 1
    else:
        print("[FAIL] Test 2: Peak-Hour Booking")
        failed += 1

    # Test 3: Night Booking (23:00 PM)
    res3 = system.process_booking(
        "C03", "A", "B", 10.0, 1, "Sedan", "2026-03-30 23:00", True, 0.0
    )
    if res3["status"] == "ACCEPTED" and res3["final_fare"] == 204.0:
        print("[PASS] Test 3: Night Booking")
        passed += 1
    else:
        print("[FAIL] Test 3: Night Booking")
        failed += 1

    # Test 4: Invalid Distance (0 km)
    res4 = system.process_booking(
        "C04", "A", "B", 0.0, 1, "Sedan", "2026-03-30 14:00", True, 0.0
    )
    if res4["status"] == "REJECTED" and res4["reason"] == "Invalid distance":
        print("[PASS] Test 4: Invalid Distance")
        passed += 1
    else:
        print("[FAIL] Test 4: Invalid Distance")
        failed += 1

    # Test 5: Invalid Passenger Count (5 in Sedan, max 4)
    res5 = system.process_booking(
        "C05", "A", "B", 10.0, 5, "Sedan", "2026-03-30 14:00", True, 0.0
    )
    if (
        res5["status"] == "REJECTED"
        and res5["reason"] == "Invalid passenger count for vehicle"
    ):
        print("[PASS] Test 5: Invalid Passenger Count")
        passed += 1
    else:
        print("[FAIL] Test 5: Invalid Passenger Count")
        failed += 1

    # Test 6: Unavailable Driver
    res6 = system.process_booking(
        "C06", "A", "B", 10.0, 1, "Sedan", "2026-03-30 14:00", False, 0.0
    )
    if res6["status"] == "REJECTED" and res6["reason"] == "No drivers available":
        print("[PASS] Test 6: Unavailable Driver")
        passed += 1
    else:
        print("[FAIL] Test 6: Unavailable Driver")
        failed += 1

    # Test 7: Maximum Discount Cap (50% requested, 30% capped)
    res7 = system.process_booking(
        "C07", "A", "B", 10.0, 1, "Sedan", "2026-03-30 14:00", True, 50.0
    )
    if res7["status"] == "ACCEPTED" and res7["final_fare"] == 119.0:
        print("[PASS] Test 7: Maximum Discount Cap")
        passed += 1
    else:
        print("[FAIL] Test 7: Maximum Discount Cap")
        failed += 1

    # Test 8: Multiple Vehicle Types (Bike)
    res8 = system.process_booking(
        "C08", "A", "B", 5.0, 1, "Bike", "2026-03-30 14:00", True, 0.0
    )
    if (
        res8["status"] == "ACCEPTED"
        and res8["final_fare"] == 60.0
        and res8["assigned_driver"] == "DRIVER_BIKE_01"
    ):
        print("[PASS] Test 8: Multiple Vehicle Types (Bike)")
        passed += 1
    else:
        print("[FAIL] Test 8: Multiple Vehicle Types (Bike)")
        failed += 1

    # Test 9: Boundary Fare Values (Minimal positive distance: 0.1 km)
    res9 = system.process_booking(
        "C09", "A", "B", 0.1, 1, "Bike", "2026-03-30 14:00", True, 0.0
    )
    if res9["status"] == "ACCEPTED" and res9["final_fare"] == 20.8:
        print("[PASS] Test 9: Boundary Fare Values")
        passed += 1
    else:
        print("[FAIL] Test 9: Boundary Fare Values")
        failed += 1

    # Test 10: Driver Allocation Logic (SUV)
    res10 = system.process_booking(
        "C10", "A", "B", 10.0, 6, "SUV", "2026-03-30 14:00", True, 0.0
    )
    if (
        res10["status"] == "ACCEPTED"
        and res10["assigned_driver"] == "DRIVER_SUV_01"
    ):
        print("[PASS] Test 10: Driver Allocation Logic")
        passed += 1
    else:
        print("[FAIL] Test 10: Driver Allocation Logic")
        failed += 1

    print("\n====== QA TEST SUMMARY ======")
    print(f"Passed: {passed} / 10")
    print(f"Failed: {failed} / 10")


if __name__ == "__main__":
    run_qa_suite()
