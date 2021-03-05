deploy-stack-15 deploy-stack-16 deploy-stack-17 deploy-stack-18: deploy-stack-%:
	./commands.sh deploy-stack $*

delete-stack:
	./commands.sh delete-stack

get-ec2-ip:
	./commands.sh get-ec2-ip

get-asg-ec2-public-ip:
	./commands.sh get-asg-ec2-public-ip

deploy-build-stack-01: deploy-build-stack-%:
	./commands.sh deploy-build-stack $*

delete-build-stack:
	./commands.sh delete-build-stack

get-deployment-bucket:
	./commands.sh get-deployment-bucket

app-backend-package:
	./commands.sh app-backend-package

app-backend-upload: app-backend-package
	./commands.sh app-backend-upload

app-lambda-package-init_db: app-lambda-package-%:
	mkdir -p upload
	./commands.sh app-lambda-package $*

app-lambda-upload: app-lambda-package-init_db
	./commands.sh app-lambda-upload
