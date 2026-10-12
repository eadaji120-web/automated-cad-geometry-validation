import csv
from pathlib import Path


INPUT_FILE = Path("sample_parts.csv")


def validate_part(part):
    """Check a part's dimensions and calculate its volume."""
    name = part.get("part_name", "").strip() or "Unnamed part"

    try:
        length = float(part["length_mm"])
        width = float(part["width_mm"])
        height = float(part["height_mm"])
    except (ValueError, TypeError, KeyError):
        return name, False, "Missing or non-numeric dimensions", None

    if length <= 0 or width <= 0 or height <= 0:
        return name, False, "Dimensions must all be greater than zero", None

    volume = length * width * height
    return name, True, "Dimensions are valid", volume


def main():
    if not INPUT_FILE.exists():
        print(f"Cannot find {INPUT_FILE}.")
        print("Place sample_parts.csv in the same folder as main.py.")
        return

    with INPUT_FILE.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required = {"part_name", "length_mm", "width_mm", "height_mm"}
        if not reader.fieldnames or not required.issubset(reader.fieldnames):
            print("CSV headers are incorrect.")
            print("Required: part_name,length_mm,width_mm,height_mm")
            return

        print("\nCAD GEOMETRY VALIDATION REPORT")
        print("=" * 55)

        total = 0
        passed = 0

        for part in reader:
            total += 1
            name, valid, message, volume = validate_part(part)

            if valid:
                passed += 1
                print(f"[PASS] {name}: {volume:.2f} mm^3")
            else:
                print(f"[FAIL] {name}: {message}")

        print("=" * 55)
        print(f"Total parts checked: {total}")
        print(f"Valid parts: {passed}")
        print(f"Invalid parts: {total - passed}")


if __name__ == "__main__":
    main()
