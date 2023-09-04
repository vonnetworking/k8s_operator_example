SERVER_IP=$(shell ifconfig en0 | grep inet | awk '{print $$2}')

hello:
	echo "hi!"

minikube_start: 
	#minikube start
	#TODO need to make the ip dynamic
	minikube start --apiserver-ips=192.168.50.200 
	#kube/config updated to have minikube pointing to accessible IP - defaults to 127.0.0.1
	sed -i".bak2" 's/127.0.0.1/$(SERVER_IP)/g' ~/.kube/config

argocd_setup:
	kubectl create namespace argocd || true
	kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
	brew install argocd
	echo "login with 'argocd login $(SERVER_IP):8881'"
	scripts/argo_start_port_fwd.sh
	scripts/argo_login_and_add_minikube.sh

kopf_setup:
	pip install kopf
	kubectl apply -f https://github.com/nolar/kopf/raw/main/peering.yaml || true
	sleep 10
	kubectl apply -f https://github.com/nolar/kopf/raw/main/peering.yaml
	kopf run --help
	scripts/kopf_install_crds.sh

destroy_dev_env:
	minikube delete

create_dev_env: minikube_start argocd_setup kopf_setup