"""Generate python requirements for the flatpak from a requirements.txt file."""

#!/usr/bin/env python3
import argparse
import json
import os
import re
import urllib.request


def join_continued_lines(text):
    """
    Replace backslash-newline sequences with a space so that
    multi-line requirements become one logical line.
    """
    return re.sub(r"\\\s*\n\s*", " ", text)


def parse_requirements(text):
    """
    Parse a requirements.txt file into a list of package dictionaries.
    Each dictionary contains:
      - name: package name (as specified in the requirements file)
      - version: package version (as a string)
      - hashes: list of sha256 hash strings (without the "sha256:" prefix)
    """
    packages = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue

        # Split the line at the first occurrence of "--hash="
        parts = line.split(" --hash=")
        main_part = parts[0].strip()
        # Remove any environment marker (everything after a ';')
        req_spec = main_part.split(";")[0].strip()

        if "==" in req_spec:
            name, version = req_spec.split("==", 1)
            name = name.strip()
            version = version.strip()
        else:
            name = req_spec.strip()
            version = ""

        # Process each hash token (if present) and remove the "sha256:" prefix.
        hashes = []
        for hash_part in parts[1:]:
            token = hash_part.split()[0].strip()
            if token.startswith("sha256:"):
                token = token[len("sha256:") :]
            hashes.append(token)

        packages.append({"name": name, "version": version, "hashes": hashes})
    return packages


def clean_package_name(name: str) -> str:
    """
    Remove extras from a package name.
    E.g., "uvicorn[standard]" becomes "uvicorn".
    """
    if "[" in name:
        return name.split("[")[0].strip()
    return name


def get_pypi_source(name: str, version: str, hashes: list) -> tuple:
    """
    Get the source information for a dependency by querying PyPI.

    Args:
        name (str): The package name (may include extras).
        version (str): The package version.
        hashes (list): The list of sha256 hashes (without "sha256:" prefix)
                       provided in the requirements file.

    Returns:
        tuple: (url, sha256) where url is the download URL and sha256 is the
               matching hash.

    Raises:
        Exception: if no matching release source is found.
    """
    # Remove extras before querying PyPI
    cleaned_name = clean_package_name(name)
    pypi_url = f"https://pypi.org/pypi/{cleaned_name}/json"
    print(f"Extracting download url and hash for {name}, version {version}")

    with urllib.request.urlopen(pypi_url) as response:
        body = json.loads(response.read().decode("utf-8"))
        releases = body.get("releases", {})
        if version not in releases:
            raise Exception(
                f"Version {version} not found for package {name} (cleaned as {cleaned_name})"
            )
        source_list = releases[version]
        # First, try to find a wheel (bdist_wheel) that supports py3.
        for source in source_list:
            if (
                source.get("packagetype") == "bdist_wheel"
                and "py3" in source.get("python_version", "")
                and source["digests"]["sha256"] in hashes
            ):
                return source["url"], source["digests"]["sha256"]
        # Fall back to sdist if no suitable wheel is found.
        for source in source_list:
            if (
                source.get("packagetype") == "sdist"
                and "source" in source.get("python_version", "")
                and source["digests"]["sha256"] in hashes
            ):
                return source["url"], source["digests"]["sha256"]

    raise Exception(f"Failed to extract url and hash from {pypi_url}")


def make_build_command(package_names):
    """
    Build a pip install command using the package names from requirements.txt.
    Note: the command uses the names as given (including extras) so that
    pip can install the extra features if required.
    """
    base = (
        'pip3 install --no-index --find-links="file://${PWD}" --prefix=${FLATPAK_DEST}'
    )
    return f'{base} {" ".join(package_names)}'


def main():
    parser = argparse.ArgumentParser(
        description="Convert a requirements.txt file into a JSON file with PyPI sources."
    )
    parser.add_argument("requirements", help="Path to requirements.txt")
    parser.add_argument(
        "-o",
        "--output",
        default="python-requirements.json",
        help="Output JSON file name (default: python-requirements.json)",
    )
    args = parser.parse_args()

    if not os.path.exists(args.requirements):
        print(f"Error: File {args.requirements} does not exist.")
        exit(1)

    with open(args.requirements, "r") as f:
        raw_text = f.read()

    joined_text = join_continued_lines(raw_text)
    parsed_packages = parse_requirements(joined_text)

    # Build the sources list by querying PyPI for each package.
    sources = []
    for pkg in parsed_packages:
        try:
            url, sha256 = get_pypi_source(pkg["name"], pkg["version"], pkg["hashes"])
            sources.append({"type": "file", "url": url, "sha256": sha256})
        except Exception as e:
            print(f"Error processing {pkg['name']}=={pkg['version']}: {e}")
            exit(1)

    # Use the original package names (including extras) for the build command.
    pkg_names = [pkg["name"] for pkg in parsed_packages]
    build_command = make_build_command(pkg_names)

    output_json = {
        "name": "poetry-deps",
        "buildsystem": "simple",
        "build-commands": [build_command],
        "sources": sources,
    }

    with open(args.output, "w") as outf:
        json.dump(output_json, outf, indent=4)
    print(f"JSON file written to {args.output}")


if __name__ == "__main__":
    main()
