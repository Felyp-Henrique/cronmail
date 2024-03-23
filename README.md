<strong>Attention: This project together your documentation, is still in start building!</strong>

# rmail

A simple tool to remove emails. Here some things that you can do:

* [ ] List all emails in your mailbox;
* [x] List all emails address senders in your mailbox;
* [x] List all mailboxes;
* [ ] Remove all emails in your mailbox;
* [x] Remove all emails by senders in your mailbox;
* [ ] Deletions scheduler;

Here some services/providers support:

* [ ] Any IMAP Server;
* [x] Gmail IMAP Server;

## Running the command:

In this section, there are some example to how is run this command.

### Running in Google Email

Get a Help:

```bash
$ rmail gmail # or use it with --help option
```

List of mailboxes:

```bash
$ rmail gmail mailboxes --password '<PASSWORD>' youremail@gmail.com
```

List of senders:

```bash
$ rmail gmail senders --password '<PASSWORD>' youremail@gmail.com
```

Delete all emails about a sender:

```bash
$ rmail gmail senders:delete --password '<PASSWORD>' youremail@gmail.com sender@gmail.com
```
