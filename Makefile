run:
	WORKSPACE=$$(PWD) \
	python -m FreeTAKServer.controllers.services.FTS \
		 -DataPackageIP 0.0.0.0 \
		 -AutoStart True

black:
	black FreeTAKServer

fmt: black
