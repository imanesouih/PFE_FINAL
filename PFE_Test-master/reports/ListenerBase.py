import threading
from jinja2 import Environment, FileSystemLoader
import yaml
import sys
import time
from datetime import timedelta
from datetime import datetime
import json
 
class ListenerBase:
    ROBOT_LISTENER_API_VERSION = 3
 
    def __init__(self, report_file='./results/oumayma.html', template_file='/reports/template3.html'):
        self.report_file = report_file
        self.template_file = template_file
        self.total_tests = 0
        self.total_passed = 0
        self.total_failed = 0
        self.total_skipped = 0
        self.suite_statistics = []
        self.test_case_statistics = []
        self.xray_tests_results = []
        self.is_closed = False
        self.start_time = None
        self.end_time = None
        self.lock = threading.Lock()
        self.summaryInformation = ()
        self.env_info = {}
        if '--variablefile' in sys.argv:
            index = sys.argv.index('--variablefile')
            env_file = sys.argv[index + 1]
            try:
                with open(env_file, 'r') as yaml_file:
                    self.env_info = yaml.safe_load(yaml_file)
            except FileNotFoundError:
                print(f"Error: File '{env_file}' not found.")
            except Exception as e:
                print(f"Error loading YAML file: {e}")
   
    def start_test(self, test, result):
        if self.start_time is None:
            start_time = result.starttime
            self.start_time = self.format_time(start_time)
 
    def start_suite(self, suite, result):
        suite_name = suite.name
        if suite.source and str(suite.source).lower().endswith('.robot') and suite.tests:

            start_time = result.starttime
            format_date_start = self.format_time(start_time)
            self.suite_stats = {
                'suite_name': suite_name,
                'total_tests': 0,
                'passed': 0,
                'failed': 0,
                'skipped': 0,
                'start_time': format_date_start,
                'end_time': None,
                'elapsed_time': None,
                'status': 'Running',
                'project_key': self.env_info.get('project_key', 'N/A'),
                'environment': self.env_info.get('environment', 'N/A'),
                'testeur': self.env_info.get('Testeur', 'N/A')
            }
           
    def end_suite(self, suite, result):
        if suite.id == 's1':
            self.summaryInformation = (suite.id, suite.name, result.statistics.total, result.statistics.passed, result.statistics.failed, result.statistics.skipped, result.statistics.message, result.starttime, result.endtime, result.elapsedtime)
        suite_name = suite.name
        if suite.source and str(suite.source).lower().endswith('.robot') and suite.tests:


            end_time = result.endtime
            format_date = self.format_time(end_time)
            elapsed_time = result.elapsedtime
            formated_elapsed_time = self.convert_elapsed_time(elapsed_time)
            self.suite_stats.update({
                'suite_name': suite_name,
                'status': result.status,
                'end_time': format_date,
                'elapsed_time': formated_elapsed_time,
                'total_tests': result.statistics.total,
                'passed': result.statistics.passed,
                'failed': result.statistics.failed,
                'skipped': result.statistics.skipped
            })
            self.suite_statistics.append(self.suite_stats)
 
    def end_test(self, test, result):
        suite_name = test.parent.longname
        self.test_case_statistics.append({
            'suite_name': suite_name,
            'test_name': test.name,
            'status': result.status,
            'message': result.message,
            'tags': test.tags
        })
        test_case_id = test.tags[0] if test.tags else None
        if test_case_id:
            self.xray_tests_results.append({
                "testKey": test_case_id,
                "suite_name": suite_name,
                "test_name": test.name,
                "status": result.status,
                "start": self.start_time,
                "finish": result.endtime,
                "comment": result.message,
                "testeur": self.env_info.get('Testeur', 'N/A'),  # Ajout du testeur
                "environment": self.env_info.get('environment', 'N/A')  # Ajout de l'environnement
               
            })
       
        #
        # self.update_report()
       
    def close(self):
        if not self.is_closed:
            self.is_closed = True
            self.end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            self.update_report()
            self.generate_custom_json_report()
 
    def update_report(self):
        env = Environment(loader=FileSystemLoader('.'))
        template = env.get_template(self.template_file)
 
        total_tests, passed, failed, skipped = self.summaryInformation[2:6]
        summary_data = {
            "total_tests": total_tests,
            "total_passed": passed,
            "total_failed": failed,
            "total_skipped": skipped,
            "tests": self.xray_tests_results
           
        }
 
        rendered_template = template.render(
            suite_statistics=self.suite_statistics,
            test_case_statistics=self.test_case_statistics,
            xray_tests_results=self.xray_tests_results,
            env_info=self.env_info,
            start_time=self.start_time,
            end_time=self.end_time,
            summaryInformation=self.summaryInformation,
            summary_data=summary_data
        )
 
        with open(self.report_file, 'w') as f:
            f.write(rendered_template)
 
        json_data = {"tests": self.xray_tests_results, **summary_data}  
        with open('test_result21.json', 'w') as json_out:
            json.dump(json_data, json_out, indent=4)
 
    def generate_custom_json_report(self, filename='custom_results.json'):
        env = Environment(loader=FileSystemLoader('.'))
        custom_results = {
            "summary": {
                "info": {
                    "project": self.env_info.get("Projet", "N/A"),
                    "summary": "Your summary here",
                    "description": "Your description here",
                    "environment": self.env_info.get("environment", "N/A"),
                    "user": self.env_info.get("Testeur", "N/A")
                }
            },
            "tests": []
        }
        
        for result in self.xray_tests_results:
            custom_result = {
                "testKey": result["testKey"],
                "start": result.get("start", ""),
                "finish": self.format_time(result.get("finish", "")),  
                "comment": result.get("comment", ""),
                "status": result.get("status", "")
            }
            custom_results["tests"].append(custom_result)

        with open(filename, 'w') as json_out:
            json.dump(custom_results, json_out, indent=4)

    def convert_elapsed_time(self, elapsed_ms):
        if elapsed_ms:
            elapsed_time = timedelta(milliseconds=elapsed_ms)
            hours = elapsed_time.seconds // 3600
            minutes = (elapsed_time.seconds % 3600) // 60
            seconds = elapsed_time.seconds % 60
            milliseconds = elapsed_time.microseconds // 1000
            return f"{hours}:{minutes}:{seconds}.{milliseconds}"
        return "N/A"
   
    def format_time(self, time_str):
        return datetime.strptime(time_str, '%Y%m%d %H:%M:%S.%f').strftime('%Y-%m-%d %H:%M:%S')
 
# Instantiate TestListener
listener = ListenerBase()
