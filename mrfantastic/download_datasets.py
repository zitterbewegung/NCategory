# download_datasets.py

from torch_geometric.datasets import GeometricShapes, ModelNet, ShapeNet, FAUST
import os

def download_datasets():
    os.makedirs('data', exist_ok=True)

    # Download GeometricShapes
    print("Downloading GeometricShapes...")
    GeometricShapes(root='data/GeometricShapes')

    # Download ModelNet10
    print("Downloading ModelNet10...")
    ModelNet(root='data/ModelNet10', name='10')

    # Download ShapeNet
    print("Downloading ShapeNet...")
    ShapeNet(root='data/ShapeNet', categories=None)  # Download all categories

    # Download FAUST
    print("Downloading FAUST...")
    FAUST(root='data/FAUST')

if __name__ == '__main__':
    download_datasets()
