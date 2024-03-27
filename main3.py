def generate_sql_query():
    table_name = input("Enter your Table's name: ")
    
    print("Enter the coordinates of the polygon vertices (latitude longitude):\nEnter vertex (or 'done' if finished):")
    polygon_vertices = []
    while True:
        vertex = input()
        if vertex.lower() == 'done':
            break
        try:
            lat, lon = map(float, vertex.split())
            polygon_vertices.append((lat, lon))
        except ValueError:
            print("Invalid input. Please enter latitude and longitude separated by space.")

    
    area_name = input("Enter the name of the bounded area: ")

   
    if len(polygon_vertices) < 3:
        print("At least three vertices are required to define a polygon.")
        return


    min_lat = min(v[0] for v in polygon_vertices)
    max_lat = max(v[0] for v in polygon_vertices)
    min_lon = min(v[1] for v in polygon_vertices)
    max_lon = max(v[1] for v in polygon_vertices)
    bounding_box_conditions = [
        f"(t.lat BETWEEN {min_lat} AND {max_lat})",
        f"(t.lon BETWEEN {min_lon} AND {max_lon})"
    ]

    vertex_conditions = []
    for vertex in polygon_vertices:
        vertex_condition = f"(t.lat < {vertex[0]} AND t.lon < {vertex[1]})"
        vertex_conditions.append(vertex_condition)

    sql_query = f"""
    SELECT *,
    CASE WHEN {' OR '.join(['(' + cond + ')' for cond in vertex_conditions])} THEN '{area_name}' ELSE NULL END AS location
    FROM SQL_EDITOR_{table_name}_TABLE AS t
    WHERE
        {' AND '.join(bounding_box_conditions)} AND
        ({' OR '.join([cond for cond in vertex_conditions])});
    """

    return sql_query

if __name__ == "__main__":
    sql_query = generate_sql_query()
    print("\nGenerated SQL Query:")
    print(sql_query)
