# generate_test_data.py

import os
import torch
from torch_geometric.datasets import GeometricShapes, ModelNet, ShapeNet, FAUST
import open3d as o3d
import numpy as np

def save_point_cloud(data, filename):
    pos = data.pos.numpy()
    # Create point cloud from positions
    pcd = o3d.geometry.PointCloud()
    pcd.points = o3d.utility.Vector3dVector(pos)
    # Save point cloud to file
    o3d.io.write_point_cloud(filename, pcd)

def generate_test_data():
    output_dir = 'test_data'
    os.makedirs(output_dir, exist_ok=True)

    # Process GeometricShapes
    print("Processing GeometricShapes...")
    geometric_shapes = GeometricShapes(root='data/GeometricShapes')
    os.makedirs(os.path.join(output_dir, 'GeometricShapes'), exist_ok=True)
    for idx, data in enumerate(geometric_shapes):
        filename = os.path.join(output_dir, 'GeometricShapes', f'shape_{idx}.ply')
        save_point_cloud(data, filename)
        print(f'Saved {filename}')
        if idx >= 9:  # Limit to first 10 samples
            break

    # Process ModelNet10
    print("Processing ModelNet10...")
    modelnet10 = ModelNet(root='data/ModelNet10', name='10')
    os.makedirs(os.path.join(output_dir, 'ModelNet10'), exist_ok=True)
    for idx, data in enumerate(modelnet10):
        filename = os.path.join(output_dir, 'ModelNet10', f'shape_{idx}.ply')
        save_point_cloud(data, filename)
        print(f'Saved {filename}')
        if idx >= 9:
            break

    # Process ShapeNet
    print("Processing ShapeNet...")
    shapenet = ShapeNet(root='data/ShapeNet', categories=None)
    os.makedirs(os.path.join(output_dir, 'ShapeNet'), exist_ok=True)
    for idx, data in enumerate(shapenet):
        filename = os.path.join(output_dir, 'ShapeNet', f'shape_{idx}.ply')
        save_point_cloud(data, filename)
        print(f'Saved {filename}')
        if idx >= 9:
            break

    # Process FAUST
    print("Processing FAUST...")
    faust = FAUST(root='data/FAUST')
    os.makedirs(os.path.join(output_dir, 'FAUST'), exist_ok=True)
    for idx, data in enumerate(faust):
        filename = os.path.join(output_dir, 'FAUST', f'shape_{idx}.ply')
        save_point_cloud(data, filename)
        print(f'Saved {filename}')
        if idx >= 9:
            break

if __name__ == '__main__':
    generate_test_data()
