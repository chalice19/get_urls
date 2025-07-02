In this part several steps are done:

## docker
 I have added a Dockerfile to creat an image with our script

``` bash
$ docker buildx build ./ -t read_links
[+] Building 3.7s (11/11) FINISHED                                                                                                                                             docker:default
 => [internal] load build definition from Dockerfile                                                                                                                                     0.1s
 => => transferring dockerfile: 248B                                                                                                                                                     0.0s
 => [internal] load metadata for docker.io/library/python:3.12-alpine                                                                                                                    1.1s
 => [internal] load .dockerignore                                                                                                                                                        0.1s
 => => transferring context: 2B                                                                                                                                                          0.0s
 => [1/6] FROM docker.io/library/python:3.12-alpine@sha256:c610e4a94a0e8b888b4b225bfc0e6b59dee607b1e61fb63ff3926083ff617216                                                              0.0s
 => [internal] load build context                                                                                                                                                        0.1s
 => => transferring context: 1.93kB                                                                                                                                                      0.0s
 => CACHED [2/6] WORKDIR /usr/local/app                                                                                                                                                  0.0s
 => CACHED [3/6] COPY requirements.txt ./                                                                                                                                                0.0s
 => CACHED [4/6] RUN pip3 install --no-cache-dir -r requirements.txt                                                                                                                     0.0s
 => [5/6] COPY links.py ./                                                                                                                                                               0.6s
 => [6/6] RUN adduser -S app                                                                                                                                                             0.7s
 => exporting to image                                                                                                                                                                   0.6s
 => => exporting layers                                                                                                                                                                  0.5s
 => => writing image sha256:d5388aa874c85fdd346cbf0aeae83370515bd116b7c4060a70f24e9d1c80f5bc                                                                                             0.0s
 => => naming to docker.io/library/read_links                                                                                                                                            0.0s
```

``` bash
$ docker run -t read_links -u https://google.com
https://www.google.com/imghp?hl=fr&tab=wi
https://www.google.com/setprefdomain?prefdom=FR&prev=https://www.google.fr/&sig=K_D8jtb1RtLMMXAZOlbSXqanPxwJY%3D
https://maps.google.fr/maps?hl=fr&tab=wl
https://play.google.com/?hl=fr&tab=w8
...
```

### Security check

I have cheked my image with the tool [trivy](https://github.com/aquasecurity/trivy).
First, my image was using `python:3.12-slim`, and the check showed:

```
read_links (debian 12.11)

Total: 101 (UNKNOWN: 1, LOW: 74, MEDIUM: 18, HIGH: 7, CRITICAL: 1)
```
With the critical vulnerability found in the `zlib1g` library.

Vulnerability: CVE-2023-45853 | Status: will_not_fix │ Installed Version: 1:1.2.13.dfsg-1 | [zlib: integer overflow and resultant heap-based buffer overflow in zipOpenNewFileInZip4_6...](https://avd.aquasec.com/nvd/cve-2023-45853)
 
After I switched to the python:3.12-alpine (alpine 3.22.0), trivy check showed no problems, vulnerabilities were not found.

## kubernetes

Our script is a one-off tasks that run to completion and then stop. This sounds like a perfect opportunity to use the Job of kubernetes to run our task and stop the pod once execution is finished. I decided this is a more suitable solution than adding an infinite sleep to the script. After launching the cluster, we can execute the job:
``` bash
$ kubectl apply -f k8s_job.yaml
```

Then we can find the pod that executed the job and find it's output in the logs [like shown here](https://kubernetes.io/docs/concepts/workloads/controllers/job/)

### improvements:

* **args**: with the current implementation we cannot really pass the arguments with URLs. A better solution would be to set them in the ConfigMap object for pods to read the URL from it. I would state one URL argument per job and execute several seperate jobs for several input URLs
* **image**: to be able to use the image we built, it needs to be uploaded to a registry
* **results**: we might want to implement the automated collection of results since they will be spreaded among different logs
