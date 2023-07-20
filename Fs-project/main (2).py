import pickle
from tkinter import *
from tkinter import messagebox
from tkinter import Listbox, Scrollbar
import hashlib
from PIL import Image, ImageTk
import os
import hashlib
import json

class Record:
    def __init__(self, key, data):
        self.key = key
        self.data = data


class FileHashTable:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.isfile(self.filename):
            with open(self.filename, "w") as file:
                file.write("[]")

    def _hash_function(self, key):
        hashed_key = hashlib.sha256(key.encode()).hexdigest()
        return hashed_key

    def add_record(self, record):
        key = record.key
        hashed_key = self._hash_function(key)
        data = {hashed_key: record.data}

        with open(self.filename, "r+") as file:
            records = json.load(file)
            records.append(data)
            file.seek(0)
            json.dump(records, file)
            file.truncate()


    def remove_record(self, key):
        hashed_key = self._hash_function(key)

        with open(self.filename, "r+") as file:
            records = json.load(file)
            updated_data = [data for data in records if hashed_key not in data]
            file.seek(0)
            json.dump(updated_data, file)
            file.truncate()

    def search_record_by_license_plate(self, license_plate):
        hashed_key = self._hash_function(license_plate)

        with open(self.filename, "r") as file:
            records = json.load(file)
            for data in records:
                if hashed_key in data:
                    return data[hashed_key]
        return None

    def search_record_by_renter_name(self, renter_name):
        hashed_renter_name = self._hash_function(renter_name)

        with open(self.filename, "r") as file:
            records = json.load(file)
            for data in records:
                if any(hashed_renter_name == self._hash_function(key) for key in data.keys()):
                    return data[self._hash_function(renter_name)]

        return None

    def search_record_by_vehicle_model(self, vehicle_model):
        results = []

        with open(self.filename, "r") as file:
            records = json.load(file)
            for data in records:
                for key, value in data.items():
                    if vehicle_model == value["Vehicle Model"]:
                        results.append(value)

        return results


class VehicleRentalSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Vehicle Rental System")
        self.root.geometry("800x600")

        # File-based hash table for efficient data retrieval
        self.rental_records = FileHashTable(filename="rental_records.txt")

        # Image
        
        # Load the image using PIL
        image = Image.open("background.png")
        image = image.resize((800, 600), Image.ANTIALIAS)
        self.background_image = ImageTk.PhotoImage(image)

        # Create a label widget to display the image as the background
        self.background_label = Label(self.root, image=self.background_image)
        self.background_label.place(x=0, y=0, relwidth=1, relheight=1)
        

        # Total number of available vehicles for rental
        self.total_vehicles = 50
        self.available_vehicles = self.total_vehicles
        self.rented_vehicles = []



        # Vehicle details
        self.license_plate = StringVar()
        self.renter_name = StringVar()
        self.vehicle_model = StringVar()

        self.available_vehicle_names = [
        "Honda Civic",
        "Toyota Camry",
        "Ford Mustang",
        "Chevrolet Silverado",
        "Tesla Model S",
        # Add more vehicle names as desired
        ]


        # Sorting criteria
        self.sort_criteria = StringVar(value="Index")

        # Tkinter
        title = Label(self.root, text="RentEase", bg="#609ebc", font=("Helvetica", 24, "bold"))
        title.pack(side=TOP, pady=10)

        lbl_license_plate = Label(self.root, text="License Plate:", bg="#609ebc", font=("Calibri", 16, "bold"))
        lbl_license_plate.place(x=30, y=50)
        entry_license_plate = Entry(self.root, textvariable=self.license_plate)
        entry_license_plate.place(x=150, y=50)

        lbl_renter_name = Label(self.root, text="Renter Name:", bg="#609ebc", font=("Calibri", 16, "bold"))
        lbl_renter_name.place(x=30, y=90)
        entry_renter_name = Entry(self.root, textvariable=self.renter_name)
        entry_renter_name.place(x=150, y=90, width=150)

        lbl_vehicle_model = Label(self.root, text="Vehicle Model:", bg="#609ebc", font=("Calibri", 16, "bold"))
        lbl_vehicle_model.place(x=30, y=130)
        entry_vehicle_model = Entry(self.root, textvariable=self.vehicle_model)
        entry_vehicle_model.place(x=150, y=130)

        # Sorting options
        lbl_sort_criteria = Label(self.root, text="Sort by:", bg="#609ebc", font=("Calibri", 12, "bold"))
        lbl_sort_criteria.place(x=30, y=170)
        sort_dropdown = OptionMenu(self.root, self.sort_criteria, "Index", "License Plate", "Renter Name")
        sort_dropdown.configure(background="#609ebc")
        sort_dropdown.place(x=150, y=166)

        # Buttons
        btn_rent = Button(self.root, text="Rent Vehicle", command=self.rent_vehicle)
        btn_rent.configure(highlightbackground="#609ebc", highlightthickness=2)
        btn_rent.place(x=30, y=210, width=100)

        btn_return = Button(self.root, text="Return Vehicle", command=self.return_vehicle)
        btn_return.configure(highlightbackground="#609ebc", highlightthickness=2)
        btn_return.place(x=150, y=210, width=100)

        btn_view_rented = Button(self.root, text="View Rented Vehicles", command=self.view_rented_vehicles)
        btn_view_rented.configure(highlightbackground="#609ebc", highlightthickness=2)
        btn_view_rented.place(x=270, y=210, width=160)

        lbl_available_vehicles = Label(self.root, text="Available Vehicles:", bg="#609ebc", font=("Calibri", 12, "bold"))
        lbl_available_vehicles.place(x=30, y=250)
        self.lbl_available_vehicles_value = Label(self.root, text=self.available_vehicles)
        self.lbl_available_vehicles_value.place(x=150, y=250)

        lbl_total_rented = Label(self.root, text="Total Rented Vehicles:", bg="#609ebc", font=("Calibri", 12, "bold"))
        lbl_total_rented.place(x=30, y=280)
        self.lbl_total_rented_value = Label(self.root, text=len(self.rented_vehicles))
        self.lbl_total_rented_value.place(x=170, y=280)

        btn_view_available = Button(self.root, text="View Available Vehicles", command=self.view_available_vehicles)
        btn_view_available.configure(highlightbackground="#609ebc", highlightthickness=2)
        btn_view_available.place(x=270, y=250, width=160)

    def view_available_vehicles(self):
        if self.available_vehicle_names:
            available_vehicles_window = Toplevel(self.root)
            available_vehicles_window.title("Available Vehicles")
            available_vehicles_window.geometry("400x300")

            lbl_available_vehicles = Label(available_vehicles_window, text="Available Vehicles", bg="#609ebc", font=("Helvetica", 14, "bold"))
            lbl_available_vehicles.pack(pady=10)

            available_vehicles_listbox = Listbox(available_vehicles_window)
            available_vehicles_listbox.pack(fill=BOTH, expand=True)

            scrollbar = Scrollbar(available_vehicles_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            available_vehicles_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=available_vehicles_listbox.yview)

            for vehicle in self.available_vehicle_names:
                available_vehicles_listbox.insert(END, vehicle)
        else:
            messagebox.showinfo("No Vehicles Available", "There are no vehicles available for rental.")


    def rent_vehicle(self):
        license_plate = self.license_plate.get()
        renter_name = self.renter_name.get()
        vehicle_model = self.vehicle_model.get()

        if license_plate and renter_name and vehicle_model:
            hashed_renter_name = hashlib.sha256(renter_name.encode()).hexdigest()

            vehicle = {
                "Index": len(self.rented_vehicles) + 1,
                "License Plate": license_plate,
                "Renter Name": hashed_renter_name,
                "Vehicle Model": vehicle_model
            }
            self.rented_vehicles.append(vehicle)
            self.available_vehicles -= 1
            self.lbl_available_vehicles_value.config(text=self.available_vehicles)
            self.lbl_total_rented_value.config(text=len(self.rented_vehicles))
            self.save_rented_vehicles()
            messagebox.showinfo("Success", "Vehicle rented successfully.")
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Please fill in all the fields.")


    def return_vehicle(self):
        if self.rented_vehicles:
            rented_vehicles_window = Toplevel(self.root)
            rented_vehicles_window.title("Select a Vehicle to Return")
            rented_vehicles_window.geometry("300x250")

            lbl_select_vehicle = Label(rented_vehicles_window, text="Select a vehicle to return:")
            lbl_select_vehicle.pack(pady=10)

            rented_vehicles_listbox = Listbox(rented_vehicles_window, selectmode=SINGLE)
            rented_vehicles_listbox.pack(fill=BOTH, expand=True)

            scrollbar = Scrollbar(rented_vehicles_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            rented_vehicles_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=rented_vehicles_listbox.yview)

            for vehicle in self.rented_vehicles:
                vehicle_info = f"Index: {vehicle['Index']} | License Plate: {vehicle['License Plate']} | Renter Name: {vehicle['Renter Name']}"
                rented_vehicles_listbox.insert(END, vehicle_info)

            btn_return_selected = Button(rented_vehicles_window, text="Return Selected Vehicle",
                                        command=lambda: self.return_selected_vehicle(rented_vehicles_listbox))
            btn_return_selected.pack(pady=10)
        else:
            messagebox.showinfo("No Vehicles Rented", "There are no vehicles rented.")

    def return_selected_vehicle(self, rented_vehicles_listbox):
        selected_index = rented_vehicles_listbox.curselection()
        if selected_index:
            selected_vehicle = self.rented_vehicles[selected_index[0]]
            license_plate = selected_vehicle['License Plate']

            # Remove the record from rental_records
            self.rental_records.remove_record(license_plate)

            # Update the available vehicles count
            self.available_vehicles += 1
            self.lbl_available_vehicles_value.config(text=self.available_vehicles)

            # Update the total rented vehicles count
            self.lbl_total_rented_value.config(text=len(self.rented_vehicles))

            # Save the updated rented vehicles
            self.save_rented_vehicles()

            # Remove the selected vehicle from the listbox
            rented_vehicles_listbox.delete(selected_index)

            messagebox.showinfo("Success", "Vehicle returned successfully.")
        else:
            messagebox.showerror("Error", "Please select a vehicle to return.")

    def update_record(self, rented_vehicles_listbox):
        selected_index = rented_vehicles_listbox.curselection()
        if selected_index:
            selected_vehicle = self.rented_vehicles[selected_index[0]]
            license_plate = selected_vehicle['License Plate']

            # Get the existing details from the selected vehicle
            existing_renter_name = selected_vehicle['Renter Name']
            existing_vehicle_model = selected_vehicle['Vehicle Model']

            # Prepopulate the entry fields with the existing values
            self.renter_name.set(existing_renter_name)
            self.vehicle_model.set(existing_vehicle_model)
            self.license_plate.set(license_plate)

            # Create a dialog box to allow the user to edit the record
            dialog = Toplevel()
            dialog.title("Edit Record")

            # Create labels and entry fields for the updated details
            renter_name_label = Label(dialog, text="Renter Name:")
            renter_name_entry = Entry(dialog, textvariable=self.renter_name)

            vehicle_model_label = Label(dialog, text="Vehicle Model:")
            vehicle_model_entry = Entry(dialog, textvariable=self.vehicle_model)

            license_plate_label = Label(dialog, text="License Plate:")
            license_plate_entry = Entry(dialog, textvariable=self.license_plate)

            # Position the labels and entry fields in the dialog box
            renter_name_label.grid(row=0, column=0, padx=10, pady=5)
            renter_name_entry.grid(row=0, column=1, padx=10, pady=5)

            vehicle_model_label.grid(row=1, column=0, padx=10, pady=5)
            vehicle_model_entry.grid(row=1, column=1, padx=10, pady=5)

            license_plate_label.grid(row=2, column=0, padx=10, pady=5)
            license_plate_entry.grid(row=2, column=1, padx=10, pady=5)

            def update_record():
                # Get the updated details from the user
                renter_name = self.renter_name.get()
                vehicle_model = self.vehicle_model.get()
                license_plate = self.license_plate.get()
                hashed_renter_name = hashlib.sha256(renter_name.encode()).hexdigest()

                # Update the record
                selected_vehicle['Renter Name'] = hashed_renter_name
                selected_vehicle['Vehicle Model'] = vehicle_model
                selected_vehicle['License Plate'] = license_plate

                messagebox.showinfo("Success", "Vehicle details updated.")
                self.clear_fields()
                dialog.destroy()
    
            # Create a button to update the record
            update_button = Button(dialog, text="Update", command=update_record)
            update_button.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

            dialog.mainloop()
        else:
            messagebox.showerror("Error", "Please select a vehicle to update.")






  
    def save_rented_vehicles(self):
        with open("rented_vehicles.json", "w") as file:
            json.dump(self.rented_vehicles, file)

    def view_rented_vehicles(self):
        if self.rented_vehicles:
            rented_vehicles_window = Toplevel(self.root)
            rented_vehicles_window.title("Rented Vehicles")
            rented_vehicles_window.geometry("400x300")

            lbl_rented_vehicles = Label(rented_vehicles_window, text="Rented Vehicles", font=("Helvetica", 14, "bold"))
            lbl_rented_vehicles.pack(pady=10)

            rented_vehicles_listbox = Listbox(rented_vehicles_window)
            rented_vehicles_listbox.pack(fill=BOTH, expand=True)

            scrollbar = Scrollbar(rented_vehicles_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            rented_vehicles_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=rented_vehicles_listbox.yview)

            sort_key = self.sort_criteria.get()  # Get the selected sorting criteria

            if sort_key == "Index":
                sorted_vehicles = sorted(self.rented_vehicles, key=lambda x: x['Index'])
            elif sort_key == "License Plate":
                sorted_vehicles = sorted(self.rented_vehicles, key=lambda x: x['License Plate'])
            else:
                sorted_vehicles = self.rented_vehicles

            for vehicle in sorted_vehicles:
                vehicle_info = f"Index: {vehicle['Index']} | License Plate: {vehicle['License Plate']} | Renter Name: {vehicle['Renter Name']}"
                rented_vehicles_listbox.insert(END, vehicle_info)
            update_button = Button(rented_vehicles_listbox, text="Update", command=lambda: self.update_record(rented_vehicles_listbox))
            update_button.pack(side=RIGHT)

        else:
            messagebox.showinfo("No Vehicles Rented", "There are no vehicles rented.")


    def sort_rented_vehicles(self, sort_key):
        if self.rented_vehicles:
            if sort_key == "Index":
                sorted_vehicles = sorted(self.rented_vehicles, key=lambda x: x['Index'])
            elif sort_key == "License Plate":
                sorted_vehicles = sorted(self.rented_vehicles, key=lambda x: x['License Plate'])
            elif sort_key == "Renter Name":
                sorted_vehicles = sorted(self.rented_vehicles, key=lambda x: x['Renter Name'])
            else:
                return

            sorted_vehicles_window = Toplevel(self.root)
            sorted_vehicles_window.title("Sorted Rented Vehicles")
            sorted_vehicles_window.geometry("400x300")

            lbl_sorted_vehicles = Label(sorted_vehicles_window, text="Sorted Rented Vehicles", font=("Helvetica", 14, "bold"))
            lbl_sorted_vehicles.pack(pady=10)

            sorted_vehicles_listbox = Listbox(sorted_vehicles_window)
            sorted_vehicles_listbox.pack(fill=BOTH, expand=True)

            scrollbar = Scrollbar(sorted_vehicles_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            sorted_vehicles_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=sorted_vehicles_listbox.yview)

            for vehicle in sorted_vehicles:
                vehicle_info = f"Index: {vehicle['Index']} | License Plate: {vehicle['License Plate']} | Renter Name: {vehicle['Renter Name']}"
                sorted_vehicles_listbox.insert(END, vehicle_info)
        else:
            messagebox.showinfo("No Vehicles Rented", "There are no vehicles rented.")


    def filter_rented_vehicles(self):
        if self.rented_vehicles:
            filter_window = Toplevel(self.root)
            filter_window.title("Filter Rented Vehicles")
            filter_window.geometry("400x300")

            lbl_filter = Label(filter_window, text="Filter by License Plate:")
            lbl_filter.pack(pady=10)

            filter_entry = Entry(filter_window)
            filter_entry.pack()

            btn_filter = Button(filter_window, text="Apply Filter",
                                command=lambda: self.apply_filter(filter_entry.get(), filter_window))
            btn_filter.pack(pady=10)
        else:
            messagebox.showinfo("No Vehicles Rented", "There are no vehicles rented.")

    def apply_filter(self, filter_text, filter_window):
        filtered_vehicles = [vehicle for vehicle in self.rented_vehicles if
                             vehicle['License Plate'].startswith(filter_text)]
        filter_window.destroy()

        if filtered_vehicles:
            filtered_vehicles_window = Toplevel(self.root)
            filtered_vehicles_window.title("Filtered Rented Vehicles")
            filtered_vehicles_window.geometry("400x300")

            lbl_filtered_vehicles = Label(filtered_vehicles_window, text="Filtered Rented Vehicles",
                                          font=("Helvetica", 14, "bold"))
            lbl_filtered_vehicles.pack(pady=10)

            filtered_vehicles_listbox = Listbox(filtered_vehicles_window)
            filtered_vehicles_listbox.pack(fill=BOTH, expand=True)

            scrollbar = Scrollbar(filtered_vehicles_window)
            scrollbar.pack(side=RIGHT, fill=Y)

            filtered_vehicles_listbox.config(yscrollcommand=scrollbar.set)
            scrollbar.config(command=filtered_vehicles_listbox.yview)

            for vehicle in filtered_vehicles:
                vehicle_info = f"Index: {vehicle['Index']} | License Plate: {vehicle['License Plate']} | Renter Name: {vehicle['Renter Name']}"
                filtered_vehicles_listbox.insert(END, vehicle_info)
        else:
            messagebox.showinfo("No Vehicles Found", "No vehicles found with the specified filter.")

    def clear_fields(self):
        self.license_plate.set("")
        self.renter_name.set("")
        self.vehicle_model.set("")


root = Tk()
VehicleRentalSystem(root)
root.mainloop()
