
interval_times = [193, 199, 200, 201, 202]
if all(198 <= x <= 202 for x in interval_times):
    print("Valid trigger")
    print(interval_times)
else:
    print("Invalid trigger")
    print(interval_times)