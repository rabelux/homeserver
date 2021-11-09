## HowTo rsync with filter file
For the main backup of the media folder place a file in the root folder of the media hdd:

`nano /mnt/Seagate5T/rsyncRemoteFilter` and insert:

```
+ /Filme/
+ /Serien/
+ /Hör*/
+ /Ratgeber/

H /Serien/Ranma/
H /Serien/Hart of Dixie/
H /Serien/One Tree Hill/
H /Serien/Friends/

- /*
H Thumbs.db

P A Quiet Place/
```

The created file is referenced in the corresponding rsync job.
Example of rsync job: 
`rsync -rtyhik --stats --delete-delay --chmod=ugo=rwx -f=". /mnt/Seagate5T/rsyncRemoteFilter" "/srv/dev-xyz/Medien/" "AS5104T:/share/Medien/"`

Explanation:
- r: recursive
- t: sync mod. times
- y: fuzzy search
- h: human readable
- i: itemize changes
- k: follow symlinks and treat them as the file/directory they point to
- chmod: For the remote side to be able to browse these files chmod to 777
- AS5104T: Alias for the remote ssh target

## HowTo create Alias for SSH:

`nano /etc/ssh/ssh_config` and insert before the `Host *` part:
```
Host AS5104T Synology
   StrictHostKeyChecking no
   User backup
   HostName my.dyndns.privider.com
   HashKnownHosts no
```
*Note: This sets the ssh-user to `backup`. Adapt if necessary.*