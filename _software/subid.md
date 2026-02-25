---
layout: software3
title: "Subid: Sub-Identity Toolkit"
show_title: true
description: "The Cooperative Computing Laboratory Sub-Identity Toolkit is a set of utilities and a Pluggable Authentication Module that provides users with the ability to create sub-users of themselves."
long_description: "The Cooperative Computing Laboratory Sub-Identity Toolkit is a set of utilities and a Pluggable Authentication Module that provides users with the ability to create sub-users of themselves. Standard Unix permissions checks prevent these subordinate users from accessing their parent user's files."
carousel: false
order: 9
skip_list: true
category: tools
publication_keywords:
  - subid
links:
  - name: User Manual
    url: https://ccl.cse.nd.edu/software/manuals/subid.html
---

### Synopsis

The Cooperative Computing Laboratory Sub-Identity Toolkit is a set of utilities and a Pluggable Authentication Module that provides users with the ability to create sub-users of themselves. Standard Unix permissions checks prevent these subordinate users from accessing their parent user's files.

The Toolkit comes packaged with a set of five utilities and a pluggable authentication module, `pam_subid.so`. The utilities and their purposes are as follows:

- **subuseradd** creates a named subuser of the calling user.
- **subuserdel** deletes a named subuser of the calling user, optionally deleting all files owned by the subuser.
- **subusersu** acts like 'su', invoking the identity of the named subuser.
- **subusersudo** acts like 'sudo', running a given command as the named subuser.
- **subuserchown** acts like 'chown', changing the ownership of the given files to the named subuser (or to the calling user).

The pluggable authentication module, `pam_subid.so`, allows various programs and services (such as 'su') to check whether the named user is a subuser of the calling user, and implicitly allow such actions. So, if there is a line in `/etc/pam.d/su` saying `auth sufficient pam_subid.so`, then if alice has a sub-user bob, then alice can '`su bob`' without having to enter a password. The module is, however, somewhat incomplete, and suggestions/patches are quite welcome.

### Documentation

- [subuseradd(1) .html](subuseradd.1.html) [.ps](subuseradd.1.ps) [.pdf](subuseradd.1.pdf)
- [subuserdel(1) .html](subuserdel.1.html) [.ps](subuserdel.1.ps) [.pdf](subuserdel.1.pdf)
- [subusersu(1) .html](subusersu.1.html) [.ps](subusersu.1.ps) [.pdf](subusersu.1.pdf)
- [subusersudo(1) .html](subusersudo.1.html) [.ps](subusersudo.1.ps) [.pdf](subusersudo.1.pdf)
- [subuserchown(1) .html](subuserchown.1.html) [.ps](subuserchown.1.ps) [.pdf](subuserchown.1.pdf)
- [subusers(5) .html](subusers.5.html) [.ps](subusers.5.ps) [.pdf](subusers.5.pdf) \- a description of the file format of `/etc/subusers`
- [subusers(7) .html](subusers.7.html) [.ps](subusers.7.ps) [.pdf](subusers.7.pdf) \- an overview of the subuser toolkit

### Downloads

The latest release can be downloaded from here: [subid-current.tgz](subid-current.tgz).
