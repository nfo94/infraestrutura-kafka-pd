u:
	docker compose up --build

ud:
	docker compose up --build -d

d:
	docker compose down --remove-orphans -v

pg:
	docker exec -it postgres /bin/bash
