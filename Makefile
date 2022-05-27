build:
	docker build -t redbirddigital/seaside-api -f docker/Dockerfile .

deploy: build
	docker push redbirddigital/seaside-api
	sleep 10
	kubectl rollout restart deployment -n seasidefm seaside-api
