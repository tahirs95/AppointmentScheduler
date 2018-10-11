from calendar import HTMLCalendar
from datetime import datetime as dtime, date, time
import datetime
from .models import Event, TimeSlots
from django.db.models import Q


class EventCalendar(HTMLCalendar):
    def __init__(self, my_year=None, my_month=None, events=None):
        super(EventCalendar, self).__init__()
        self.year = my_year
        self.month = my_month
        self.events = events

    def formatday(self, day, weekday, events):
        """
        Return a day as a table cell.
        """
        if day != 0:
            dateofthisblock = datetime.date(self.year, self.month, day)
        else:
            dateofthisblock = ''
        actual_date = str(dateofthisblock)
        events_from_day = events.filter(event_date__day=day)
        events_html = "<ul>"
        for event in events_from_day:
            if event.available == 0:
                events_html += event.get_absolute_url() + " (Purchased)<br>"
            else:
                events_html += event.get_absolute_url() + "<br>"
        events_html += "</ul><select class='id_check'><option value=''>Add New</option><br>"
        if day != 0:
            time_slot = TimeSlots.objects.filter(~Q(event__event_date=actual_date))
            for timeset in time_slot:
                a = '/new/' + str(timeset.start) + '/' + actual_date + '/';
                events_html += "<option value='" + a + "'>" + timeset.start.strftime(
                    "%I:%M %p") + '-' + timeset.end.strftime("%I:%M %p") + "</option><br>"
        events_html += "</select>"

        if day == 0:
            return '<td class="noday">&nbsp;</td>'  # day outside month
        else:
            return '<td class="%s">%d%s</td>' % (self.cssclasses[weekday], day, events_html)

    def formatweek(self, theweek, events):
        """
        Return a complete week as a table row.
        """
        s = ''.join(self.formatday(d, wd, events) for (d, wd) in theweek)
        return '<tr>%s</tr>' % s

    def formatmonth(self, theyear, themonth, withyear=True):
        """
        Return a formatted month as a table.
        """

        events = Event.objects.filter(event_date__month=themonth)

        v = []
        a = v.append
        a('<table border="0" cellpadding="0" cellspacing="0" class="month">')
        a('\n')
        a(self.formatmonthname(theyear, themonth, withyear=withyear))
        a('\n')
        a(self.formatweekheader())
        a('\n')
        for week in self.monthdays2calendar(theyear, themonth):
            a(self.formatweek(week, events))
            a('\n')
        a('</table>')
        a('\n')
        return ''.join(v)
