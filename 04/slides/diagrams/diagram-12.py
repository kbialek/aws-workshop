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

with Diagram("template-12", show=False, direction="TB", filename="diagram-12", graph_attr=graph_attr):
    with Cluster("Vpc 10.0.0.0/16"):
        webSg = Firewall("SG in 8080/tcp")

        with Cluster("AZ1 (eu-central-1a)"):
            with Cluster("PublicSubnet 10.0.0.0/24"):
                publicSubnetRouter = VPCRouter("Router\n10.0.0.1")
                ec2 = EC2("ec2\n10.0.0.x")
                ec2 - Edge(style="dashed") - publicSubnetRouter
                ec2 - webSg - publicSubnetRouter
            with Cluster("PrivateSubnetA 10.0.8.0/24"):
                privateSubnetARouter = VPCRouter("Router\n10.0.8.1")
                dbPrimary = RDS("Database (Primary)")
                dbPrimary - Edge(style="dashed") - privateSubnetARouter

        dbClientSg = Firewall("SG out 3306/tcp")
        dbServerSg = Firewall("SG in 3306/tcp")

        with Cluster("AZ2 (eu-central-1b)"):
            with Cluster("PrivateSubnetB 10.0.9.0/24"):
                privateSubnetBRouter = VPCRouter("Router\n10.0.9.1")
                dbSecondary = RDS("Database (Secondary)")
                dbSecondary - Edge(style="dashed") - privateSubnetBRouter

        dbServerSg >> dbClientSg
        ec2 - dbClientSg
        dbPrimary - dbServerSg
        dbSecondary - dbServerSg
