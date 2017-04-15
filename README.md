# Static Jinja2
A simple wrapper of the powerful [Jinja2](http://jinja.pocoo.org/docs/2.9/) template engine for static sites <br/>
This tool helps you modularize your index page in sub-files, keeping everything cleaner

## Usage
### Basic compilation
Just launch static_jinja2.py and it will watch for file changes in the templates folder and generate the output file <br/>
### Config file
Through the `.config.json` file you can pass arguments to the Jinja2 engine in json format, then from the html 
files simply access them with `data[key]=value` 
### Examples
You can find examples in the [templates](https://github.com/andreatulimiero/static_jinja2/tree/master/templates) folder