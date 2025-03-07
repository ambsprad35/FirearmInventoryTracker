import tkinter as tk
from tkinter import ttk, messagebox

class Firearm:
    def __init__(self, firearmType, make, model):
        self.firearmType = firearmType
        self.make = make
        self.model = model
    
    def __str__(self):
        return f"{self.firearmType} - {self.make} {self.model}"

class Inventory:
    def __init__(self):
        self.firearms = []
    
    def addFirearm(self, firearm):
        self.firearms.append(firearm)
    
    def deleteFirearm(self, index):
        if 0 <= index < len(self.firearms):
            del self.firearms[index]
    
    def getInventory(self, firearmType=None):
        if firearmType:
            return [f for f in self.firearms if f.firearmType == firearmType]
        return self.firearms
    
    def getInventoryCount(self):
        return len(self.firearms)

class InventoryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cash America Firearm Inventory Tracker")
        self.inventory = Inventory()
        
        # Design the layout of the window
        ttk.Label(root, text="Firearm Type:").grid(row=0, column=0)
        self.type_var = ttk.Combobox(root, values=["Handgun", "Shotgun", "Rifle"], state="readonly")
        self.type_var.grid(row=0, column=1)
        
        ttk.Label(root, text="Manufacturer:").grid(row=1, column=0)
        self.make_entry = ttk.Entry(root)
        self.make_entry.grid(row=1, column=1)
        
        ttk.Label(root, text="Model:").grid(row=2, column=0)
        self.model_entry = ttk.Entry(root)
        self.model_entry.grid(row=2, column=1)
        
        self.add_button = ttk.Button(root, text="Add Firearm", command=self.addFirearm)
        self.add_button.grid(row=3, column=0, columnspan=2, pady=5)
        
        self.remove_button = ttk.Button(root, text="Delete Selected", command=self.deleteSelected)
        self.remove_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.filterType_var = ttk.Combobox(root, values=["All", "Handgun", "Shotgun", "Rifle"], state="readonly")
        self.filterType_var.grid(row=5, column=0)
        self.filterType_var.set("All")
        
        self.filter_button = ttk.Button(root, text="Filter", command=self.filter_inventory)
        self.filter_button.grid(row=5, column=1)
        
        self.tree = ttk.Treeview(root, columns=("Type", "Manufacturer", "Model"), show="headings")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Manufacturer", text="Manufacturer")
        self.tree.heading("Model", text="Model")
        self.tree.grid(row=6, column=0, columnspan=2)
        
        self.total_label = ttk.Label(root, text="Total Inventory: 0")
        self.total_label.grid(row=7, column=0, columnspan=2, pady=5)
        
    def addFirearm(self):
        # Add a firearm to the inventory
        firearmType = self.type_var.get()
        make = self.make_entry.get().strip()
        model = self.model_entry.get().strip()
        
        # Error checking - all fields must filled in before adding a firearm
        if not (firearmType and make and model):
            messagebox.showerror("Error", "All fields must be filled!")
            return
        
        # Add the firearm to the firearm inventory list
        firearm = Firearm(firearmType, make, model)
        self.inventory.addFirearm(firearm)

        # update the display list and clear the entry boxes
        self.updateList()
        self.make_entry.delete(0,'end')
        self.model_entry.delete(0, 'end')
        self.type_var.set("")
        
    def deleteSelected(self):
        # delete the selected firearm
        selected = self.tree.selection()
        # Error checking - ensure a firearm is selected before deleting
        if not selected:
            messagebox.showerror("Error", "No firearm selected!")
            return
        
        # Remove the selected firearms
        for item in selected:
            index = self.tree.index(item)
            self.inventory.deleteFirearm(index)
        # Update the firearm inventory list
        self.updateList()
        
    def filter_inventory(self):
        # Display the selected type of firearms - All, Handgun, Shotgun, Rifle
        filter_type = self.filterType_var.get()
        if filter_type == "All":
            firearms = self.inventory.getInventory()
        else:
            firearms = self.inventory.getInventory(filter_type)
        
        self.updateList(firearms)
        
    def updateList(self, firearms=None):
        # Update the list of firearms in the inventory
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        if firearms is None:
            firearms = self.inventory.getInventory()
        
        for firearm in firearms:
            self.tree.insert("", "end", values=(firearm.firearmType, firearm.make, firearm.model))
        
        self.total_label.config(text=f"Total Inventory: {self.inventory.getInventoryCount()}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InventoryApp(root)
    root.mainloop()
