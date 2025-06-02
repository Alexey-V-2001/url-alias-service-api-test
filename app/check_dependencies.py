import subprocess
import sys
import pkg_resources

# Parse requirements.txt and return list of requirements
# Each line is a requirement string, e.g. 'package>=1.0' or 'module[extra]==2.0'
def parse_requirements(filename):
    requirements = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                requirements.append(line)
    return requirements

# Check if a requirement is already satisfied
# Uses pkg_resources.require to verify version and extras
def is_requirement_satisfied(requirement):
    try:
        pkg_resources.require(requirement)
        return True
    except (pkg_resources.DistributionNotFound, pkg_resources.VersionConflict):
        return False

# Install a package via pip using subprocess
def install_package(package):
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])

def main():
    requirements = parse_requirements('requirements.txt')

    print("Checking dependencies...")

    for req in requirements:
        if not is_requirement_satisfied(req):
            print(f'Installing {req}...')
            install_package(req)

    print("All dependencies are installed")

if __name__ == '__main__':
    main()
