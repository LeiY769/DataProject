CREATE TABLE IF NOT EXISTS railway (
    geom GEOMETRY(MULTILINESTRING, 4326),
    line_number VARCHAR(255),
    ptcarfrom VARCHAR(255)
) ; 