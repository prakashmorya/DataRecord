import psycopg2
import pandas as pd


# database connection
def connection():
    return psycopg2.connect(
        dbname="automark_india",
        user="postgres",
        password="Jai2525",
        host="localhost",
        port="5432"
    )

# get data from the user 

# --- Insert Record ---
def insert_record():
    conn = connection()
    cur = conn.cursor()
    entry_date = input("Enter date (YYYY-MM-DD): ")
    type_var = input("Enter type (e.g., Income/Expense): ")
    entry_desc = input("Enter description: ")
    entry_amount = input("Enter amount: ")

    cur.execute("""
        INSERT INTO finance_records (date, type, description, amount)
        VALUES (%s, %s, %s, %s)
    """, (entry_date, type_var, entry_desc, entry_amount))
    conn.commit()
    conn.close()
    print("Success: Record added successfully")
    
#save data to excel
def save_to_excel():
    conn = connection()
    
    query="SELECT * FROM finance_records"
    df= pd.read_sql(query,conn)

    df.to_excel('output.xlsx',index=False)
    conn.close()
    

# get all data 
def getData():
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM finance_records")
    
    data = cur.fetchall()
    
    conn.close()
    

    if not data:
        print("No records found.")
    else:
        headers = [desc[0] for desc in cur.description]
        print(" | ".join(f"{h:<20}" for h in headers))
        print("-" * (len(headers) * 18))

        for row in data:
     
         print(" | ".join(f"{str(item):<20}" for item in row))
          
# update data 

def update_data():
    record_id = int(input("Enter record ID to update: "))
    conn = connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM finance_records WHERE id = %s", (record_id,))
    data = cur.fetchone()

    if not data:
        print(f"⚠️ No record found with ID {record_id}.\n")
        conn.close()
        return

    print("Current record:", data)
    print("""
Which field do you want to update?
1. Date
2. Type
3. Description
4. Amount
5. All fields
""")
    choice = input("Enter your choice (1-5): ")

    # Use match-case to handle update choice
    match choice:
        case "1":
            new_date = input("Enter new date (YYYY-MM-DD): ")
            cur.execute("UPDATE finance_records SET date = %s WHERE id = %s", (new_date, record_id))

        case "2":
            new_type = input("Enter new type (Income/Expense): ")
            cur.execute("UPDATE finance_records SET type = %s WHERE id = %s", (new_type, record_id))

        case "3":
            new_desc = input("Enter new description: ")
            cur.execute("UPDATE finance_records SET description = %s WHERE id = %s", (new_desc, record_id))

        case "4":
            new_amount = float(input("Enter new amount: "))
            cur.execute("UPDATE finance_records SET amount = %s WHERE id = %s", (new_amount, record_id))

        case "5":
            new_date = input("Enter new date (YYYY-MM-DD): ")
            new_type = input("Enter new type (Income/Expense): ")
            new_desc = input("Enter new description: ")
            new_amount = float(input("Enter new amount: "))
            cur.execute("""
                UPDATE finance_records
                SET date=%s, type=%s, description=%s, amount=%s
                WHERE id=%s
            """, (new_date, new_type, new_desc, new_amount, record_id))

        case _:
            print("⚠️ Invalid choice. No changes made.")
            conn.close()
            return

    conn.commit()
    conn.close()
    print("✅ Record updated successfully!\n")


# --- Program Start ---
def main():
    print("""
========= Finance Tracker =========
1. Add a new record
2. View all records
3. Update data
4. Exit
5. To save data in excel
===================================
""")
    while True:
        choice = input("Enter your choice (1/2/3/4/5): ")

        match choice:
            case "1":
                print("🟢 Adding a new record...")
                insert_record()

            case "2":
                print("📋 Fetching records...")
                getData()

            case "3":
                print("👋 update the data.")
                update_data()

            case "4":
                print("👋 Exiting program.")
                break
            case "5":
                print("save to data in excel.")
                save_to_excel()
                break

            case _:
                print("⚠️ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
