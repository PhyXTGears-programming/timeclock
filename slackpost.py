import importlib

slackapiExists = importlib.util.find_spec('slacker')
if slackapiExists is not None:

else:
	print("Can't find SlackAPI python module")