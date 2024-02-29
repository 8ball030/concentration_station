import json

# Path to the packages.json file
packages_json_path = 'packages/packages.json'

# Open and load the packages.json file
with open(packages_json_path, 'r') as file:
    data = json.load(file)

# Extract third_party packages
third_party_packages = data['third_party']

# Generate and print paths for .gitignore
for package in third_party_packages:
    # Extract the package type (protocol, connection, skill, contract, agent) and name
    package_type, author, package_name, pack = package.split('/')
    # Format the path according to the provided structure
    path = f"packages/{author}/{package_type}s/{package_name}"
    # Print the path for .gitignore
    print(path)

