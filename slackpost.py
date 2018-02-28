import importlib

slackapiExists = importlib.util.find_spec('slacker')
if slackapiExists is not None:
    pass

else:
    print("Can't find 'Slacker' SlackAPI Python module")
