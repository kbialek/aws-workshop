.SILENT: deploy-stack-01 deploy-stack-02 deploy-stack-03 deploy-stack-04 delete-stack get-ec2-ip

deploy-stack-01 deploy-stack-02 deploy-stack-03 deploy-stack-04: deploy-stack-%:
	./commands.sh deploy-stack $*

delete-stack:
	./commands.sh delete-stack

get-ec2-ip:
	./commands.sh get-ec2-ip
