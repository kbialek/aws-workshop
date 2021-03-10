deploy-stack-18 deploy-stack-19 deploy-stack-20 deploy-stack-21: deploy-stack-%:
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

get-logs-bucket:
	./commands.sh get-logs-bucket

app-backend-package:
	./commands.sh app-backend-package

app-backend-upload: app-backend-package
	./commands.sh app-backend-upload

app-lambda-package-init_db: app-lambda-package-%:
	mkdir -p upload
	./commands.sh app-lambda-package $*

app-lambda-upload: app-lambda-package-init_db
	./commands.sh app-lambda-upload

app-frontend-package:
	./commands.sh app-frontend-package

deploy-frontend-stack-01: deploy-frontend-stack-%:
	./commands.sh deploy-frontend-stack $*

get-website-bucket:
	./commands.sh get-website-bucket

get-website-domain-name:
	./commands.sh get-website-domain-name

app-frontend-upload: app-frontend-package
	./commands.sh app-frontend-upload
