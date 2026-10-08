import json

resources = [
    {"id": "R001", "name": "Laptop", "category": "Electronics",
     "total": 10, "available": 10},
    {"id": "R002", "name": "Keyboard", "category": "Accessories",
     "total": 5, "available": 5},
    {"id": "R003", "name": "Headset", "category": "Accessories",
     "total": 3, "available": 3}
]

fellows = {
    "F001": "Ada",
    "F002": "John",
    "F003": "Grace"
}

borrow_records = []


# 1. Find a resource
def find_resource(resource_id):
    for resource in resources:
        if resource["id"] == resource_id.upper():
            return resource
    return None


# 2. Add a resource
def add_resource():
    resource_id = input("Enter resource ID: ").strip().upper()

    if find_resource(resource_id):
        print("Error: Resource ID already exists.")
        return

    name = input("Enter resource name: ").strip()
    category = input("Enter category: ").strip()

    try:
        total = int(input("Enter total units: "))

        if total <= 0 or not name or not category:
            print("Invalid input.")
            return

    except ValueError:
        print("Enter a valid whole number.")
        return

    resources.append({
        "id": resource_id,
        "name": name,
        "category": category,
        "total": total,
        "available": total
    })

    print("Resource added successfully.")


# 3. List resources
def list_resources():
    print("\n--- RESOURCE INVENTORY ---")

    for r in resources:
        print(
            f'ID: {r["id"]}, '
            f'Name: {r["name"]}, '
            f'Category: {r["category"]}, '
            f'Total: {r["total"]}, '
            f'Available: {r["available"]}'
        )


# 4. Borrow resources
def borrow_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource = find_resource(resource_id.strip())

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    if resource is None:
        print("Error: Resource ID not found.")
        return

    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return

    if quantity > resource["available"]:
        print("Error: Not enough resources available.")
        return

    # Update inventory after validation
    resource["available"] -= quantity

    # Update borrowing record
    for record in borrow_records:
        if (record["fellow_id"] == fellow_id
                and record["resource_id"] == resource["id"]):
            record["quantity"] += quantity
            break
    else:
        borrow_records.append({
            "fellow_id": fellow_id,
            "resource_id": resource["id"],
            "quantity": quantity
        })

    print(f'{fellows[fellow_id]} borrowed {quantity} {resource["name"]}(s).')


# 5. Return resources
def return_resource(fellow_id, resource_id, quantity):
    fellow_id = fellow_id.strip().upper()
    resource = find_resource(resource_id.strip())

    if fellow_id not in fellows:
        print("Error: Fellow ID not found.")
        return

    if resource is None:
        print("Error: Resource ID not found.")
        return

    if not isinstance(quantity, int) or quantity <= 0:
        print("Error: Quantity must be a positive integer.")
        return

    record = next(
        (r for r in borrow_records
         if r["fellow_id"] == fellow_id
         and r["resource_id"] == resource["id"]),
        None
    )

    if record is None or quantity > record["quantity"]:
        print("Error: Invalid return quantity.")
        return

    # Update the loan and inventory
    record["quantity"] -= quantity
    resource["available"] += quantity

    if record["quantity"] == 0:
        borrow_records.remove(record)

    print(f'{fellows[fellow_id]} returned {quantity} {resource["name"]}(s).')


# 6. Search resources by name
def search_resource():
    name = input("Enter resource name: ").strip().casefold()

    found = False

    for r in resources:
        if name in r["name"].casefold():
            print(r)
            found = True

    if not found:
        print("Resource not found.")


# 7. Filter resources by category
def filter_category():
    category = input("Enter category: ").strip().casefold()

    found = False

    for r in resources:
        if r["category"].casefold() == category:
            print(r)
            found = True

    if not found:
        print("No resources found in this category.")


# 8. Generate inventory report
def generate_report():
    total_units = sum(r["total"] for r in resources)
    available_units = sum(r["available"] for r in resources)
    borrowed_units = total_units - available_units

    print("\n--- INVENTORY REPORT ---")
    print("Total units:", total_units)
    print("Available units:", available_units)
    print("Units currently borrowed:", borrowed_units)

    print("\nLow-stock resources (fewer than 3 available):")

    low_stock = [r for r in resources if r["available"] < 3]

    if low_stock:
        for r in low_stock:
            print(r["name"], "-", r["available"], "available")
    else:
        print("None")

    borrowed = {
        r["id"]: r["total"] - r["available"]
        for r in resources
    }

    highest = max(borrowed.values(), default=0)

    if highest == 0:
        print("\nNo resources are currently borrowed.")
    else:
        print("\nMost borrowed resource(s):")

        for r in resources:
            if borrowed[r["id"]] == highest:
                print(r["name"], "-", highest, "units")


# 9. Save data using JSON
def save_data():
    data = {
        "resources": resources,
        "fellows": fellows,
        "borrow_records": borrow_records
    }

    with open("learn2earn_data.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    print("Data saved successfully.")


# 10. Load saved data
def load_data():
    global resources, fellows, borrow_records

    try:
        with open("learn2earn_data.json", "r", encoding="utf-8") as file:
            data = json.load(file)

        resources = data["resources"]
        fellows = data["fellows"]
        borrow_records = data["borrow_records"]

        print("Data loaded successfully.")

    except FileNotFoundError:
        print("No saved data found.")

    except (json.JSONDecodeError, KeyError, TypeError):
        print("Saved data is invalid.")


# 11. Demonstrate all required transactions
def demonstration():
    print("\n--- REQUIRED DEMONSTRATION ---")

    borrow_resource("F001", "R001", 2)
    print("Laptop available:", find_resource("R001")["available"])

    borrow_resource("F002", "R002", 3)
    print("Keyboard available:", find_resource("R002")["available"])

    return_resource("F001", "R001", 1)
    print("Laptop available:", find_resource("R001")["available"])

    borrow_resource("F003", "R003", 4)
    print("Headset available:", find_resource("R003")["available"])

    return_resource("F002", "R002", 4)
    print("Keyboard available:", find_resource("R002")["available"])

    print("\nSearch for LAPtop:")

    for r in resources:
        if "laptop" in r["name"].casefold():
            print(r["name"])

    generate_report()


# 12. Main menu
def main():
    while True:
        print("""
===== LEARN2EARN RESOURCE SYSTEM =====

1. Add resource
2. List resources
3. Borrow resource
4. Return resource
5. Search resource
6. Filter by category
7. Generate report
8. Save data
9. Load data
10. Run demonstration
0. Exit
""")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_resource()

        elif choice == "2":
            list_resources()

        elif choice == "3":
            fellow_id = input("Enter fellow ID: ")
            resource_id = input("Enter resource ID: ")

            try:
                quantity = int(input("Enter quantity: "))
                borrow_resource(fellow_id, resource_id, quantity)
            except ValueError:
                print("Enter a valid whole number.")

        elif choice == "4":
            fellow_id = input("Enter fellow ID: ")
            resource_id = input("Enter resource ID: ")

            try:
                quantity = int(input("Enter quantity: "))
                return_resource(fellow_id, resource_id, quantity)
            except ValueError:
                print("Enter a valid whole number.")

        elif choice == "5":
            search_resource()

        elif choice == "6":
            filter_category()

        elif choice == "7":
            generate_report()

        elif choice == "8":
            save_data()

        elif choice == "9":
            load_data()

        elif choice == "10":
            demonstration()

        elif choice == "0":
            print("Thank you for using Learn2Earn.")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()