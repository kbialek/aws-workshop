from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPCRouter
from diagrams.onprem.network import Internet

graph_attr = {
    "pad": "0",
    "bgcolor": "transparent"
}

with Diagram("template-01", show=False, direction="LR", filename="diagram-01", graph_attr=graph_attr):
    Internet("Public Internet")
    with Cluster("Vpc 10.0.0.0/16"):
        with Cluster("Subnet 10.0.0.0/24"):
            router = VPCRouter("Router\n10.0.0.1")
            ec2 = EC2("ec2\n10.0.0.x")
            ec2 - Edge(style="dashed") -  router

