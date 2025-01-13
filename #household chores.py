import datetime
import csv
import os

# Define chores as a list
chores = [
    "Vacuum upstairs",
    "Vacuum main floor",
    "Vacuum basement",
    "Clean a toilet and sink in upstairs bathroom",
    "Clean a toilet and sink in main floor bathroom",
    "Clean a toilet and sink in basement bathroom",
    "Do one load of house laundry (bedding, towels, dishcloths, dog towels, dog blankets)",
    "Wipe down one appliance in the kitchen",
    "Wipe dust from surfaces - main floor (side tables, fireplace mantel, junk drawer cabinet)",
    "Wipe down kitchen table and chairs, including the legs",
    "Vacuum living room furniture",
    "Vacuum dining room bench seat",
    "Wipe down windowsills",
    "Wipe down the metal frame around the fireplace",
    "Scrub kitchen sinks and clean green drying rack",
    "Wipe down all mirrors in the house",
    "Wipe down the stairway banister and handrails"
]

# File to track the chores
CHORE_FILE = "chores_tracker.csv"

class ChoreTracker:
    def __init__(self, chores, file_path):
        self.chores = chores
        self.file_path = file_path
        self.last_completed = self.load_last_completed()

    def load_last_completed(self):
        """Load the last completed dates from the CSV file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, mode='r', newline='') as file:
                reader = csv.reader(file)
                last_completed = {}
                for row in reader:
                    if row:
                        chore, last_date = row
                        if last_date != "Not Done":
                            last_completed[chore] = datetime.datetime.strptime(last_date, "%Y-%m-%d").date()
                        else:
                            last_completed[chore] = None  # If not done, set as None
                return last_completed
        else:
            # If the file does not exist, initialize with empty last completed dates
            return {chore: None for chore in self.chores}

    def save_last_completed(self):
        """Save the last completed dates to the CSV file"""
        with open(self.file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            for chore, last_date in self.last_completed.items():
                writer.writerow([chore, last_date.strftime("%Y-%m-%d") if last_date else "Not Done"])

    def mark_chores_done(self, completed_chores):
        today = datetime.date.today()
        for chore in completed_chores:
            if chore in self.chores:
                self.last_completed[chore] = today
        self.save_last_completed()

    def show_completed_tasks(self):
        return self.last_completed

    def display_chores(self):
        """Display the list of chores and ask the user to select completed ones."""
        print("Please select the chores you've completed today:")
        for i, chore in enumerate(self.chores, 1):
            print(f"{i}. {chore}")
        print(f"\n[Press Enter to finish selecting]")

        selected_chores = []
        while True:
            try:
                choice = input("Enter the number of the chore you completed (or just press Enter to finish): ")
                if choice == '':
                    break
                selected_chores.append(self.chores[int(choice) - 1])
            except (ValueError, IndexError):
                print("Invalid selection. Please enter a valid number or press Enter to finish.")

        # Mark the selected chores as done
        self.mark_chores_done(selected_chores)
        print(f"\nTasks completed today: {', '.join(selected_chores)}")

# Create a ChoreTracker object
tracker = ChoreTracker(chores, CHORE_FILE)

# Example of showing and selecting chores for the day
tracker.display_chores()

# Print all completed tasks (for reference)
print("\nAll completed tasks:")
print(tracker.show_completed_tasks())


