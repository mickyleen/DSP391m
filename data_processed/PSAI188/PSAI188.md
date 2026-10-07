# **Improve tooling, integrations, and testing infrastructure of Zulip**

Proposal: Google Summer of Code 2021

![](images/_page_0_Picture_2.jpeg)


| Personal Details       | 2  |
|------------------------|----|
| About me               | 2  |
| Previous contributions | 2  |
| Proposal               | 4  |
| Abstract               | 4  |
| Project details        | 4  |
| Proposed Timeline      | 9  |
| Personal projects      | 10 |
| Why Zulip and why me?  | 11 |
| Availability           | 11 |
| Post GSoC              | 11 |

# <span id="page-1-0"></span>**Personal Details**

### <span id="page-1-1"></span>**About me**

Name: Ganesh Pawar

Email: [pawarg256@gmail.com](mailto:pawarg256@gmail.com)

Github: [ganpa3](https://github.com/ganpa3)

Username on [chat.zulip.org:](http://chat.zulip.org) Ganesh Pawar (ganpa3)

Timezone: Indian Standard Time Zone (GMT+5:30)

## <span id="page-1-2"></span>**Previous contributions**

### **Code contributions**

[A list of merged PRs](https://github.com/zulip/zulip/pulls?q=is%3Amerged+is%3Apr+author%3Aganpa3+)

[A list of open PRs](https://github.com/zulip/zulip/pulls/ganpa3)

[A list of commits made by me](https://github.com/zulip/zulip/commits?author=ganpa3)

#### **Merged PRs:**

| PR Number | Description                                                    |
|-----------|----------------------------------------------------------------|
| #Z21      | minor: Change encoding to UTF-8 in `open()` calls.             |
| #P652     | Fix tests failing on Windows.                                  |
| #P662     | ci: Setup Github Actions for Windows.                          |
| #16976    | custom_emojis: Fix unresponsiveness after submitting without a |
| #16978    | run-dev: Suppress the notices by third-party tools.            |
| #17076    | circleci: Resolve node installation error in CircleCI          |
| #17122    | ui_report: Add ui_report.client_error.                         |
| #17123    | populate_db: Implement pictures.                               |
| #17161    | composebox: Add typeahead for /todo.                           |

| #17170 | provision: Add provision support for Ubuntu 20.10(Groovy).         |
|--------|--------------------------------------------------------------------|
| #17343 | stream-ui: Fix oddly spaced elements in streams tab.               |
| #17545 | minor: Check if typeahead query exists.                            |
| #17719 | provision: Add support for Fedora 33.                              |
| #17974 | hotkey: Fix Ctrl+C not working when recent topics view is visible. |
| #17992 | hotkey: Map numpad navigation keys to close compose when empty.    |

#### **Open PRs:**

| PR Number | Description                                                          |
|-----------|----------------------------------------------------------------------|
| #1074     | ci: Migrate Windows CI from Appveyor to Github Actions.              |
| #17066    | streams: Split stream creation option in org settings.               |
| #17166    | widgets: Prevent edits to widgets.                                   |
| #17299    | settings_ui: Avoid hiding user deactivation modal.                   |
| #17551    | integration: Add wekan integration.                                  |
| #17690    | upload: Refactor and add tests for ensure_avatar_image in upload.py. |

### **Issues filed**

#### [A list of issues created by me in zulip/zulip](https://github.com/zulip/zulip/issues?q=is%3Aissue+author%3Aganpa3+)

[A list of issues created by me in zulip/zulip-mobile](https://github.com/zulip/zulip-mobile/issues?q=is%3Aissue+author%3Aganpa3+)

| Issue Number | Description                                                     |
|--------------|-----------------------------------------------------------------|
| #4359        | Unread messages includes messages from muted streams            |
| #17190       | Can't close message edit form after internet connection is lost |
| #17297       | Deactivation user modal flickers when trying to deactivate      |

### **PRs reviewed**

[A list of PRs reviewed by me](https://github.com/zulip/zulip/pulls?q=is%3Apr+reviewed-by%3Aganpa3+-author%3Aganpa3)

| PR Number | Description                               |
|-----------|-------------------------------------------|
| #16796    | todo_widget: Add task creation shorthand. |
| #17098    | Vagrant hyperv                            |
| #17735    | non-Vagrant environment docs updated      |

# <span id="page-3-0"></span>**Proposal**

### <span id="page-3-1"></span>**Abstract**

My goal during this GSoC will be improving the tooling and testing infrastructure, thereby increasing developer productivity a lot. I will also focus on adding interesting integrations to Zulip and improving support for more platforms. All this will likely result in many follow-up projects. I will make sure to allocate sufficient time to them.

### <span id="page-3-2"></span>**Project details**

#### **1. Improve and stabilize support for Red Hat based Linux distributions**

Red Hat is the most used enterprise Linux distribution. Currently, Zulip has experimental support for Reh Hat and friends. My goal would be to improve support for it.

In [#17719](https://github.com/zulip/zulip/pull/17719), I added support for Fedora 33 and noticed some bugs with the current implementation. This could have been avoided if we had a CI setup for the same.

Along with adding support, I will also be working on setting up CI to test installation and run backend tests for Red Hat based distributions.

Red Hat provides free OCI-compliant [Universal Base](https://www.redhat.com/en/blog/introducing-red-hat-universal-base-image) Images. We could either use these or Fedora docker images for CI set up.

#### **2. Improve and fix bugs of populate\_db**

#### Related issues

| Issue Number | Description                                              |
|--------------|----------------------------------------------------------|
| #6967        | Change the "zulip" realm from populate_db to be more     |
| #14958       | populate_db --nodelete is nonfunctional                  |
| #14991       | Make populate_db generated messages/data like a real     |
| #6020        | dev tooling: Make streams and initial messages more like |
| #14664       | Include lear realm in development environment            |

populate\_db is a highly useful tool for testing Zulip in a local development environment.

I will be working on making it simulate a real-life production install along with setting up realms, users, etc.

As of now, one can't add more messages to the database while preserving the current ones using the "--nodelete" option. I will work on fixing this bug and adding ways to simulate file uploads.

#### **3. Add a way to publish test results in Github Actions**

#### Related issue

Github Actions doesn't support publishing test results yet.

Upstream discussion:

<https://github.community/t/publishing-test-results/16215>

So, one would have to go through logs deep down to find the failed tests.

There are some Actions that support publishing test results from a supported test result format (e.g. JUnit XML format). I will find ways to better integrate them in our CI so that one could easily see a quick summary of the tests along with the failed tests.

#### **4. Extend Slack meta-integration and other Slack integration issues**

#### Related issue

| Issue Number | Description                                             |
|--------------|---------------------------------------------------------|
| #9004        | Improve how Slack import handles Slack "file mentions"  |
| #9006        | Improve how we import Slack threads into Zulip          |
| #2047        | I own my own words: one-click export of my own messages |

Zulip currently supports a Slack meta-integration which lets users put a Zulip webhook URL in place of the Slack server URL. This allows us to receive messages from integrations that Zulip doesn't currently support or are made only for Slack. However, it's quite limited now. I will work on making it more compatible with more Slack integrations.

#### **5. Make it easy to import from RocketChat**

#### Related issue

There exists a pull request [#16683](https://github.com/zulip/zulip/pull/16683) which aims to solve this issue but hasn't been active for quite some time. I will rebase it and resolve conflicts to make it mergeable.

#### **6. Add more entries to RealmAuditLog**

| Issue Number | Description                                                |
|--------------|------------------------------------------------------------|
| #12630       | realmauditlog: Add entries for all administrative actions. |
| #11422       | import: Add RealmAuditLog entries for users.               |
| #13245       | billing: Add RemoteRealmAuditLog.                          |
| #10274       | RealmAuditLog: Add an old_value and new_value field, and   |

Few of these issues already have pull requests which are quite old and not up to date. I will work on rebasing them and making them mergeable. This set of issues will likely have follow-up projects so I will make sure to allocate sufficient time to these.

#### **7. Add more integrations**

#### Related issue

| Issue Number | Description                                              |
|--------------|----------------------------------------------------------|
| #5142        | Confluence Integration                                   |
| #9221        | Add a proper webhook-style integration for phabricator   |
| #10907       | Add support for incoming webhooks with a callback to the |

Some of these already have pull requests which are quite old and not up to date. I will work on rebasing them and making them mergeable.

The last issue will make it possible to have a framework allowing our incoming webhook type bots to contact an API (as a callback). This allows us to have more fleshed out integrations with webhooks which don't have data required by us to create meaningful messages. I felt the need for such a framework while working on adding the Wekan integration [#17551](https://github.com/zulip/zulip/pull/17551) since Wekan's webhook was quite limited.

#### **8. Improve zulip-js and migrate it to Typescript**

zulip-js isn't at par with python-zulip-api as of now. I will work on implementing the remaining endpoints and also migrating it to Typescript.

#### **9. Stretch goal: Upgrade tornado to the latest version**

#### Related issue

Zulip uses one of tornado's features, set\_blocking\_log\_threshold, which allows us to catch situations when the IOLoop is blocked for longer than expected. It also helps us in logging idle time, basically monitoring the IOLoop which helps in debugging.

However, tornado dropped this feature in version 5 onwards and has now moved to fully using asyncio for its internals. This has caused us to be stuck on version 4 for more than 2 years.

I will figure out a way to achieve the same monitoring ability in the latest version of tornado which will let us upgrade and benefit from the various improvements tornado has added since then.

This may give rise to many other compatibility issues, because of our tornado being a bit old, which will spur out many follow-up projects. So, I have added this as a stretch goal.

#### 10.**Stretch goal: Work on improving docker-zulip**

docker-zulip is a great way to install Zulip in a container. But it isn't at par with the normal installer yet. Most of the work here will be to troubleshoot the issues users have raised and fixing them. Also, make it easier and less error-prone to configure it.

### <span id="page-8-0"></span>**Proposed Timeline**

### **Community Bonding Period**

- Continue work on existing open PRs
- Discuss approach regarding CI set up for Fedora
- Figure out better base images (UBI vs docker images)
- Start doing preparatory changes for some of the mentioned tasks

### **Week 1 - 2**

- Start working on Fedora CI
- Deploy CI Fedora images on Docker Hub
- Run installation tests and backend- tests on Fedora CI
- Iterate on any follow-up projects

### **Week 3 - 4**

- Start work on populate\_db
- SImulate a real-life production install in populate\_db
- Start working on zulip-js
- Migrate zulip-js to Typescript

### **Week 5**

- Figure a good way to publish test results on Github Actions
- Start implementing the same
- Figure out a way to generate test results in a standard test result format (e.g. JUnit XML)

### **Week 6**

- Start adding the mentioned integrations
- If possible, figure out a way to make it easy for non-technical users to setup integrations in Zulip
- Start rebasing the existing PR on "incoming webhooks with a callback to the third-party server"
- Iterate on ways to improve existing integrations

### **Week 7 - 8**

- Start work on improving the import/export tool for Slack

- Find ways and implement to improve the existing Slack meta integration
- Allocate time for any follow-up projects from integrations

### **Week 9 - 10**

- Start extending the RealmAuditLog model
- Refactor code related to it
- Complete any follow-up projects regarding it
- Complete any pending work or follow-ups task from the above tasks
- Write a product report
- If time permits, complete the stretch goals

This is a rough estimate of the timeline. Priorities may change with time. I will make sure to adapt to those.

# <span id="page-9-0"></span>**Personal projects**

- I have recently started packaging for Debian and am currently the maintainer of two small libraries used by the Caddy web server, written in Golang.
  - golang-github-libdns-libdns-dev (Uploaded to Debian sid) <https://packages.debian.org/sid/golang-github-libdns-libdns-dev>
  - golang-github-mholt-acmez (Uploaded to mentors.debian.net, yet to be uploaded to Debian sid) <https://mentors.debian.net/package/golang-github-mholt-acmez/>
- [Bodhitree-Scrapper](https://github.com/ganpa3/Bodhitree-Scrapper) My college has been using Bodhitree (by IIT Bombay) as an educational platform during this lockdown. But it doesn't provide an API to easily fetch data, e.g. uploaded quizzes, pending quizzes, assignments, links of videos to download them, etc. So, I wrote this Selenium-based web crawler that does all of these!

# <span id="page-10-0"></span>**Why Zulip and why me?**

I personally like Zulip a lot. The way it encourages the use of streams and topics to better manage long conversations is just awesome. It makes it so easy to better focus on the important aspects of a conversation right now and catch up later for the rest. Working with the Zulip community has taught me so much about good software engineering practices. After all, it's what made me realize the importance of good and nicely structured commit messages

I have been contributing to Zulip for the last 4 months. In these 4 months, I have learned a lot about how Zulip works and how the codebase is structured. I have fixed many bugs, added new platform support and integrations and a lot more.

I enjoy working on open source projects and solving real life problems. I assure that my experience and commitment will make my project successful.

# <span id="page-10-1"></span>**Availability**

I have no other commitments this summer, so GSoC will be my only priority.

My university hasn't yet released the schedule of the final exams, but I guess it will be around the end of May or early June. If that's the case, I will be able to focus completely during the coding phase (7 June - 16 Aug).

If, after exams, my university timings coincide with the timeline, I won't have any exams, tests, or assignments. So, I will be able to devote ample time to work on the project.

I will keep my status updated in #checkins regularly

# <span id="page-10-2"></span>**Post GSoC**

I have been involved with the Zulip community for the last 4 months and will keep doing so after GSoC ends. Zulip has a very friendly community and I will make sure that new people coming to Zulip feel the same.

I will try my hands on docker-zulip and hopefully become it's maintainer.