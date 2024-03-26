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
    min_lat = min(v[0] for v in polygon_vertices)
    max_lat = max(v[0] for v in polygon_vertices)
    min_lon = min(v[1] for v in polygon_vertices)
    max_lon = max(v[1] for v in polygon_vertices)
    bounding_box_conditions = [
        f"(t.lat BETWEEN {min_lat} AND {max_lat})",
        f"(t.lon BETWEEN {min_lon} AND {max_lon})"
    ]

    # Create individual vertex conditions
    vertex_conditions = []
    for vertex in polygon_vertices:
        vertex_condition = f"(t.lat < {vertex[0]} AND t.lon < {vertex[1]})"
        vertex_conditions.append(vertex_condition)

    # Combine all conditions into the final SQL query
    sql_query = f"""
    SELECT *,
    CASE WHEN {' OR '.join(['(' + cond + ')' for cond in vertex_conditions])} THEN '{area_name}' ELSE NULL END AS location
    FROM SQL_EDITOR_All_Panama_PWandLS_Feb2023_to_Feb2024_TABLE AS t
    WHERE
        {' AND '.join(bounding_box_conditions)} AND
        ({' OR '.join([cond for cond in vertex_conditions])});
    """

    return sql_query

if __name__ == "__main__":
    sql_query = generate_sql_query()
    print("\nGenerated SQL Query:")
    print(sql_query)
