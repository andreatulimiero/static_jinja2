import os, sys, time
import json
import jinja2
from jinja2 import Environment, PackageLoader
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

def create_templates_folder():
  if 'templates' not in os.listdir():
    os.mkdir('templates')
    print('Created templates directory')
  if '__init__.py' not in os.listdir('templates'):
    open('templates/__init__.py', mode='w+').close()
  if '_index.html' not in os.listdir('templates'):
    open('templates/_index.html', mode='w+').close()
    print('Created _index.html')


supported_files = ['html', 'htm']
create_templates_folder()
env = Environment(loader=PackageLoader('templates', '.'))

def get_config_file():
  with open('templates/.config.json') as f:
    try:
      return json.loads(f.read().strip())
    except ValueError:
      print('.config.json is malformed')
    return {}

def render_template():
    template = env.get_template('_index.html')
    with open('index.html', mode='w+') as f:
      try:
        rendered_template = template.render(get_config_file())
        print(rendered_template, file=f)
      except jinja2.exceptions.TemplateNotFound as TemplateNotFound:
        print(TemplateNotFound.name + ' not found')
        return
      except jinja2.exceptions.TemplateSyntaxError as TemplateSyntaxError:
        print(
          'Wrong formatting at line ' + str(TemplateSyntaxError.lineno) + ' in ' + TemplateSyntaxError.filename +
          ': \n\n' + TemplateSyntaxError.message + '\n'
          )
      print('Rendered _index.html -> index.html')

class EventHandler(FileSystemEventHandler):
  def on_modified(self, event):
    file_path = event.src_path.replace('\\', '/')
    if file_path.split('.')[-1] in supported_files:
      print('Modified ' + file_path.split('/')[-1])
      render_template()
  
  def on_created(self, event):
    file_path = event.src_path.replace('\\', '/')
    if file_path.split('.')[-1] in supported_files:
      print('Created ' + file_path.split('/')[-1])
      render_template()

  def on_deleted(self, event):
    file_path = event.src_path.replace('\\', '/')
    if file_path.split('.')[-1] in supported_files:
      print('Deleted ' + file_path.split('/')[-1])
      render_template()

if __name__ == '__main__':
  os.chdir(sys.path[0])
  template = env.get_template('_index.html')
  render_template()

  event_handler = EventHandler()
  observer = Observer()
  observer.schedule(event_handler, path=sys.path[0] + '/templates', recursive=True)
  observer.start()

  print('Watching for file changes ...')
  try:
    while True:
      time.sleep(1)
  except KeyboardInterrupt:
    print('Stopped watcher')
    observer.stop()
  observer.join()
  
