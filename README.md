# TheMuppets Mirror Manifest

Usage: `repo init -u https://github.com/TheMuppets/manifests -b mirror --mirror`

Once the mirror is synced you can then run `repo init -u /path/to/TheMuppets/mirror/manifests.git -b $BRANCHNAME` and sync normally.

If you want to sync the source quickly but want it to be up-to-date without syncing the mirror every time, then run `repo init -u http://www.github.com/TheMuppets/manifests -b $BRANCHNAME --reference=/path/to/TheMuppets/mirror/`. This will init the new repo and fetch all the (available) data from the mirror, but will fallback to GitHub if something is missing in the mirror.

To update the mirror, either edit the manifest manually or use the `mirror-regen.sh` script.  
**WARNING:** The script causes a data usage of ~15 MB. Also, it is possible that it fails downloading a page of repositories. As a result, these repositories that were on that page will be missing in the mirror manifest. **Please double check the results**
