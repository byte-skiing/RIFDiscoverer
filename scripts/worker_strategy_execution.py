import os
import csv
import time
import random
import asyncio
import logging

async def check_output(cmd):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    stdout, stderr = await proc.communicate()
    return proc.returncode, stdout, stderr

def get_enabled_resources_string(resources):
    enabled_resources = []

    for resource in resources:
        table_name = resource['table_name']

        if resource['is_enabled']:
            enabled_resources.append(table_name)
    
    return ','.join(enabled_resources)

def settings_to_csv(settings, reports_folder_path):
    file_path = f'{reports_folder_path}/settings.csv'

    with open(file_path, mode='w') as settings_file:
        settings_writer = csv.writer(settings_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        for setting in settings:
            setting_id = setting['id']
            enabled_resources = []

            for resource in setting['resources']:
                if resource['is_enabled']:
                    enabled_resources.append(resource['table_name'])

            settings_writer.writerow([setting_id, *enabled_resources])

async def run_testing_strategy(execution_parameters, strategy, handleBroadcast, abort_event):
    settings = strategy['settings']
    strategy_name = strategy['file_name']
    strategy_display_name = strategy['display_name']
    app_folder = execution_parameters['app_project_folder']
    reports_folder = execution_parameters['test_reports_folder']
    gradle_task = execution_parameters['gradle_task_name']
    number_of_executions = int(execution_parameters['number_of_executions'])
    strategy_reports_folder = f"testReports-{strategy_name}/{time.strftime('%Y-%m-%d-%H%M%S')}"
    logs_file_path = f'{app_folder}/{strategy_reports_folder}/strategy.log'

    os.makedirs(os.path.dirname(logs_file_path), exist_ok=True)
    open(logs_file_path, 'w').close()

    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s]: %(message)s', filename=logs_file_path, filemode='a', force=True)
    logger = logging.getLogger(strategy_name)

    async def broadcast(message, data):
        if message == 'printToTerminal':
            logger.info(data)

        await handleBroadcast(message, data)

    total_executions = number_of_executions * len(settings)
    await broadcast('startProgressBar', total_executions)

    await broadcast('printToTerminal', '========== Starting tests execution ==========')
    await broadcast('printToTerminal', f"Testing strategy: {strategy_display_name}")
    await broadcast('printToTerminal', f"Number of executions: {number_of_executions}")
    await broadcast('printToTerminal', f"Number of settings: {len(settings)}")
    await broadcast('printToTerminal', f"Total number of executions: {total_executions}")
    await broadcast('printToTerminal', f"App folder: {app_folder}")
    await broadcast('printToTerminal', f"Gradle reports folder: {reports_folder}")
    await broadcast('reportsFolderPath', f'{app_folder}/{strategy_reports_folder}')

    settings_to_csv(settings, f'{app_folder}/{strategy_reports_folder}')

    for execution_number in range(number_of_executions):   
        shuffled_settings = settings.copy()
        random.shuffle(shuffled_settings)

        await broadcast('printToTerminal', f'===== Starting execution {execution_number + 1}/{number_of_executions} =====')

        for setting_index, setting in enumerate(shuffled_settings):
            if abort_event.is_set():
                await broadcast('finishExecution', 'Execution aborted!')
                await broadcast('printToTerminal', 'Execution aborted!')
                return

            current_execution = (setting_index + 1) + (execution_number * len(settings))

            await broadcast('printToTerminal', f'[{current_execution}/{total_executions}] Starting tests for setting {setting["id"]} on execution ({execution_number + 1}/{number_of_executions})')

            setting_id = setting['id']
            enabled_resources = get_enabled_resources_string(setting['resources'])
            enabled_resources_param = f"--enabled {enabled_resources}" if enabled_resources else ""

            new_setting_reports_folder = f"{strategy_reports_folder}/execution{execution_number}/report{setting_id}"
            command = f"python3 scripts/worker_setting_execution.py {enabled_resources_param} --app-folder {app_folder} --reports-folder {reports_folder} --new-reports-folder {new_setting_reports_folder} --strategy-name {strategy_name} --execution {execution_number} --setting-id {setting_id} --gradle-task {gradle_task}"
            await check_output(command)

            await broadcast('printToTerminal', f'[{current_execution}/{total_executions}] Reports for setting {setting["id"]} on execution ({execution_number + 1}/{number_of_executions}) {new_setting_reports_folder}')
            await broadcast('printToTerminal', f'[{current_execution}/{total_executions}] Finished running tests for setting {setting["id"]} on execution ({execution_number + 1}/{number_of_executions})')
            await broadcast('updateProgressBar', current_execution)

    await broadcast('finishExecution', 'Finished running all tests!!')
    await broadcast('printToTerminal', f"The test report collection is available at {app_folder}/{strategy_reports_folder}")
    await broadcast('printToTerminal', '========== Finished tests execution ==========')
