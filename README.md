Here is an example of python script that accepts URLs with '-u' option, connects to the websites, reads all links (not including emails/phones/sms) and outputs the result in two ways depending on the '-o' option.

Two solutions provided: [syncronious](https://github.com/chalice19/get_urls/commit/ceec573c86c02c628f479b26b6ab7d08a93234b9) and [asyncronious](https://github.com/chalice19/get_urls/commit/d006b7947fef802fbe5d1071a8b9a563df0d77b4)

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
