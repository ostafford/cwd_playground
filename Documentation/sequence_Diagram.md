```mermaid 
sequenceDiagram
    autonumber
    participant User
    participant UI as UserInterface
    participant PM as PantryManager
    participant SH as StorageHandler
    
    Note over User,SH: Application Startup
    UI->>PM: initialize()
    PM->>SH: load()
    SH-->>PM: stored_data
    

    Note over User,SH: Add Item Flow
    User->>UI: select "Add Item"
    UI->>UI: display_categories()
    User->>UI: select/create category
    UI->>UI: display_item_form()
    User->>UI: input item details
    UI->>PM: add_item(item)
    PM->>SH: save()
    
    Note over User,SH: View Inventory
    User->>UI: select "View Inventory"
    UI->>PM: get_items_by_category()
    PM-->>UI: items
    UI->>User: display items
    
    Note over User,SH: Application Exit
    User->>UI: select "Exit"
    UI->>PM: save_data()
    PM->>SH: backup()
```

<h2>Description</h2>

<details><summary><u>Application Startup Flow</u></summary>

### When the app starts:

1. UserInterface initializes PantryManager
2. PantryManager requests data (fileName.csv) from StorageHandler
3. StorageHandler loads and returns stored data
- The app is now ready with user's previous inventory
</details>

<details><summary><u>Add Item Flow</u></summary>

### User initiates add item process

1. Shows available categories
2. Lets user select existing or create new category
3. Displays form for item details

### After user inputs details:

4. Data flows through UI → PantryManager → StorageHandler
5. StorageHandler saves the updated inventory
</details>

<details><summary><u>View Inventory Flow</u></summary>

### User requests to view inventory

1. UI requests items from PantryManager
2. PantryManager returns categorized items
3. UI displays organized inventory to user
</details>

<details><summary><u>Application Exit Flow</u></summary>

### User selects exit

1. UI triggers PantryManager to save
2. PantryManager tells StorageHandler to backup
3. Ensures data is safely stored and backed up
</details>
