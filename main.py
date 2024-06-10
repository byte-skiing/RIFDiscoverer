import os 
import sys
import eel
import sqlite3
from tkinter import Tk, filedialog
from multiprocessing import Process

from utils.database import db
from scripts.socket_server import socket_server

@eel.expose
def get_folder_os_dialog():
	root = Tk()
	root.withdraw()
	root.wm_attributes('-topmost', 1)
	folder = filedialog.askdirectory()
	root.quit()
	return folder

@eel.expose
def set_app_project_folder(folder):
	db.execute("UPDATE execution_parameters SET value = ? WHERE name = 'app_project_folder'", (folder,))

@eel.expose
def set_test_reports_folder(folder):
	db.execute("UPDATE execution_parameters SET value = ? WHERE name = 'test_reports_folder'", (folder,))

@eel.expose
def set_number_of_executions(number):
	if int(number) < 1 or int(number) > 100:
		return False

	db.execute("UPDATE execution_parameters SET value = ? WHERE name = 'number_of_executions'", (number,))
	return True

@eel.expose
def set_gradle_task_name(task_name):
	db.execute("UPDATE execution_parameters SET value = ? WHERE name = 'gradle_task_name'", (task_name,))

@eel.expose
def get_execution_parameters():
	parameters = db.execute("SELECT name, value FROM execution_parameters")
	parameters_dict = {}

	for parameter in parameters:
		parameters_dict[parameter[0]] = parameter[1]

	return parameters_dict

@eel.expose
def get_available_resources():
	resources_json = []
	resources = db.execute("SELECT id, table_name, display_name FROM resources")

	for resource in resources:
		resources_json.append({
			'id': resource[0],
			'table_name': resource[1],
			'display_name': resource[2]
		})

	return resources_json

def _transform_strategy_query_to_json(strategy):
	return {
		'id': strategy[0],
		'file_name': strategy[1],
		'display_name': strategy[2],
		'is_from_db': strategy[3] == 1,
		'is_custom': strategy[4] == 1,
		'is_random': strategy[5] == 1,
		'is_range_strategy': strategy[6] == 1,
		'range_end': strategy[7]
	}

@eel.expose
def get_available_settings():
	strategies = db.execute("SELECT id, file_name, display_name, is_from_db, is_custom, is_random, is_range_strategy, range_end FROM testing_stragies")
	strategies_json = []

	for strategy in strategies:
		strategy_json = _transform_strategy_query_to_json(strategy)
		strategies_json.append(strategy_json)

	return strategies_json

def get_strategy_data(setting_name):
	strategy = db.execute("SELECT id, file_name, display_name, is_from_db, is_custom, is_random, is_range_strategy, range_end FROM testing_stragies WHERE file_name = ?", (setting_name,))

	if not strategy:
		return None

	return _transform_strategy_query_to_json(strategy)

def get_csv_file(file_path):
	if not os.path.exists(file_path):
		return None

	with open(file_path, 'r') as file:
		lines = file.readlines()
		return lines

def lines_to_dict(lines):
	if not lines:
		return None

	header = lines[0].strip().split(',')
	data = []
	for line in lines[1:]:
		data.append(dict(zip(header, line.strip().split(','))))

	return data

def get_complete_setting_from_dict(data):
	resources = []

	for key, value in data.items():
		if key == 'id':
			continue

		value = True if value.strip() == '1' else False
		resources.append({
			'table_name': key,
			'is_enabled': value
		})
	
	return {
		'id': data['id'],
		'resources': resources
	}


def get_strategy_settings_from_csv(setting_name):
	file_path = f'utils/settings/{setting_name}.csv'
	lines =  get_csv_file(file_path)
	settings_dicts = lines_to_dict(lines)

	if not settings_dicts:
		return None

	settings = []

	for setting in settings_dicts:
		completed_setting = get_complete_setting_from_dict(setting)
		settings.append(completed_setting)

	return settings

def get_strategy_from_db(strategy_file_name):
	stored_settings = db.execute("SELECT setting_id FROM resource_settings WHERE strategy_file_name = ? GROUP BY setting_id", (strategy_file_name,))
	stored_settings = stored_settings if isinstance(stored_settings, list) else [stored_settings]
	
	settings = []

	for stored_setting in stored_settings:
		resources = []
		setting_id = stored_setting[0]
		resource_settings = db.execute("SELECT resource_table_name, is_enabled FROM resource_settings WHERE setting_id = ? AND strategy_file_name = ?", (setting_id, strategy_file_name, ))

		for resource_setting in resource_settings:
			resources.append({
				'table_name': resource_setting[0],
				'is_enabled': resource_setting[1] == 1
			})

		settings.append({
			'id': setting_id,
			'resources': resources
		})

	return settings

def _get_strategy_settings(strategy_name, metadata, range):
	is_from_db = metadata['is_from_db']
	is_range_strategy = metadata['is_range_strategy']

	if is_from_db:
		return get_strategy_from_db(strategy_name)
	elif is_range_strategy:
		return get_strategy_settings_from_csv(strategy_name + f'-{range}') 
	else:
		return get_strategy_settings_from_csv(strategy_name)

@eel.expose
def create_resource_setting(strategy_id, resources):
	strategy = db.execute("SELECT is_from_db FROM testing_stragies WHERE id = ?", (strategy_id,))
	is_from_db = strategy[0] == 1
	
	if not is_from_db:
		return None

	last_setting_id = db.execute("SELECT MAX(setting_id) FROM resource_settings WHERE strategy_id = ?", (strategy_id,))[0]
	setting_id = 0 if last_setting_id is None else last_setting_id + 1

	for resource in resources:
		resource_id = resource['id']
		is_enabled = resource['is_enabled'] == 1
		
		db.execute("INSERT INTO resource_settings (setting_id, strategy_id, resource_id, is_enabled) VALUES (?, ?, ?, ?)", (setting_id, strategy_id, resource_id, is_enabled))

	return {
		'id': setting_id,
		'checkbox_enabled': is_from_db,
		'resources': resources
	}

def add_checkbox_state_to_settings(settings, metadata):
	is_from_db = metadata['is_from_db']

	for i, setting in enumerate(settings):
		settings[i] = {
			**setting,
			'checkbox_enabled': is_from_db
		}

	return settings

@eel.expose
def get_testing_strategy(strategy_name, range=None):
	metadata = get_strategy_data(strategy_name)
	settings = _get_strategy_settings(strategy_name, metadata, range)
	settings_with_checkbox = add_checkbox_state_to_settings(settings, metadata)

	return {
		**metadata,
		'selected_range': int(range) if metadata['is_range_strategy'] else None,
		'settings': settings_with_checkbox
	}

@eel.expose
def delete_testing_strategies_resource_settings(strategy, settings):
	strategy_id = strategy['id']
	settings_ids = [setting['id'] for setting in settings]

	for setting_id in settings_ids:
		db.execute("DELETE FROM resource_settings WHERE strategy_id = ? AND setting_id = ?", (strategy_id, setting_id,))

	updated_settings = []
	settings = db.execute("SELECT setting_id FROM resource_settings WHERE strategy_id = ? GROUP BY setting_id ORDER BY setting_id", (strategy_id,))

	for i, setting in enumerate(settings):
		db.execute("UPDATE resource_settings SET setting_id = ? WHERE strategy_id = ? AND setting_id = ?", (i, strategy_id, setting[0],))
		updated_settings.append({
			'previous_id': setting[0],
			'new_id': i
		})

	return updated_settings

socket_process = Process(target=socket_server, args=())

@eel.expose
def open_folder(folder_path):
	if sys.platform == 'win32':
		os.system(f'start {folder_path}') # Windows
	elif sys.platform == 'darwin':
		os.system(f'open {folder_path}') # MacOS
	else:
		os.system(f'xdg-open {folder_path}') # Linux

def eel_start():
	def close_callback(route, websockets):
		if not websockets:
			socket_process.terminate()
			sys.exit(0)

	try:
		eel.init('public')
		eel.start('index.html', mode='chrome', size=(1600, 900), close_callback=close_callback)
	except Exception as e:
		eel.start('index.html', mode='default', size=(1600, 900), close_callback=close_callback)
	
if __name__ == '__main__':
	try:
		socket_process.start()
		eel_start()
	except KeyboardInterrupt:
		sys.exit(0)
