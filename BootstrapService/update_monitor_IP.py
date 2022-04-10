import re

TEMPLATE_PATH = "./BootstrapService/Template_Dockerfile.txt"

def generate_env_string(env_file_path):
    try:
        env_file = open(env_file_path, 'r')
        env_lines = env_file.readlines()
        if len(env_lines) == 0:
            raise Exception("No lines present in env file")
        env_str = "ENV "
        for line in env_lines:
            env_str = env_str + " \   \n" + line.strip() 
        env_file.close()
        return env_str
    except Exception as e:
        return ""

def create_docker_file(destination_folder_path, monitor_ip, entry_point_py_file_name):
    """Creating docker file in root folder"""

    docker_file = open(TEMPLATE_PATH, 'r')
    docker_template = docker_file.read()

    # erase existing content
    open(destination_folder_path+'/Dockerfile', 'w').close()

    # open file again and write
    new_docker_file = open(destination_folder_path+'/Dockerfile', 'w')

    docker_template = re.sub(r'<monitor_ip>', monitor_ip, docker_template)
    # docker_template = re.sub(r'<source_folder>', destination_folder_path, docker_template)
    
    env_str = generate_env_string(".env")
    if env_str == "":
        return "Error: .env file not found in "+destination_folder_path
    docker_template = re.sub(r'<env_vars>', env_str, docker_template)
    docker_template = re.sub(
        r'<entry_point>', entry_point_py_file_name, docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return "Done"

if __name__ == "__main__":
    create_docker_file(".", "10.2.136.88", "demo.py")