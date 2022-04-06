import re

def edit_docker_file(file_loc, service_id, service_type):
    docker_file = open('{}/Dockerfile'.format(file_loc), 'r+')
    docker_template = docker_file.read()

    docker_template = re.sub(r'<service_id>', service_id, docker_template)
    docker_template = re.sub(r'<service_type>', service_type, docker_template)

    docker_file.write(docker_template)
    docker_file.close()