class ICUAllocation:

    def __init__(self, total_beds=0):
        self.total_beds = max(0, total_beds)
        self.available_beds = self.total_beds
        self.registered_patient_ids = set()
        self.allocated_beds = {}  # {patient_id: details}
        self.waiting_list = []  # List of patient dicts sorted by priority

    def _calculate_priority_score(
        self,
        age,
        oxygen_level,
        heart_rate,
        bp_systolic,
        temperature,
        conditions_count,
        is_emergency,
    ):
        """Calculates a composite severity score (higher score = higher priority)."""
        score = 0.0

        # Oxygen saturation weight (Critical < 90, High 90-93)
        if oxygen_level < 85:
            score += 40
        elif oxygen_level < 90:
            score += 30
        elif oxygen_level <= 93:
            score += 15

        # Heart rate weight (Normal ~60-100 bpm)
        if heart_rate < 40 or heart_rate > 130:
            score += 25
        elif heart_rate < 50 or heart_rate > 110:
            score += 15

        # Systolic Blood pressure weight (Normal ~120 mmHg)
        if bp_systolic < 90 or bp_systolic > 180:
            score += 20
        elif bp_systolic < 100 or bp_systolic > 160:
            score += 10

        # Age risk factor
        if age >= 75:
            score += 10
        elif age >= 60:
            score += 5

        # Temperature extremes (°C)
        if temperature >= 39.5 or temperature <= 35.0:
            score += 10

        # Existing medical conditions ($5$ pts each, capped at $20$)
        score += min(20, conditions_count * 5)

        # Emergency override score boost
        if is_emergency:
            score += 50

        return score

    def _determine_category(self, score, is_emergency):
        """Classifies severity priority based on total score."""
        if is_emergency or score >= 70:
            return "CRITICAL"
        elif score >= 45:
            return "HIGH"
        elif score >= 25:
            return "MEDIUM"
        else:
            return "LOW"

    def process_patient(
        self,
        patient_id,
        age,
        oxygen_level,
        heart_rate,
        bp_systolic,
        temperature,
        conditions_count=0,
        is_emergency=False,
    ):

        # --- Validation Checks ---
        if patient_id in self.registered_patient_ids:
            return {"status": "REJECTED", "reason": "Duplicate patient ID"}

        if not (0 <= oxygen_level <= 100):
            return {"status": "REJECTED", "reason": "Invalid oxygen level"}

        if not (0 <= heart_rate <= 300):
            return {"status": "REJECTED", "reason": "Invalid heart rate"}

        if age < 0 or bp_systolic <= 0 or temperature <= 0:
            return {"status": "REJECTED", "reason": "Invalid vital parameters"}

        # Calculate score & category
        score = self._calculate_priority_score(
            age,
            oxygen_level,
            heart_rate,
            bp_systolic,
            temperature,
            conditions_count,
            is_emergency,
        )
        category = self._determine_category(score, is_emergency)

        self.registered_patient_ids.add(patient_id)

        patient_record = {
            "patient_id": patient_id,
            "priority_score": score,
            "category": category,
            "is_emergency": is_emergency,
        }

        # --- Allocation & Emergency Override Logic ---
        if self.available_beds > 0:
            self.available_beds -= 1
            self.allocated_beds[patient_id] = patient_record
            return {
                "status": "ALLOCATED",
                "patient_id": patient_id,
                "category": category,
                "priority_score": score,
                "beds_left": self.available_beds,
            }

        # Emergency Override Rule: Bumps lowest priority allocated non-critical patient if no beds available
        if is_emergency or category == "CRITICAL":
            preemptable = [
                p
                for p in self.allocated_beds.values()
                if p["category"] not in ["CRITICAL"] and not p["is_emergency"]
            ]
            if preemptable:
                # Find the record with lowest priority score
                lowest_p = min(preemptable, key=lambda x: x["priority_score"])
                # Demote lowest priority patient back to waiting list
                del self.allocated_beds[lowest_p["patient_id"]]
                self.waiting_list.append(lowest_p)

                # Allocate bed to new Critical/Emergency patient
                self.allocated_beds[patient_id] = patient_record
                return {
                    "status": "ALLOCATED_OVERRIDE",
                    "patient_id": patient_id,
                    "category": category,
                    "priority_score": score,
                    "preempted_patient_id": lowest_p["patient_id"],
                }

        # No beds available -> Add to waiting list
        self.waiting_list.append(patient_record)
        self.waiting_list.sort(key=lambda x: x["priority_score"], reverse=True)

        return {
            "status": "WAITLISTED",
            "patient_id": patient_id,
            "category": category,
            "priority_score": score,
            "waitlist_position": [
                p["patient_id"] for p in self.waiting_list
            ].index(patient_id)
            + 1,
        }
