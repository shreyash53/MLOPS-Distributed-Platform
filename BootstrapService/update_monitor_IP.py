import re

TEMPLATE_PATH = "./BootstrapService/Template_Dockerfile.txt"


def create_docker(destination_path, monitor_ip, entry_point_py_file_name):

    docker_file = open(TEMPLATE_PATH, 'r')
    docker_template = docker_file.read()

    # erase existing content
    open(destination_path+"/"+'Dockerfile', 'w').close()

    # open file again and write
    new_docker_file = open(destination_path+"/"+'Dockerfile', 'w')

    docker_template = re.sub(r'<monitor_ip>', monitor_ip, docker_template)
    docker_template = re.sub(
        r'<entry_point>', entry_point_py_file_name, docker_template)
    new_docker_file.write(docker_template)
    new_docker_file.close()
    docker_file.close()
    return "Done"

if __name__ == "__main__":
    create_docker(".", "10.2.136.88", "demo.py")