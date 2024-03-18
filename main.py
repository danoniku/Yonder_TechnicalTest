import requests
import datetime
import pandas as pd


class LicenseAuthority:
    def __init__(self):
        self.api_url = "http://localhost:30000/drivers-licenses/list"

    def fetch_data(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from the API.")
            return []

    def list_suspended_licenses(self):
        data = self.fetch_data()
        suspended_licenses = [
            license for license in data if license.get("suspendat") == True]
        return suspended_licenses

    def extract_valid_licenses(self):
        data = self.fetch_data()
        today = datetime.datetime.today()
        valid_licenses = [license for license in data if (
            datetime.datetime.strptime(license.get(
                "dataDeExpirare"), "%d/%m/%Y") > today
            and today > datetime.datetime.strptime(license.get("dataDeEmitere"), "%d/%m/%Y")
            and license.get("suspendat") == False)]
        return valid_licenses

    def find_license_counts_by_category(self):
        data = self.fetch_data()
        license_counts = {}
        for license in data:
            category = license.get("categorie")
            if category in license_counts:
                license_counts[category] += 1
            else:
                license_counts[category] = 1
        return license_counts

    def export_to_excel(self, data, filename):
        if not data:
            print("No data to export.")
            return

        df = pd.DataFrame(data)
        df.to_excel(filename, index=False)
        print(f"Data exported to {filename}")

    def display_menu(self):
        while True:
            print("\nMenu:")
            print("1. Display Suspended Licenses and Export to Excel")
            print("2. Display Valid Licenses and Export to Excel")
            print("3. Display License Counts by Category and Export to Excel")
            print("4. Exit")
            choice = input("Enter your choice (1/2/3/4): ")

            if choice == "1":
                suspended_licenses = self.list_suspended_licenses()
                self.export_to_excel(
                    suspended_licenses, "suspended_licenses.xlsx")
                print("Suspended Licenses:", suspended_licenses)
            elif choice == "2":
                valid_licenses = self.extract_valid_licenses()
                self.export_to_excel(valid_licenses, "valid_licenses.xlsx")
                print("Valid Licenses:", valid_licenses)
            elif choice == "3":
                license_counts = self.find_license_counts_by_category()
                self.export_to_excel(
                    [{"Category": key, "Count": value}
                        for key, value in license_counts.items()],
                    "license_counts_by_category.xlsx"
                )
                print("License Counts by Category:", license_counts)
            elif choice == "4":
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter a valid option.")


# Example of usage:
authority = LicenseAuthority()
authority.display_menu()
