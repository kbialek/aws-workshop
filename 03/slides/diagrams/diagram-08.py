from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import InternetGateway, RouteTable, VPCRouter
from diagrams.aws.security import KMS, IAMRole
from diagrams.generic.network import Firewall
from diagrams.onprem.network import Internet

graph_attr = {
    "pad": "0",
    "bgcolor": "transparent"
}

with Diagram("template-08", show=False, direction="LR", filename="diagram-08", graph_attr=graph_attr):
    internet = Internet("Public Internet")
    with Cluster("Vpc 10.0.0.0/16"):
        internet_gateway = InternetGateway("Igw")
        internet - internet_gateway
        routeTable = RouteTable("RouteTable")
        routeTable >> Edge(label="0.0.0.0/0", style="dashed") >> internet_gateway
        with Cluster("Subnet 10.0.0.0/24"):
            router = VPCRouter("Router\n10.0.0.1")
            router - Edge(style="dashed") - routeTable
            router - internet_gateway
            ec2 = EC2("ec2\n10.0.0.x")
            ec2 - Edge(style="dashed") - router
            sg = Firewall("SG: 22/tcp")
            ec2 - sg - router
    KMS("KeyPair") - ec2
    ec2Role = IAMRole("Ec2InstanceRole") - ec2

    cw = Cloudwatch("CloudWatch")
    cw - internet
