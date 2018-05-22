import yaml
import pprint
name='templates/desired.yaml'

f = open(name, 'r'); 

x={}
x.update(yaml.load(f))

pprint.pprint(x)