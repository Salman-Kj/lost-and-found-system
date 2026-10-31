class Found_item:
    def __init__(self, item, color, location, finder, ph_num):
        self.item = item
        self.color = color
        self.location = location
        self.finder = finder
        self.number = ph_num


class Lost_item:
    def __init__(self, item, color, location, owner, ph_num):
        self.item = item
        self.color = color
        self.location = location
        self.owner = owner
        self.number = ph_num


found_items = []
lost_items = []

# Add Found Item First
print("\n--- Add Found Item ---")

item = input("Enter found item name: ").strip().lower()
color = input("Enter item color: ").strip().lower()
location = input("Where did you find the item? ").strip().lower()
finder = input("Enter finder name: ").strip()
number = input("Enter finder phone number: ").strip()

item1 = Found_item(item, color, location, finder, number)
found_items.append(item1)

print("\nFound item added successfully!")

# Add Lost Item
print("\n--- Report Lost Item ---")

item = input("Enter lost item name: ").strip().lower()
color = input("Enter item color: ").strip().lower()
location = input("Where did you lose the item? ").strip().lower()
owner = input("Enter owner name: ").strip()
number = input("Enter owner phone number: ").strip()

item2 = Lost_item(item, color, location, owner, number)
lost_items.append(item2)

print("\nLost item added successfully!")

# Compare Found and Lost Items
print("\n--- Matching Results ---")

match_found = False

for found_item in found_items:
    for lost_item in lost_items:

        if (found_item.item == lost_item.item and
                found_item.color == lost_item.color):

            match_found = True

            print("\nMatching Item Found!")
            print("Item:", found_item.item)
            print("Color:", found_item.color)
            print("Finder:", found_item.finder)
            print("Finder Phone:", found_item.number)
            print("Found Location:", found_item.location)
            print("Owner:", lost_item.owner)
            print("Owner Phone:", lost_item.number)
            print("Lost Location:", lost_item.location)

if not match_found:
    print("No matching item found.")
