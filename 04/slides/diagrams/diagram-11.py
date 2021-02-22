from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import InternetGateway, RouteTable, VPCRouter
from diagrams.aws.security import KMS, IAMRole
from diagrams.aws.storage import S3
from diagrams.generic.network import Firewall
from diagrams.onprem.network import Internet

graph_attr = {
    "pad": "0",
    "bgcolor": "transparent"
}

with Diagram("template-11", show=False, direction="LR", filename="diagram-11", graph_attr=graph_attr):
    cw = Cloudwatch("CloudWatch")
    deployment_bucket = S3("DeploymentBucket")

    internet = Internet("Public Internet")

    internet - cw
    internet - deployment_bucket

    internet_gateway = InternetGateway("Igw")

    internet_gateway - internet

    with Cluster("Vpc 10.0.0.0/16"):
        publicRouteTable = RouteTable("PublicRouteTable")
        publicRouteTable >> Edge(label="0.0.0.0/0", style="dashed") >> internet_gateway
        privateRouteTable = RouteTable("PrivateRouteTable")
        with Cluster("AZ1 (eu-central-1a)"):
            with Cluster("PublicSubnet 10.0.0.0/24"):
                publicSubnetRouter = VPCRouter("Router\n10.0.0.1")
                publicSubnetRouter - internet_gateway
                publicSubnetRouter - Edge(style="dashed") - publicRouteTable
                ec2 = EC2("ec2\n10.0.0.x")
                webSg = Firewall("SG: 8080/tcp")
                ec2 - Edge(style="dashed") - publicSubnetRouter
                ec2 - webSg - publicSubnetRouter
            with Cluster("PrivateSubnetA 10.0.8.0/24"):
                privateSubnetARouter = VPCRouter("Router\n10.0.8.1")
                privateSubnetARouter - Edge(style="dashed") - privateRouteTable
                dbPrimary = RDS("Database (Primary)")
                dbPrimary - Edge(style="dashed") - privateSubnetARouter
        with Cluster("AZ2 (eu-central-1b)"):
            with Cluster("PrivateSubnetB 10.0.9.0/24"):
                privateSubnetBRouter = VPCRouter("Router\n10.0.9.1")
                privateSubnetBRouter - Edge(style="dashed") - privateRouteTable
                dbSecondary = RDS("Database (Secondary)")
                dbSecondary - Edge(style="dashed") - privateSubnetBRouter

