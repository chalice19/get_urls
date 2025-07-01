Here is an example of python script that accepts URLs with '-u' option, connects to the websites, reads all links (not including emails/phones/sms) and outputs the result in two ways depending on the '-o' option.

## Usage

```bash
$ ./links.py [-h] -u URL [-o {stdout,json}]
```

For example:

```bash
$ ./links.py -u https://kubernetes.io

https://kubernetes.io/
https://kubernetes.io/docs/
https://kubernetes.io/blog/
https://kubernetes.io/training/
https://kubernetes.io/careers/
https://kubernetes.io/partners/
...

$ ./links.py -u https://kubernetes.io -o json

{
  "https://kubernetes.io": [
    "/",
    "/docs/",
    "/blog/",
    "/training/",
    "/careers/",
    "/partners/",
    ...
  ],
  ...
}
```
