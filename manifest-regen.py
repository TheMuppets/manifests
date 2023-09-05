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

branchName = "lineage-20"

file = open("muppets.xml", "w")
file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
file.write("<manifest>\n")

repos = []

for repo in org.get_repos():
    if (repo.full_name.find("proprietary_vendor") != -1
            and repo.full_name != ("proprietary_vendor_xiaomi")):
        # Only add repos with the correct branch present
        try:
            repo.get_branch(branch=branchName)
            repos.append(repo.full_name)
        except GithubException:
            # Skip the repo, we don't have the branch we want
            continue

for repo in sorted(repos):
    # Repo name is TheMuppets/proprietary_vendor_$vendor_$device
    splits = repo.split("_")
    # Some vendor only repos got a lineage-20 branch early
    if len(splits) < 4:
         continue
    vendor = splits[2]
    device = splits[3]
    # If there are 4 underscores, the device name contains an underscore
    if (len(splits) == 5):
        device += "_" + splits[4]

    file.write("  <project name=\"" + repo + "\" path=\"vendor/" + vendor +
            "/" + device + "\"" + " revision=\"" + branchName + "\"" +
            " clone-depth=\"1\"" + " />\n")

file.write("</manifest>\n")
file.close()
