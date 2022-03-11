build:
	docker buildx build --platform linux/arm64 --push -t registry.dougflynn.dev/seaside-api -f docker/Dockerfile .

deploy: build
	sleep 10
	kubectl rollout restart deployment -n seasidefm seaside-api