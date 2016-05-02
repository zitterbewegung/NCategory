import subprocess, tempfile 

def pcd_to_vfh_histogram(inputFileName, outputFileName):
    """
    
    """
    args = ['pcl_extract_feature', inputFileName, outputFileName, '-feature', 'VFHEstimation', '-n_k', '1', '-f_k', '1']
    p = subprocess.call(args)
    

def convert_obj_pcd(inputFileName, outputFileName):
    with tempfile.NamedTemporaryFile(suffix='.pcd') as tf:
        args = ['pcl_obj2pcd', inputFileName, tf.name]
        tf.flush()
        p = subprocess.call(args)
        convert_args = ['pcl_convert_pcd_ascii_binary', tf.name, outputFileName, '0']
        p2 = subprocess.call(convert_args)
        tf.flush()
def train_model(directory):
    """Trains a model using knearestneighbors"""
    args_build_tree = ['./build/build_tree', '~/datasets/GroundTruthDatabase/']
    p = subprocess.call(args)

def query_model(queryFile):
        pass