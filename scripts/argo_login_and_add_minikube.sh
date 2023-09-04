export ARGO_PASSWORD=$(argocd admin initial-password -n argocd | head -1) 

argocd login 127.0.0.1:8881 --insecure --username admin --password ${ARGO_PASSWORD}

argocd cluster add minikube --cluster-endpoint=kubeconfig --yes