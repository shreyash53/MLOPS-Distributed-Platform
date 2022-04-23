import re

def edit_docker_file(file_loc, service_id, service_type, monitor_ip, monitor_port):
    docker_file = open('{}/Dockerfile'.format(file_loc), 'r')
    docker_template = docker_file.read()
    docker_file.close()
    docker_file = open('{}/Dockerfile'.format(file_loc), 'w')

    docker_template = re.sub(r'<service_id>', service_id, docker_template)
    docker_template = re.sub(r'<service_type>', service_type, docker_template)
    docker_template = re.sub(r'<monitor_ip>', monitor_ip, docker_template)
    docker_template = re.sub(r'<monitor_port>', monitor_port, docker_template)

    docker_file.write(docker_template)
    docker_file.close()