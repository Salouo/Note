import sys
import open3d as o3d
import numpy as np


filename = sys.argv[1]     # Path of the target 3D point cloud object
s = float(sys.argv[2])     # Size of each voxel
pcd = o3d.io.read_point_cloud(filename)  # Load 3D point cloud data

# Visualize the original 3d point cloud data
o3d.visualization.draw_geometries([pcd], zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])
def voxel_down_sample_custom(points, colors, voxel_size):
    # Compute the minimum and maximum bounds of all points
    min_bound = np.min(points, axis=0)

    # Get the voxel indices of each point along the x, y, z directions
    voxel_indices = (points - min_bound) // voxel_size

    # Create two dictionaries to store the voxels and the corresponding colors
    voxel_dict_points = {}
    voxel_dict_colors = {}

    for i, vidx in enumerate(voxel_indices):
        key = (vidx[0], vidx[1], vidx[2])  # Key is a triplet, each representing a voxel
        # If this voxel hasn't been stored in the dictionary yet, create an empty voxel
        if key not in voxel_dict_points:
            voxel_dict_points[key] = []
            # If this voxel doesn't have any color yet, create a color list
            if voxel_dict_colors is not None:
                voxel_dict_colors[key] = []
        # Store the point in the corresponding voxel
        voxel_dict_points[key].append(points[i])
        voxel_dict_colors[key].append(colors[i])

    # Compute the average coordinate values for the points in each voxel (also average the colors)
    # ps: I am not sure whether averaging the colors is the correct operation...
    downsampled_points = []
    downsampled_colors = []
    for key in voxel_dict_points:
        downsampled_points.append(np.mean(voxel_dict_points[key], axis=0))
        downsampled_colors.append(np.mean(voxel_dict_colors[key], axis=0))

    # Convert the results to ndarray format
    downsampled_points = np.array(downsampled_points)
    downsampled_colors = np.array(downsampled_colors)

    # Create a new point cloud object and return the downsampled result
    down_pcd = o3d.geometry.PointCloud()
    down_pcd.points = o3d.utility.Vector3dVector(downsampled_points)
    down_pcd.colors = o3d.utility.Vector3dVector(downsampled_colors)

    return down_pcd


# Convert the 3D point cloud data to ndarray
pcd_points_np = np.array(pcd.points)
pcd_colors_np = np.array(pcd.colors)

# Get the result after downsampling
downpcd = voxel_down_sample_custom(pcd_points_np, pcd_colors_np, 0.03)

# Visualize the result
o3d.visualization.draw_geometries([downpcd], zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])
