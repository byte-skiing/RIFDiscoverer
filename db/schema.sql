CREATE TABLE IF NOT EXISTS execution_parameters
(
    id INTEGER UNIQUE PRIMARY KEY,
    name TEXT,
    value TEXT
);

CREATE TABLE IF NOT EXISTS resources 
(
    id INTEGER UNIQUE PRIMARY KEY,
    table_name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS testing_stragies
(
    id INTEGER UNIQUE PRIMARY KEY,
    file_name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL,
    is_from_db BOOLEAN NOT NULL DEFAULT FALSE,
    is_custom BOOLEAN NOT NULL DEFAULT FALSE,
    is_random BOOLEAN NOT NULL DEFAULT FALSE,
    is_range_strategy BOOLEAN NOT NULL DEFAULT FALSE,
    range_end INTEGER DEFAULT NULL
);

CREATE TABLE IF NOT EXISTS resource_settings
(
    setting_id INTEGER NOT NULL,
    strategy_id INTEGER NOT NULL,
    resource_id INTEGER NOT NULL,
    is_enabled BOOLEAN NOT NULL DEFAULT FALSE,
    resource_table_name TEXT,
    strategy_file_name TEXT,

    PRIMARY KEY (setting_id, strategy_id, resource_id),
    FOREIGN KEY (setting_id) REFERENCES settings(id),
    FOREIGN KEY (strategy_id) REFERENCES testing_stragies(id),
    FOREIGN KEY (resource_id) REFERENCES resources(id)
);

CREATE TRIGGER IF NOT EXISTS update_resource_settings
AFTER INSERT ON resource_settings
BEGIN
    UPDATE resource_settings
    SET resource_table_name = (SELECT table_name FROM resources WHERE id = resource_id),
        strategy_file_name = (SELECT file_name FROM testing_stragies WHERE id = strategy_id)
    WHERE 
        setting_id = NEW.setting_id AND 
        strategy_id = NEW.strategy_id AND 
        resource_id = NEW.resource_id AND 
        is_enabled = NEW.is_enabled;
END;