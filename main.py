def generate_sql_query():
    # Prompt user for polygon coordinates
    print("Enter the coordinates of the polygon vertices (latitude longitude):")
    polygon_vertices = []
    while True:
        vertex = input("Enter vertex (or 'done' if finished): ")
        if vertex.lower() == 'done':
            break
        try:
            lat, lon = map(float, vertex.split())
            polygon_vertices.append((lat, lon))
        except ValueError:
            print("Invalid input. Please enter latitude and longitude separated by space.")

    # Prompt user for the name of the area
    area_name = input("Enter the name of the bounded area: ")

    # Generate the SQL query
    if len(polygon_vertices) < 3:
        print("At least three vertices are required to define a polygon.")
        return

    # Create the bounding box conditions
    bounding_box_conditions = [
        f"(t.lat BETWEEN {min(v[0] for v in polygon_vertices)} AND {max(v[0] for v in polygon_vertices)})",
        f"(t.lon BETWEEN {min(v[1] for v in polygon_vertices)} AND {max(v[1] for v in polygon_vertices)})"
    ]

    # Create the conditions for each polygon vertex
    vertex_conditions = []
    for v, next_v in zip(polygon_vertices, polygon_vertices[1:] + [polygon_vertices[0]]):
        vertex_conditions.append(f"(t.lat < {next_v[0]} AND t.lon < {next_v[1]})")

    # Combine all conditions with OR for polygon vertices
    polygon_condition = " OR ".join(vertex_conditions)

    # Combine all conditions into the final SQL query
    sql_query = f"""
    SELECT *,
    CASE WHEN ({polygon_condition}) THEN '{area_name}' ELSE NULL END AS location
    FROM SQL_EDITOR_All_Panama_PWandLS_Feb2023_to_Feb2024_TABLE AS t
    WHERE
        ({' AND '.join(bounding_box_conditions)});
    """

    return sql_query

if __name__ == "__main__":
    sql_query = generate_sql_query()
    print("\nGenerated SQL Query:")
    print(sql_query)
