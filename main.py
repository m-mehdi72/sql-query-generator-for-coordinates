def generate_query(table_name, column_names, entries):
    query = f"SELECT * FROM {table_name}\nWHERE "
    conditions = []

    for i, values in enumerate(zip(*[entries[column] for column in column_names])):
        column_conditions = []
        for column_name, value in zip(column_names, values):
            column_conditions.append(f"LOWER({column_name}) LIKE LOWER('%{value}%')")
        conditions.append("(" + " AND ".join(column_conditions) + ")")

    query += " OR ".join(conditions) + ";"
    return query

def main():
    table_name = input("Enter the name of the table: ")
    num_columns = int(input("Enter the number of columns: "))

    column_names = []
    for i in range(num_columns):
        column_name = input(f"Enter the name of column {i + 1}: ")
        column_names.append(column_name)

    entries = {column_name: [] for column_name in column_names}
    print("Enter the list of entries for each column (one entry per line). Type 'done' for each column when finished.")
    for column_name in column_names:
        print(f"For column '{column_name}':")
        while True:
            entry = input().strip()
            if entry.lower() == 'done':
                break
            entries[column_name].append(entry)

    query = generate_query(table_name, column_names, entries)
    print("\nGenerated SQL query:")
    print(query)

if __name__ == "__main__":
    main()
