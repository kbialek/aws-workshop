from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import InternetGateway, VPCRouter
from diagrams.onprem.network import Internet

graph_attr = {
    "pad": "0",
    "bgcolor": "transparent"
}

with Diagram("template-02", show=False, direction="LR", filename="diagram-02", graph_attr=graph_attr):
    internet = Internet("Public Internet")
    with Cluster("Vpc 10.0.0.0/16"):
        internet - InternetGateway("Igw")
        with Cluster("Subnet 10.0.0.0/24"):
            router = VPCRouter("Router\n10.0.0.1")
            ec2 = EC2("ec2\n10.0.0.x")
            ec2 - Edge(style="dashed") - router
