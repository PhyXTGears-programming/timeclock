from imp import reload

import Service_Handler

while True:
	Service_Handler.main()
	reload(Service_Handler)
