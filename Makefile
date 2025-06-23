NAMESPACE := craftsman
build_env := /tmp/crafter.build.env
registry := registry.internal:80

.PHONY: up down reload status build ns logs init

build:
	@echo "API_VERSION=$(shell jq '.API_VERSION' versions.json | tr -d '"')" > ${build_env}
	@echo "APP_VERSION=$(shell jq '.APP_VERSION' versions.json | tr -d '"')" >> ${build_env}
	docker-compose --env-file=$(build_env) build
	docker tag craftsman:$(shell jq '.API_VERSION' versions.json | tr -d '"') $(registry)/craftsman:$(shell jq '.API_VERSION' versions.json | tr -d '"')
	docker push $(registry)/craftsman:$(shell jq '.API_VERSION' versions.json | tr -d '"')
	@rm ${build_env}

ns:
	kubens $(NAMESPACE) 

up: ns
	kubectl apply -f k8s/

down:
	kubectl delete -f k8s/ --wait

reload: down up

status:
	kubectl get pods -o wide
	kubectl get services -o wide
	kubectl get ingresses -o wide

logs:
	kubectl logs craftsman

init: build ns up

exec:
	kubectl exec -it craftsman -- bash
