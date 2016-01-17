#!/usr/bin/env python

import smtplib, subprocess, gzip
from email.mime.text import MIMEText


def send_mail(sender, receivers, message):

    try:
        smtpObj = smtplib.SMTP('localhost', 25)
        smtpObj.sendmail(sender, receivers, message)
        print "Successfully sent email"
    except SMTPException:
        print "Error: unable to send email"


def dump_database(db_host, db_user, db_pass, sql_dump_filename):
    args = ["mysqldump", "-h", db_host, "-u", db_user, "-p" + db_pass, "--max_allowed_packet=512M", "--all-databases", "--ignore-table=mysql.event"]

    with open(sql_dump_filename, 'w', 0) as f:
        p = subprocess.Popen(args, stdout=subprocess.PIPE)
        f.write(p.communicate()[0])
        with gzip.open(f) as file_in:
            sql_dump_filename.writelines(file_in)
        f.close()

        return p.returncode


def main():
    # Check how to add date timestamp to filename

    sender = "atlassian_mysql@eda-tech.com"
    receivers = ["borisy@delatek.com", "monitor@secureemail.biz"]

    return_code = dump_database("localhost", "root", "1234", "/home/veeambackup/atlassian-all-$(date +%Y%m%d).sql")

    if return_code == 0:
        print "Atlassian MySQL Backup - OK"
        send_mail(sender, receivers, "Atlassian MySQL Backups - OK" "MySQL Backup completed successfully OK")
    else:
        print "Atlassian MySQL Backups gave an ERROR !"
        send_mail(sender, receivers, "Atlassian MySQL Backups - Gave an ERROR!" "MySQL Backup failed - Need to investigate!!")


if __name__ == "__main__":
    main()

# Get timestamp to add to filename
# Remove old dumps should keep only 3.