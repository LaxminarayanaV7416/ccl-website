---
layout: software3
title: ftsh - The Fault Tolerant Shell
show_title: true
description: Description goes here.
long_description: "Description goes here."
carousel: false
order: 9
skip_list: true
category: tools
# publication_keywords:
#   - ftsh
# links:
#   - name: User Manual
#     url: https://ccl.cse.nd.edu/software/manuals/ftsh.html
---

The Fault-Tolerant Shell (ftsh) is a small language for system integration that makes failures a first class concept. Ftsh aims to combine the ease of scripting with very precise error semantics. It is especially useful in building distributed systems, where failures are common, making timeouts, retry, and alternation necessary techniques. For example:

```
    try for 30 minutes
         cd /tmp
         rm -f data
         forany host in xxx yyy zzz
               wget http://${host}/fresh.data data
         end
    end
```

If any element of the script fails, all running process trees are reliably cleaned up, and the block is tried again with an exponential backoff. You might think of this as exception handling for scripts. To learn more, please read the technical manual, or a more [philosophical paper](/assets/pdf/ethernet-hpdc12.pdf).

## News Items

- ftsh started an interesting discussion on [Slashdot](http://developers.slashdot.org/article.pl?sid=04/03/15/0051221)
- ftsh is distributed with the [Virtual Data Toolkit](http://www.lsc-group.phys.uwm.edu/vdt/)
- ftsh is available on [Sun Freeware](http://www.sunfreeware.com)
