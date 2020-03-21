dev-db:
	@gcloud beta emulators firestore start --host-port localhost:8888

dev-server:
	@FIRESTORE_EMULATOR_HOST=127.0.0.1:8888 \
		FLASK_DEBUG=true FLASK_APP=./api.py flask run

server:
	@FLASK_APP=./multitude/api.py flask run
