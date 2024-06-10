INSERT INTO execution_parameters (id, name, value) 
VALUES 
    (0, 'app_project_folder', ''),
    (1, 'test_reports_folder', ''),
    (2, 'number_of_executions', '3'),
    (3, 'gradle_task_name', 'connectedDebugAndroidTest')
    ON CONFLICT (id) DO NOTHING;

INSERT INTO resources (id, table_name, display_name) 
VALUES
    (0, 'location', 'Location'),
    (1, 'wifi', 'Wi-Fi'),
    (2, 'mobiledata', 'Mobile Data'),
    (3, 'bluetooth', 'Bluetooth'),
    (4, 'autorotate', 'Auto Rotate'),
    (5, 'batterysaver', 'Battery Saver'),
    (6, 'donotdisturb', 'Do Not Disturb'),
    (7, 'camera', 'Camera'),
    (8, 'accelerometer', 'Accelerometer'),
    (9, 'gyroscope', 'Gyroscope'),
    (10, 'magneticfield', 'Magnetic Field'),
    (11, 'proximity', 'Proximity')
    ON CONFLICT (id) DO NOTHING;

INSERT INTO testing_stragies (id, file_name, display_name)
VALUES
    (0, 'one-enabled', 'One-Enabled'),
    (1, 'one-disabled', 'One-Disabled'),
    (2, 'most-enabled-disabled', 'Most-Enabled-Disabled'),
    (3, 'pairwise', 'Pairwise'),
    (4, 'incling', 'IncLing')
    ON CONFLICT (id) DO NOTHING;

INSERT INTO testing_stragies (id, file_name, display_name, is_range_strategy, range_end)
VALUES
    (5, 'casa', 'CASA', TRUE, 3),
    (6, 'chvatal', 'Chvatal', TRUE, 3),
    (7, 'icpl', 'ICPL', TRUE, 3)
    ON CONFLICT (id) DO NOTHING;

INSERT INTO testing_stragies (id, file_name, display_name, is_from_db, is_custom, is_random)
VALUES
    (8, 'custom', 'Custom', TRUE, TRUE, FALSE),
    (9, 'random', 'Random', TRUE, FALSE, TRUE)
    ON CONFLICT (id) DO NOTHING;

INSERT INTO resource_settings (setting_id, strategy_id, resource_id, is_enabled)
VALUES
    (0, 8, 0, FALSE),
    (0, 8, 1, FALSE),
    (0, 8, 2, FALSE),
    (0, 8, 3, FALSE),
    (0, 8, 4, FALSE),
    (0, 8, 5, FALSE),
    (0, 8, 6, FALSE),
    (0, 8, 7, FALSE),
    (0, 8, 8, FALSE),
    (0, 8, 9, FALSE),
    (0, 8, 10, FALSE),
    (0, 8, 11, FALSE),
    (1, 8, 0, TRUE),
    (1, 8, 1, TRUE),
    (1, 8, 2, TRUE),
    (1, 8, 3, TRUE),
    (1, 8, 4, TRUE),
    (1, 8, 5, TRUE),
    (1, 8, 6, TRUE),
    (1, 8, 7, TRUE),
    (1, 8, 8, TRUE),
    (1, 8, 9, TRUE),
    (1, 8, 10, TRUE),
    (1, 8, 11, TRUE)
ON CONFLICT (setting_id, strategy_id, resource_id) DO NOTHING;

INSERT INTO resource_settings (setting_id, strategy_id, resource_id, is_enabled)
VALUES
    (0, 9, 0, FALSE),
    (0, 9, 1, FALSE),
    (0, 9, 2, FALSE),
    (0, 9, 3, FALSE),
    (0, 9, 4, FALSE),
    (0, 9, 5, FALSE),
    (0, 9, 6, FALSE),
    (0, 9, 7, FALSE),
    (0, 9, 8, FALSE),
    (0, 9, 9, FALSE),
    (0, 9, 10, FALSE),
    (0, 9, 11, FALSE),
    (1, 9, 0, TRUE),
    (1, 9, 1, TRUE),
    (1, 9, 2, TRUE),
    (1, 9, 3, TRUE),
    (1, 9, 4, TRUE),
    (1, 9, 5, TRUE),
    (1, 9, 6, TRUE),
    (1, 9, 7, TRUE),
    (1, 9, 8, TRUE),
    (1, 9, 9, TRUE),
    (1, 9, 10, TRUE),
    (1, 9, 11, TRUE)
ON CONFLICT (setting_id, strategy_id, resource_id) DO NOTHING;