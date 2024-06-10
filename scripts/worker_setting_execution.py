import os
import csv
import time
import random
import logging
import argparse
from subprocess import check_output
from time import perf_counter

logging_format='%(asctime)s [%(levelname)s]: %(message)s'
logging.basicConfig(level=logging.INFO, format=logging_format, filename='utils/worker.log', filemode='a')
logger = logging.getLogger(__name__)

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('--enabled', type=str, help='Enabled settings separated by commas', default="")
parser.add_argument('--gradle-task', type=str, help='Gradle task to run', default="connectedDebugAndroidTest")
parser.add_argument('--app-folder', type=str, help='App folder')
parser.add_argument('--reports-folder', type=str, help='Reports folder')
parser.add_argument('--new-reports-folder', type=str, help='Folder to copy the reports to')
parser.add_argument('--strategy-name', type=str, help='Testing strategy name')
parser.add_argument('--execution', type=int, help='Current execution number')
parser.add_argument('--setting-id', type=int, help='Resource setting id')
parser.add_argument('--debug', type=bool, help='Run the commands', default=False)

args = parser.parse_args()

def get_setting_resources(enabled_resources_string):
    resources_dict = {}
    enabled_resources = enabled_resources_string.split(',') if enabled_resources_string else []
    disabled_resources = ['location','wifi','mobiledata','bluetooth','autorotate','batterysaver','donotdisturb', 'camera','accelerometer','gyroscope','magneticfield','proximity']

    for setting in enabled_resources:
        disabled_resources.remove(setting)

    for resource in enabled_resources:
        resources_dict[resource] = True

    for resource in disabled_resources:
        resources_dict[resource] = False

    return resources_dict

def get_gradle_args(resource_dict):
    gradle_args = []
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.locationEnabled={resource_dict['location']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.wifiEnabled={resource_dict['wifi']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.mobileDataEnabled={resource_dict['mobiledata']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.bluetoothEnabled={resource_dict['bluetooth']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.autoRotateEnabled={resource_dict['autorotate']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.batterySaverEnabled={resource_dict['batterysaver']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.doNotDisturbEnabled={resource_dict['donotdisturb']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.cameraEnabled={resource_dict['camera']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.accelerometerEnabled={resource_dict['accelerometer']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.gyroscopeEnabled={resource_dict['gyroscope']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.magneticFieldEnabled={resource_dict['magneticfield']}")
    gradle_args.append(f"-Pandroid.testInstrumentationRunnerArguments.proximityEnabled={resource_dict['proximity']}")
    return ' '.join(gradle_args)

def get_test_suit_command(resource_dict, gradle_task):
    gradle_args = get_gradle_args(resource_dict)
    return f"./gradlew {gradle_args} {gradle_task}"

def run_command(command):
    logger.debug(f"Executing {command}")

    if args.debug:
        return None

    os.system(command)

def print_statistics_to_csv(stats):
    reports_path = args.new_reports_folder.split('/execution')[0]
    file_path = f'{reports_path}/execution_statistics.csv'
    execution_number = args.execution
    setting_id = args.setting_id
    
    if not os.path.exists(file_path):
        with open(file_path, mode='w') as stats_file:
            stats_writer = csv.writer(stats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            stats_writer.writerow(['execution_number', 'setting_id', *stats.keys()])

    with open(file_path, mode='a') as stats_file:
        stats_writer = csv.writer(stats_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        stats_writer.writerow([execution_number, setting_id, *stats.values()])

    logger.info(f"Statistics saved to {reports_path}")

if __name__ == '__main__':
    start_time = perf_counter() 
    resource_dict = get_setting_resources(args.enabled)
    app_folder = args.app_folder
    strategy_name = args.strategy_name
    execution_number = args.execution
    setting_id = args.setting_id
    new_reports_folder = args.new_reports_folder

    logger.info(f"Running test suite for {strategy_name} with setting id {setting_id} and execution number {execution_number}")

    os.chdir(app_folder)
    os.makedirs(new_reports_folder, exist_ok=True)

    run_command("adb shell dumpsys battery unplug")

    resource_dict = get_setting_resources(args.enabled)
    gradle_task = args.gradle_task
    run_test_suit_command = get_test_suit_command(resource_dict, gradle_task)
    run_command(run_test_suit_command)

    run_command("adb shell dumpsys battery reset")

    reports_folder = args.reports_folder
    run_command(f"cp -Rf {reports_folder}/* {new_reports_folder}") # copy the content of the reports folder

    time_taken = perf_counter() - start_time

    print_statistics_to_csv({
        'time_taken': time_taken
    })

    logger.info(f"Time taken for the current config: {time_taken}")
    logger.info(f"Test suite execution completed for {strategy_name} with setting id {setting_id} on execution number {execution_number}")