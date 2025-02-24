import docker
import json

# Initialize the Docker client
client = docker.from_env()

# Pull an image (e.g., the official Nginx image)
image_name = "nginx"

# Pull the image from Docker registry
image = client.images.pull(image_name)

# Get the short image ID (first 12 characters of the full image ID)
short_image_id = image.id[:12]  # Slice to get the first 12 characters of the SHA256 hash

print(f"Short Image ID: {short_image_id}")



# Your image ID (provided)
image_id = image_name

# Run the container using the image ID and list installed packages with dpkg-query
container = client.containers.run(
    image_id,  # Use the image ID
    "dpkg-query -W -f='${Package} ${Version} ${Architecture}\n'",  # Get package name, version, and architecture
    detach=True  # Run the container in the background
)

# Get the container object by ID
container = client.containers.get(container.id)

# Wait for the container to finish and get the logs (output)
output = container.logs()

# Decode the output to string
output_str = output.decode("utf-8")

# Split the output into lines
lines = output_str.splitlines()

# Initialize a list to hold package data
packages = []

# Process each line and create a dictionary with name, version, and architecture
for line in lines:
    parts = line.split()
    if len(parts) == 3:
        package = {
            "name": parts[0],
            "version": parts[1],
            "architecture": parts[2]
        }
        packages.append(package)

# Convert the list of packages to JSON format
installed_packages_json = json.dumps(packages, indent=4)

# Save the output to a JSON file
with open("file.json", "w") as json_file:
    json_file.write(installed_packages_json)

# Optionally, remove the container after execution
container.remove()

# Remove the image after usage
client.images.remove(image.id)  # Removes the image using its full image ID

print(f"Image with ID {short_image_id} has been removed.")

# Let the user know the file has been saved
print("Package list saved to file.json")
