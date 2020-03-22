dev-db:
	@gcloud beta emulators firestore start --host-port localhost:8888

dev-server:
	@FIRESTORE_EMULATOR_HOST=127.0.0.1:8888 \
		PYTHONPATH=multitude uvicorn api:app --reload

server:
	@PYTHONPATH=multitude uvicorn api:app
