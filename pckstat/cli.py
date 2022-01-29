import click
import requests
import gzip
import re


def file_parsed(data: str) -> list:
    data = data.split('\n')
    rejected = False

    # List of common linux directories in /
    linux_dir_list = ['bin', 'boot', 'dev', 'etc', 'home', 'lib', 'lib64', 'media', 'mnt', 'opt', 'proc', 'root', 'run',
                      'sbin', 'srv', 'sys', 'tmp', 'usr', 'var']
    parsed_data = {}
    for raw in data:
        # Remove whitespaces from right side of raw and split by last whitespace
        splited_raw = raw.rstrip().rsplit(' ', 1)
        if len(splited_raw) != 2:
            continue

        # remove whitespaces from each column and tabulations
        # splited_raw = [column.replace(" ","") for column in splited_raw]
        splited_raw = [re.sub('(\s+)', '', column) for column in splited_raw]

        # check if FILE and LOCATION in raw
        if splited_raw[0] == 'FILE' and splited_raw[1] == "LOCATION":
            if not rejected:
                rejected = True
                # Clear table
                parsed_data = {}
                # Go to next element with clear result table
                continue

        # try catch here if no '/' char in splited_raw[0]
        # check, that the first column does not start from "/" and that name of dir is one of common linux dir
        if re.search(r'[^/]*', splited_raw[0]).group() not in linux_dir_list:  # zaczem tut
            continue

        # split package if specified by ',' ex.debian-installer/partman-auto-crypto,debian-installer/partman-auto-raid
        splited_raw[1] = splited_raw[1].split(",")
        # check if package structure correponds to [[$AREA/]$SECTION/]$NAME
        # if not any([re.match("^([^/]+/)?([^/]+/)?[^/]+$", package) for package in splited_second_column]):
        # print(any([re.match("^([^/]+/)?([^/]+/)[^/]+$", package) for package in splited_second_column]))
        if not any([re.match("^([^/]+/)?([^/]+/)[^/]+$", package) for package in splited_raw[1]]):
            continue

        for package in splited_raw[1]:
            if package in parsed_data:
                parsed_data[package] += 1
            else:
                parsed_data[package] = 1
                # result.append(splited_raw)
    parsed_data = sorted(parsed_data.items(), reverse=True, key=lambda item: item[1])

    return parsed_data


@click.command()
@click.argument('architecture')
def pckstat(architecture):
    """Print parsed repository"""
    response = requests.get('http://ftp.uk.debian.org/debian/dists/stable/main/Contents-' + architecture + '.gz')
    response.raise_for_status()
    data = gzip.decompress(response.content).decode("utf-8")

    for package, number in file_parsed(data)[:10]:
        print("%s   %s" % (package, number))

