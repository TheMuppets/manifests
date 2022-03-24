#!/usr/bin/python3

import os
import sys
try:
    from github import Github
    from github import GithubException
except ImportError:
    print("Please install the pygithub package via pip3")
    exit(1)
e = os.environ.copy()
# Environment variables for github username and api token
try:
    u = e["GHUSER"]
    p = e["GHTOKEN"]
except KeyError:
    print("Please set the GHUSER and GHTOKEN environment variables")
    exit(1)

orgName = "TheMuppets"
org = Github(u, p).get_user(orgName)

file = open("muppets.xml", "w")
file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
file.write("<manifest>\n")

repos = []

for repo in org.get_repos():
    if (repo.full_name.find("proprietary_vendor") != -1
            and repo.full_name.find("proprietary_vendor_xiaomi") == -1):
        # Only add repos with the correct branch present
        try:
            repo.get_branch(branch="lineage-18.1")
            repos.append(repo.full_name)
        except GithubException:
            # Skip the repo, we don't have the branch we want
            continue

for repo in sorted(repos):
    # Repo name is TheMuppets/proprietary_vendor_$vendor
    # split on "_" and grab the last one
    vendor = repo.split("_")[-1]
    file.write("  <project name=\"" + repo + "\" path=\"vendor/" + vendor +
            "\" />\n")

file.write("</manifest>\n")
file.close()
