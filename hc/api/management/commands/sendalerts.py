import logging
import time
from concurrent.futures import ThreadPoolExecutor
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.db import connection
from django.utils import timezone
from hc.api.models import Check

executor = ThreadPoolExecutor(max_workers=10)
logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Sends email alerts on status of checks'

    def handle_many(self):
        """ Send alerts for many checks simultaneously. """

        query = Check.objects.filter(user__isnull=False).select_related("user")

        running_checks = query.filter(
            Q(status="up") | Q(status="down"))

        now = timezone.now()
        repeat_list_approved = query.filter(
            alert_after__lt=now,
            status="down",
            nag_after_time__lt=now)
        repeat_list = query.filter(
            alert_after__lt=now,
            status="down")

        for check in repeat_list:
            if check.nag_after_time is None:
                check.nag_after_time = now + check.nag_intervals
                check.save()

        for check in repeat_list_approved:
            if (now - check.nag_after_time) > (check.nag_intervals):
                check.nag_after_time = now + check.nag_intervals
            else:

                check.nag_after_time = check.nag_after_time + \
                    check.nag_intervals
            check.save()

        if repeat_list_approved:
            checks = (
                list(
                    running_checks.iterator()) +
                list(repeat_list_approved))
        else:
            checks = (
                list(running_checks.iterator()) +
                list(repeat_list_approved.iterator()))

        if not checks:
            return False

        # Solve the problem of the difference of the nag_after_time and now()
        # being huge
        futures = [executor.submit(self.handle_one, check) for check in checks]
        for future in futures:
            future.result()

        return True

    def handle_one(self, check):
        """ Send an alert for a single check.

        Return True if an appropriate check was selected and processed.
        Return False if no checks need to be processed.

        """

        try:
            if connection.connection is None:
                connection.ensure_connection()
        except Exception:
            self.stdout.write(
                "Error starting: "
                "Connection to database cannot be established.")

        # Save the new status. If sendalerts crashes,
        # it won't process this check again.
        check.status = check.get_status()
        check.save()

        tmpl = "\nSending alert, status=%s, code=%s\n"
        self.stdout.write(tmpl % (check.status, check.code))

        if check.runs_too_often:
            self.stdout.write("Check %s is running too often" % check.name)

        errors = check.send_alert()
        for ch, error in errors:
            self.stdout.write("ERROR: %s %s %s\n" % (ch.kind, ch.value, error))

        connection.close()
        return True

    def handle(self, *args, **options):
        self.stdout.write("sendalerts is now running")

        ticks = 0
        while True:
            if self.handle_many():
                ticks = 1
            else:
                ticks += 1

            time.sleep(1)
            if ticks % 60 == 0:
                formatted = timezone.now().isoformat()
                self.stdout.write("-- MARK %s --" % formatted)
