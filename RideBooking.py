from datetime import datetime


class RideBooking:

    def __init__(self):
        # Vehicle capacity limits
        self.CAPACITY = {"Bike": 1, "Sedan": 4, "SUV": 6, "Premium": 4}

        # Base fares per vehicle type
        self.BASE_FARES = {
            "Bike": 20.0,
            "Sedan": 50.0,
            "SUV": 80.0,
            "Premium": 100.0,
        }

        # Per-km rates
        self.PER_KM_RATES = {
            "Bike": 8.0,
            "Sedan": 12.0,
            "SUV": 18.0,
            "Premium": 25.0,
        }

    def process_booking(
        self,
        customer_id,
        pickup,
        drop,
        distance_km,
        passengers,
        vehicle_type,
        booking_time_str,
        driver_available,
        promo_discount_pct=0.0,
    ):

        # --- Validation Checks ---
        if distance_km <= 0:
            return {"status": "REJECTED", "reason": "Invalid distance"}

        if vehicle_type not in self.CAPACITY:
            return {"status": "REJECTED", "reason": "Invalid vehicle type"}

        if passengers <= 0 or passengers > self.CAPACITY[vehicle_type]:
            return {
                "status": "REJECTED",
                "reason": "Invalid passenger count for vehicle",
            }

        if not driver_available:
            return {"status": "REJECTED", "reason": "No drivers available"}

        try:
            booking_time = datetime.strptime(
                booking_time_str, "%Y-%m-%d %H:%M"
            )
        except ValueError:
            return {"status": "REJECTED", "reason": "Invalid booking time format"}

        # --- Fare Calculations ---
        base_fare = self.BASE_FARES[vehicle_type]
        distance_fare = distance_km * self.PER_KM_RATES[vehicle_type]

        # Peak Hour Surcharge (8:00–10:00 & 17:00–20:00) -> 25% surcharge
        hour = booking_time.hour
        is_peak = (8 <= hour < 10) or (17 <= hour < 20)
        peak_surcharge = (
            (base_fare + distance_fare) * 0.25 if is_peak else 0.0
        )

        # Night Surcharge (22:00–05:00) -> 20% surcharge
        is_night = (hour >= 22) or (hour < 5)
        night_surcharge = (
            (base_fare + distance_fare) * 0.20 if is_night else 0.0
        )

        # Passenger Surcharge ($5 per extra passenger above 1)
        passenger_surcharge = 5.0 * max(0, passengers - 1)

        subtotal = (
            base_fare
            + distance_fare
            + peak_surcharge
            + night_surcharge
            + passenger_surcharge
        )

        # Promotional Discount (Capped at maximum 30%)
        effective_discount_pct = min(max(0.0, promo_discount_pct), 30.0)
        promo_discount = subtotal * (effective_discount_pct / 100.0)

        final_fare = max(0.0, round(subtotal - promo_discount, 2))

        # Driver Allocation Strategy
        assigned_driver = f"DRIVER_{vehicle_type.upper()}_01"

        return {
            "status": "ACCEPTED",
            "customer_id": customer_id,
            "pickup": pickup,
            "drop": drop,
            "base_fare": base_fare,
            "distance_fare": distance_fare,
            "peak_surcharge": peak_surcharge,
            "night_surcharge": night_surcharge,
            "passenger_surcharge": passenger_surcharge,
            "promo_discount": promo_discount,
            "final_fare": final_fare,
            "assigned_driver": assigned_driver,
        }
